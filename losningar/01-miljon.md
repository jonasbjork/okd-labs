# Lösningsförslag 01: CLI, projekt och webbgränssnitt

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/01-miljon.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc version --client
oc version
oc whoami
oc whoami --show-server
oc project
oc get pods,deployments,services,routes,configmaps,secrets,pvc
oc create configmap orientation --from-literal=course=ex180
oc get configmap orientation -o yaml
oc explain pod.spec.containers
```

Ändra `data.course` i webbgränssnittet och spara. CLI läser därefter det uppdaterade
API-objektet. Gör aldrig webbändringen i `metadata.managedFields` eller `status`.

## Vanliga fel och vad de betyder

`Forbidden`: kontrollera `oc auth can-i create configmaps` och projektbehörighet.
`oc get all` missar bland annat din ConfigMap, eftersom `all` är en API-kategori.
