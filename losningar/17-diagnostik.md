# Lösningsförslag 17: Samla diagnostik och klusterunderlag

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/17-diagnostik.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
mkdir -p .work/diagnostik-17
oc project -q > .work/diagnostik-17/project.txt
date -u > .work/diagnostik-17/time.txt
oc get deployment,replicaset,pods,service -o yaml > .work/diagnostik-17/resources.yaml
oc get events --sort-by=.metadata.creationTimestamp -o yaml > .work/diagnostik-17/events.yaml
oc describe deployment web > .work/diagnostik-17/deployment.txt
oc logs deployment/web --timestamps > .work/diagnostik-17/web.log
```

## Analys av lärarens underlag

Läraren genomför insamlingen enligt [lärarhandledningen](../docs/lararhandledning.md).
Elevens uppgift är att jämföra det tilldelade utdraget med projektets eget underlag:

- Koppla ett resursnamn och ett projekt till rätt applikation.
- Jämför loggtid, eventtid och containerstatus innan du drar slutsatser.
- Förklara om felet hör till appens konfiguration eller behöver utredas på klusternivå.
- Formulera en konkret fråga till läraren med symptom, tidpunkt och redan kontrollerade hypoteser.

Exempel: Poden är Pending, PVC har inte bundits och events hänvisar till provisionering.
Eleven bifogar Pod- och PVC-events. Läraren utreder StorageClass/CSI på klusternivå.
Detta är en metod för analys, inte ett påhittat resultat från en genomförd insamling.

## Vanliga fel och vad de betyder

`Forbidden` vid en klusterresurs betyder inte att elevens projekt är trasigt.
Samla det du har rätt att läsa i projektet och be läraren om det saknade underlaget.
Byt inte konto eller försök ge appens service account klusterbehörighet.
