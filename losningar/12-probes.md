# Lösningsförslag 12: Readiness, liveness och startup

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/12-probes.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc set probe deployment/web --readiness --get-url=http://:8080/ready --period-seconds=5 --timeout-seconds=2 --failure-threshold=1
oc set probe deployment/web --liveness --get-url=http://:8080/live --period-seconds=5 --timeout-seconds=2 --failure-threshold=3
oc set probe deployment/web --startup --get-url=http://:8080/live --period-seconds=5 --timeout-seconds=2 --failure-threshold=30
oc rollout status deployment/web --timeout=180s
POD=$(oc get pods -l app=web -o jsonpath='{.items[0].metadata.name}')
oc get pod "$POD" -o jsonpath='{.metadata.uid}{" "}{.status.containerStatuses[0].restartCount}{"\n"}'
oc exec "$POD" -- touch /tmp/not-ready
oc get pod "$POD" -w
```

Avsluta watch med Ctrl-C när Ready blivit 0/1. Inspektera EndpointSlice:
Podens adress kan finnas kvar med `ready: false`. Testa direkt Pod-port-forward mot
`/` (200) och `/ready` (503). En redan etablerad Service-port-forward är inte ett
pålitligt test av nytt nätverksurval; använd EndpointSlice och en ny klientförbindelse.

```sh
oc exec "$POD" -- rm /tmp/not-ready
oc wait --for=condition=Ready "pod/$POD" --timeout=60s
oc exec "$POD" -- touch /tmp/fail-live
oc get pod "$POD" -w
```

Vänta på ökad restartCount och Ready 1/1. Containerns lager återställs vid omstart,
så flaggan försvinner. En flagga i en beständig volym hade kunnat ge en omstartsloop.

## Vanliga fel och vad de betyder

Probe mot `/` döljer våra simulerade fel: använd rätt sökväg. För sträng liveness
kan starta om en frisk men tillfälligt belastad process; granska timing och events.
