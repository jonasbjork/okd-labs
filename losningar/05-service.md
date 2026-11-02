# Lösningsförslag 05: Service, selectors och intern DNS

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/05-service.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc apply -f assets/service.yaml
oc run client --image=docker.io/library/python:3.12-slim --command -- sleep 3600
oc wait --for=condition=Ready pod/client --timeout=180s
oc exec client -- python -c 'import urllib.request; print(urllib.request.urlopen("http://web", timeout=5).status)'
oc patch service web --type=merge -p '{"spec":{"selector":{"app":"missing"}}}'
oc get endpointslices -l kubernetes.io/service-name=web -o yaml
```

Upprepa HTTP-anropet: det ska nu misslyckas. Återställ:

```sh
oc apply -f assets/service.yaml
oc scale deployment/web --replicas=2
oc rollout status deployment/web --timeout=180s
NS=$(oc project -q)
oc exec client -- python -c "import socket; print(socket.gethostbyname('web.${NS}.svc.cluster.local'))"
oc exec client -- python -c 'import urllib.request; print(urllib.request.urlopen("http://web", timeout=5).status)'
oc get endpointslices -l kubernetes.io/service-name=web -o yaml
```

Om klustret använder annan DNS-domän, använd den i stället för `cluster.local`.
Service gör nätverksval; den övervakar inte HTTP-hälsa utan en readiness-probe.

## Vanliga fel och vad de betyder

Tomma EndpointSlices: jämför Service-selector med Pod-labels. Timeout med rätt
endpoints: kontrollera targetPort, processens lyssningsadress och NetworkPolicies.
