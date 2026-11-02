# Lösningsförslag 08: Secret som miljö och fil

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/08-secret.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc create secret generic web-secret --from-literal=token=training-token-v1
oc patch deployment web --type=strategic -p '{"spec":{"template":{"spec":{"containers":[{"name":"web","env":[{"name":"LAB_TOKEN","valueFrom":{"secretKeyRef":{"name":"web-secret","key":"token"}}}]}]}}}}'
oc rollout status deployment/web --timeout=180s
```

Verifiera `/` med port-forward. Byt sedan till volym:

```sh
oc set env deployment/web LAB_TOKEN-
oc set volume deployment/web --add --name=secret --type=secret --secret-name=web-secret --mount-path=/etc/lab-secret --read-only=true
oc rollout status deployment/web --timeout=180s
oc create secret generic web-secret --from-literal=token=training-token-v2 --dry-run=client -o yaml | oc apply -f -
oc describe secret web-secret
```

En monterad Secret uppdateras asynkront, och vår app läser filen vid varje anrop.
Att skapa referensen kräver inte att du först hämtar värdet med `oc get secret -o yaml`.
Kubernetes kubelet hämtar monterade Secrets åt Poden; appen behöver inte själv
API-rättigheten `get secrets`. RBAC för användare som skapar Pods är ändå relevant.

## Vanliga fel och vad de betyder

`secret_loaded: false`: kontrollera namn, nyckeln `token` och mount-path.
Miljövärdet har företräde i appen; glömmer du ta bort det ser du inte effekten av tokenfilen.
