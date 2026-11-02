# Lösningsförslag 14: Autoskalning med kontrollerad belastning

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/14-hpa.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc set resources deployment/web --requests=cpu=100m,memory=64Mi --limits=cpu=250m,memory=128Mi
oc set probe deployment/web --readiness --get-url=http://:8080/ready --period-seconds=5 --timeout-seconds=2
oc rollout status deployment/web --timeout=180s
oc adm top pods
oc apply -f assets/hpa.yaml
oc create configmap load-code --from-file=load.py=assets/load.py
oc apply -f assets/load-job.yaml
oc get hpa web -w
```

Använd andra terminaler för `oc get pods -w` och `oc adm top pods`. Lastens trådar
kan skapa parallella HTTP-anrop; webbservern utför ett kort CPU-arbete per anrop.
När uppskalning är dokumenterad:

```sh
oc delete job load
oc get hpa web -w
```

Ta slutligen bort HPA om du vill experimentera med manuell skalning:
`oc delete hpa web`. Om lasten inte räcker i din miljö: kontrollera först att `/work`
anropas, att Jobben kör och att mätvärden finns. Öka inte maxReplicas för att lösa ett
mätfel. HPA skalar Pods, inte antalet klusternoder.

## Vanliga fel och vad de betyder

`FailedGetResourceMetric`: kontrollera metrics API, CPU-requests och HPA-events.
Desired replicas ökar men Pods är Pending: HPA fungerar men klustret saknar kapacitet.
`oc apply` av en gammal Deployment med replicas kan tillfälligt strida mot HPA:s skalning.
