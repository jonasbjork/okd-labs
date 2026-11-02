#!/usr/bin/env python3
"""Kontrollera kursfiler lokalt, utan åtkomst till Kubernetes/OKD."""
import ast
from contextlib import contextmanager
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def yaml_documents(path):
    result = subprocess.run(
        ['ruby', '-ryaml', '-rjson', '-e',
         'puts JSON.generate(YAML.load_stream(File.read(ARGV[0])) .compact)', str(path)],
        text=True, capture_output=True, check=True,
    )
    return json.loads(result.stdout)


def check_documents():
    labs = sorted(Path('labbar').glob('*.md'))
    solutions = sorted(Path('losningar').glob('*.md'))
    require(len(labs) == len(solutions) == 18, '18 uppgifter och lösningar krävs')
    for number, lab in enumerate(labs, 1):
        require(lab.name.startswith(f'{number:02}-'), f'Fel numrering: {lab}')
        require((Path('losningar') / lab.name).is_file(), f'Saknad lösning: {lab}')
    for path in [*labs, *solutions, Path('docs/forberedelser.md')]:
        text = path.read_text()
        require(not re.search(r'oc\s+(?:new-project|delete\s+(?:project|namespace)\b)', text),
                f'Projektadministration i elevmaterial: {path}')
        require('oc adm must-gather' not in text, f'Klusterinsamling som elevkommando: {path}')
    for lab in labs:
        text = lab.read_text()
        require('oc project "$LAB_PROJECT"' in text, f'Saknat tilldelat projekt: {lab}')
        for line in text.splitlines():
            if re.match(r'oc(?: -n "\$LAB_PROJECT")? delete ', line):
                require(line.startswith('oc -n "$LAB_PROJECT" delete '), f'Oavgränsad städning: {lab}')
                require('--all' not in line, f'För bred städning: {lab}')
    markdown = list(Path('.').rglob('*.md'))
    snippets = 0
    for path in markdown:
        if '.work' in path.parts:
            continue
        text = path.read_text()
        require(text.count('```') % 2 == 0, f'Oavslutat kodblock: {path}')
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
            if '://' in target or target.startswith('#'):
                continue
            require((path.parent / target.split('#')[0]).exists(), f'Trasig länk i {path}: {target}')
        for code in re.findall(r'```sh\n(.*?)```', text, re.S):
            subprocess.run(['bash', '-n'], input=code, text=True, check=True, capture_output=True)
            snippets += 1
    print(f'OK: 18 uppgifter, 18 lösningar, elevbehörigheter, avgränsad städning, länkar och {snippets} shellblock')


def check_manifests():
    files = sorted(Path('assets').rglob('*.yaml')) + sorted(Path('losningar').glob('*.yaml'))
    count = 0
    for path in files:
        for obj in yaml_documents(path):
            count += 1
            require(all(k in obj for k in ('apiVersion', 'kind', 'metadata')), f'Ofullständigt objekt: {path}')
            require(isinstance(obj['metadata']['name'], str), f'Saknat namn: {path}')
            if obj['kind'] == 'Deployment':
                labels = obj['spec']['template']['metadata']['labels']
                selector = obj['spec']['selector']['matchLabels']
                require(all(labels.get(k) == v for k, v in selector.items()), f'Deployment-selector: {path}')
                spec = obj['spec']['template']['spec']
            elif obj['kind'] == 'Pod':
                spec = obj['spec']
            elif obj['kind'] == 'Job':
                spec = obj['spec']['template']['spec']
            else:
                continue
            volumes = {v['name'] for v in spec.get('volumes', [])}
            for container in spec['containers']:
                require(isinstance(container['image'], str), f'Image ska vara sträng: {path}')
                for env in container.get('env', []):
                    require(not ('value' in env and 'valueFrom' in env), f'Dubbla env-källor: {path}')
                    if 'value' in env:
                        require(isinstance(env['value'], str), f'Env ska vara sträng: {path}')
                for mount in container.get('volumeMounts', []):
                    require(mount['name'] in volumes, f'Odefinierad volym: {path}')
    # Integrationskedjans relationer kontrolleras som en helhet.
    stack = yaml_documents(Path('losningar/15-stack.yaml'))
    objects = {(o['kind'], o['metadata']['name']): o for o in stack}
    for name in ('web', 'backend'):
        deploy = objects['Deployment', name]
        service = objects['Service', name]
        pod = deploy['spec']['template']
        require(service['spec']['selector'] == pod['metadata']['labels'], f'Service-selector {name}')
        container = pod['spec']['containers'][0]
        require(service['spec']['ports'][0]['targetPort'] == container['ports'][0]['name'], f'TargetPort {name}')
        for field in ('readinessProbe', 'livenessProbe', 'startupProbe'):
            require(container[field]['httpGet']['port'] == 'http', f'Probe-port {name}')
        for env in container['env']:
            ref = env.get('valueFrom', {}).get('configMapKeyRef')
            if ref:
                require(ref['key'] in objects['ConfigMap', ref['name']]['data'], f'ConfigMap-nyckel {name}')
        for volume in pod['spec']['volumes']:
            if 'persistentVolumeClaim' in volume:
                require(('PersistentVolumeClaim', volume['persistentVolumeClaim']['claimName']) in objects, 'Saknad PVC')
            if 'secret' in volume:
                require(('Secret', volume['secret']['secretName']) in objects, 'Saknad Secret')
    require(objects['Deployment', 'backend']['spec']['strategy']['type'] == 'Recreate', 'Backend-strategi')
    require(objects['Route', 'web']['spec']['to']['name'] == 'web', 'Route pekar fel')
    print(f'OK: {len(files)} YAML-filer, {count} objekt och integrationskedjans referenser')


def check_cli():
    if not shutil.which('oc'):
        print('EJ KÖRT: lokala oc-kontroller (oc saknas)')
        return
    result = subprocess.run(['oc', 'process', '--local', '-f', 'assets/template.yaml',
                             '-p', 'NAME=demo', '-p', 'MESSAGE=Kontroll', '-o', 'json'],
                            text=True, capture_output=True, check=True)
    objects = json.loads(result.stdout)['items']
    require({o['metadata']['name'] for o in objects} == {'demo'}, 'Template-parametrisering')
    require('${' not in result.stdout, 'Oersatt mallparameter')
    transforms = [
        ['set', 'volume', '--add', '--name=config', '--type=configmap', '--configmap-name=web-config', '--mount-path=/etc/lab-config', '--read-only=true'],
        ['set', 'volume', '--add', '--name=secret', '--type=secret', '--secret-name=web-secret', '--mount-path=/etc/lab-secret', '--read-only=true'],
        ['set', 'volume', '--add', '--name=data', '--type=persistentVolumeClaim', '--claim-name=web-data', '--mount-path=/data'],
        ['set', 'probe', '--readiness', '--get-url=http://:8080/ready', '--period-seconds=5', '--timeout-seconds=2', '--failure-threshold=1'],
        ['set', 'probe', '--liveness', '--get-url=http://:8080/live', '--period-seconds=5', '--timeout-seconds=2', '--failure-threshold=3'],
        ['set', 'probe', '--startup', '--get-url=http://:8080/live', '--period-seconds=5', '--timeout-seconds=2', '--failure-threshold=30'],
        ['set', 'resources', '--requests=cpu=100m,memory=64Mi', '--limits=cpu=250m,memory=128Mi'],
    ]
    for cmd in transforms:
        result = subprocess.run(['oc', *cmd, '--local', '-f', 'assets/app-deployment.yaml', '-o', 'json'],
                                text=True, capture_output=True, check=True)
        require(json.loads(result.stdout)['kind'] == 'Deployment', 'CLI-transformering')
    print('OK: lokal Template-bearbetning och sju oc-transformeringar (utan API-anrop)')


@contextmanager
def environment(values):
    old = {k: os.environ.get(k) for k in values}
    for key, value in values.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    try:
        yield
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def check_server():
    for path in Path('assets').glob('*.py'):
        ast.parse(path.read_text(), filename=str(path))
    with tempfile.TemporaryDirectory(prefix='okd-labs-') as temp:
        folder = Path(temp)
        for name in ('config', 'secret', 'data', 'flags'):
            (folder / name).mkdir()
        values = {f'{k}_DIR': str(folder / v) for k, v in [('CONFIG', 'config'), ('SECRET', 'secret'), ('DATA', 'data'), ('FLAG', 'flags')]}
        values.update(MESSAGE='Kontrollhälsning', APP_VERSION='v2', LAB_TOKEN=None, BACKEND_URL=None)
        with environment(values):
            spec = importlib.util.spec_from_file_location('lab_server', ROOT / 'assets/server.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            class QuietHandler(module.Handler):
                def log_message(self, *args):
                    pass
            server = module.ThreadingHTTPServer(('127.0.0.1', 0), QuietHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base = f'http://127.0.0.1:{server.server_port}'

            def request(path, data=None, token=None):
                headers = {'X-Lab-Token': token} if token else {}
                req = Request(base + path, data=data, headers=headers)
                try:
                    with urlopen(req, timeout=5) as response:
                        return response.status, json.load(response)
                except HTTPError as error:
                    return error.code, json.load(error)
            try:
                status, body = request('/')
                require(status == 200 and body['message'] == 'Kontrollhälsning' and body['version'] == 'v2', 'Grundsvar')
                require(body['secret_loaded'] is False, 'Secret utan token')
                (folder / 'config/message').write_text('Filversion 1')
                require(request('/')[1]['file_message'] == 'Filversion 1', 'ConfigMap-fil')
                (folder / 'config/message').write_text('Filversion 2')
                require(request('/')[1]['file_message'] == 'Filversion 2', 'Omläsning av fil')
                for endpoint, flag in [('/ready', 'not-ready'), ('/live', 'fail-live')]:
                    require(request(endpoint)[0] == 200, f'Frisk {endpoint}')
                    (folder / 'flags' / flag).touch()
                    require(request(endpoint)[0] == 503, f'Felande {endpoint}')
                    (folder / 'flags' / flag).unlink()
                    require(request(endpoint)[0] == 200, f'Återställd {endpoint}')
                require(request('/state', b'nekas', 'wrong')[0] == 403, 'Skrivning utan Secret')
                (folder / 'secret/token').write_text('training-token-v1')
                require(request('/')[1]['secret_loaded'] is True, 'Monterad Secret')
                require('training-token-v1' not in json.dumps(request('/')[1]), 'Token läcker i svar')
                require(request('/state', b'marker', 'training-token-v1')[0] == 200, 'Autentiserad skrivning')
                require(request('/state', b'fel', 'wrong')[0] == 403, 'Fel token nekas')
                require(request('/state')[1]['value'] == 'marker', 'Nekad skrivning ändrar inte data')
                (folder / 'secret/token').write_text('training-token-v2')
                require(request('/state', b'fel', 'training-token-v1')[0] == 403, 'Gammal token efter rotation')
                require(request('/state', b'marker2', 'training-token-v2')[0] == 200, 'Roterad Secret-fil')
                require(request('/state', b'x' * 4097, 'training-token-v2')[0] == 400, 'Skrivgräns')
                require((folder / 'data/state.txt').read_text() == 'marker2', 'Faktisk lagring')
                require(request('/backend')[0] == 503, 'Saknad backend')
                os.environ['BACKEND_URL'] = base + '/'
                require(request('/backend')[1]['backend']['message'] == 'Kontrollhälsning', 'Backend-anrop')
                require(request('/work')[0] == 200, 'CPU-endpoint')
                require(request('/does-not-exist')[0] == 404, 'Fel sökväg för probe-labb')
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)
    print('OK: riktiga HTTP-anrop, filkonfiguration, probes, tokenrotation, skrivgräns, lagring och backend')


if __name__ == '__main__':
    check_documents()
    check_manifests()
    check_cli()
    check_server()
    print('Lokala kontroller klara. Klustrets admission, SCC, routing, CSI och HPA kräver OKD-körning.')
