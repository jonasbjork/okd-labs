# Lösningsförslag 03: En Pod från kommando till YAML

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/03-pod.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc run first --image=docker.io/library/python:3.12-slim --port=8080 --command -- python -m http.server 8080 --bind 0.0.0.0 --directory /tmp
oc wait --for=condition=Ready pod/first --timeout=180s
oc describe pod first
oc logs first
oc port-forward pod/first 18083:8080
```

Testa i annan terminal: `curl -fsS http://127.0.0.1:18083/`. Avsluta tunneln.

```sh
mkdir -p .work
oc run second --image=docker.io/library/python:3.12-slim --port=8080 --dry-run=client -o yaml --command -- python -m http.server 8080 --bind 0.0.0.0 --directory /tmp > .work/pod.yaml
oc apply -f .work/pod.yaml
oc wait --for=condition=Ready pod/second --timeout=180s
oc delete pod first
oc get pods
```

Upprepa port-forward för `second`. Ett genererat manifest är en startpunkt: läs det
innan du tillämpar det och jämför med API-hjälpen.

## Vanliga fel och vad de betyder

`CrashLoopBackOff`: se `oc logs second --previous` och kommandot i manifestet.
`ImagePullBackOff`: kontrollera image-namn och pull-events. En Pod-IP är normalt inte
nåbar direkt från din laptop.
