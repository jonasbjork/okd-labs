# Lösningsförslag 16: Felsökningsverkstad med förberedda fel

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/16-felsokning.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

| Fall | Grundorsak | Riktad åtgärd |
| --- | --- | --- |
| 01 | Service väljer app=wrong | Ändra selector till app=web |
| 02 | Service targetPort 9999 saknar lyssnare | Återställ targetPort till http |
| 03 | Deployment använder en image-tagg som inte finns | Återställ python:3.12-slim |
| 04 | Readiness söker /does-not-exist, som ger 404 | Ändra till /ready |
| 05 | MESSAGE refererar till en saknad ConfigMap | Skapa missing-config med rätt MESSAGE-nyckel |

```sh
# 01 och 02
oc apply -f assets/service.yaml
# 03
oc set image deployment/web web=docker.io/library/python:3.12-slim
# 04
oc set probe deployment/web --readiness --get-url=http://:8080/ready --period-seconds=5
# 05
oc create configmap missing-config --from-literal='MESSAGE=Återställd konfiguration'
```

Utför endast åtgärden för det aktiva fallet. För 05 kan du också ändra referensen till
en existerande avsedd ConfigMap efter att ha dokumenterat kravet. Baslinjeåterställning
innan nästa fall hindrar att flera avsiktliga fel blandas ihop.

Fall 01–02 har ofta friska Pods men trasig Service-trafik. Fall 03 visar image-pull-events.
Fall 04 visar probe-fel och ej redo endpoint. Fall 05 visar CreateContainerConfigError;
processen har inte startat, så applikationsloggar räcker inte som diagnos.

## Vanliga fel och vad de betyder

Om ett gammalt ReplicaSet fortsätter servera trafik kan Route fortfarande svara trots
fel i den nya Pod-mallen. Kontrollera därför alltid både utrullning och HTTP.
Fil 05 fungerar inte som nytt mysterium om missing-config finns kvar: radera den efter återställning.
