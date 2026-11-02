# Lösningsförslag 13: Requests, limits och ett minnesfel

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/13-resurser.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc set resources deployment/web --requests=cpu=100m,memory=64Mi --limits=cpu=250m,memory=128Mi
oc rollout status deployment/web --timeout=180s
oc apply -f assets/memory-test.yaml
oc get pod memory-test -w
```

Avsluta watch när Poden har avslutats. Läs:

```sh
oc get pod memory-test -o jsonpath='{.status.containerStatuses[0].state.terminated}{"\n"}'
oc delete pod memory-test
oc apply -f assets/schedule-test.yaml
oc describe pod schedule-test
oc delete pod schedule-test --ignore-not-found
oc get pods -l app=web -o jsonpath='{.items[*].status.qosClass}{"\n"}'
```

Olika requests och limits ger här normalt Burstable. Exit 137 ensam bevisar inte
OOM; läs reason. En miljö med ytterligare gränser kan ge ett tidigare avslag.
Minnestestet begär en begränsad total mängd och har activeDeadlineSeconds.

## Vanliga fel och vad de betyder

MemoryError i stället för OOMKilled kan bero på en ytterligare processgräns;
dokumentera reason och loggar. Hög request konsumerar ingen CPU i en oschemalagd Pod,
men städa bort testet så att det inte ligger kvar som väntande arbete.
