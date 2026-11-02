# Lösningsförslag 09: PVC och data efter Pod-byte

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/09-pvc.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc create secret generic web-secret --from-literal=token=training-token-v1
oc set volume deployment/web --add --name=secret --type=secret --secret-name=web-secret --mount-path=/etc/lab-secret --read-only=true
oc apply -f assets/pvc.yaml
oc patch deployment web --type=merge -p '{"spec":{"strategy":{"type":"Recreate","rollingUpdate":null}}}'
oc set volume deployment/web --add --name=data --type=persistentVolumeClaim --claim-name=web-data --mount-path=/data
oc rollout status deployment/web --timeout=240s
oc get pvc web-data
oc port-forward service/web 18080:80
```

I annan terminal:

```sh
curl -fsS -H 'X-Lab-Token: training-token-v1' --data-binary 'Min beständiga anteckning' http://127.0.0.1:18080/state
curl -sS -o /dev/null -w '%{http_code}\n' -H 'X-Lab-Token: wrong' --data-binary 'ska nekas' http://127.0.0.1:18080/state
curl -fsS http://127.0.0.1:18080/state
```

Avsluta tunneln och ersätt Poden:

```sh
POD=$(oc get pods -l app=web -o jsonpath='{.items[0].metadata.name}')
oc get pod "$POD" -o jsonpath='{.metadata.uid}{"\n"}'
oc delete pod "$POD"
oc rollout status deployment/web --timeout=240s
oc get pods -l app=web -o custom-columns=NAME:.metadata.name,UID:.metadata.uid
```

Starta om port-forward och läs `/state`. PVC ägs inte av Poden och finns kvar när
Poden byts. Städningen tar senare bort PVC-objektet; själva elevprojektet behålls.

## Vanliga fel och vad de betyder

Pending PVC utan konsument: kontrollera bindingMode. Pending med konsument: se
`oc describe pvc web-data` och Pod-events. 500 vid skrivning: undersök `/data`-rättigheter,
CSI-drivrutinens fsGroup-stöd och om volymen är skrivbar. Ändra inte till root som standardlösning.
