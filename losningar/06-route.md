# Lösningsförslag 06: Route, HTTP och TLS

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/06-route.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc expose service web --port=http
HOST=$(oc get route web -o jsonpath='{.spec.host}')
curl -fsS "http://${HOST}/"
oc create route edge web-tls --service=web --port=http --insecure-policy=Redirect
TLS_HOST=$(oc get route web-tls -o jsonpath='{.spec.host}')
curl -fsS "https://${TLS_HOST}/"
curl -sS -D - -o /dev/null "http://${TLS_HOST}/"
oc get route web-tls -o jsonpath='{.status.ingress[*].conditions}{"\n"}'
```

Använd `--cacert` för HTTPS om din CA inte finns i datorns trust store.
Omdirigeringstestet använder inte `-L`, eftersom vi vill se första svarets status
(typiskt 301/302) och Location. En vanlig HTTP-Route kan blockeras av klustrets policy;
notera då policyn och använd tillåten TLS-åtkomst.

## Vanliga fel och vad de betyder

DNS-fel: kontrollera apps-domänens uppslag. 503 från routern: kontrollera Service,
endpoints och readiness. Certifikatfel: kontrollera CA, värdnamn och datum.
