# Lösningsförslag 04: Deployment, repliker och självläkning

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/04-deployment.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc apply -f assets/basic-deployment.yaml
oc rollout status deployment/web --timeout=180s
```

```sh
oc scale deployment/web --replicas=3
oc rollout status deployment/web --timeout=180s
oc get pods -l app=web -o wide
POD=$(oc get pods -l app=web -o jsonpath='{.items[0].metadata.name}')
oc get pod "$POD" -o jsonpath='{.metadata.uid}{" "}{.metadata.ownerReferences}{"\n"}'
oc delete pod "$POD"
oc rollout status deployment/web --timeout=180s
oc get pods -l app=web
oc scale deployment/web --replicas=1
oc rollout status deployment/web --timeout=180s
```

Podens ägare är ett ReplicaSet. Läs sedan ReplicaSetets ownerReferences för att
hitta Deploymenten. `oc get pods -w` i en annan terminal visar förloppet.

## Vanliga fel och vad de betyder

En ersättare fastnar Pending: `oc describe pod` visar exempelvis resursbrist.
Ingen ersättare: kontrollera att du raderade en Pod som faktiskt ägs av Deploymenten.
