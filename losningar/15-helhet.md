# Lösningsförslag 15: Bygg en sammanhängande applikation

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/15-helhet.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

Ett komplett möjligt manifest finns i [15-stack.yaml](15-stack.yaml).
Läs det och jämför med dina egna filer innan du använder det.

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py
oc apply -f losningar/15-stack.yaml
oc rollout status deployment/backend --timeout=240s
oc rollout status deployment/web --timeout=240s
HOST=$(oc get route web -o jsonpath='{.spec.host}')
curl -fsS "https://${HOST}/"
curl -fsS "https://${HOST}/backend"
oc port-forward service/backend 18081:80
```

Använd rätt CA vid behov. I en annan terminal:

```sh
curl -fsS -H 'X-Lab-Token: training-token-v1' --data-binary 'integration-marker' http://127.0.0.1:18081/state
curl -fsS http://127.0.0.1:18081/state
curl -sS -o /dev/null -w '%{http_code}\n' -H 'X-Lab-Token: wrong' --data-binary 'nekas' http://127.0.0.1:18081/state
```

Avsluta tunneln och ersätt backend-Poden:

```sh
oc delete pod -l app=backend
oc rollout status deployment/backend --timeout=240s
POD=$(oc get pods -l app=web -o jsonpath='{.items[0].metadata.name}')
oc delete pod "$POD"
oc rollout status deployment/web --timeout=240s
```

En frontend-Pod ersätts medan den andra kan fortsätta ta emot trafik. Starta om
backend-port-forward och läs tillbaka markören. Testa Route igen.

## Vanliga fel och vad de betyder

Multi-Attach vid backenduppdatering: kontrollera Recreate och att en gammal Pod
släppt volymen. Backend 502: kontrollera BACKEND_URL, Service-selector och endpoints.
Secret-värdet i lösningsfilen är avsiktligt ett publikt fiktivt övningsvärde.
