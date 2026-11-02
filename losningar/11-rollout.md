# Lösningsförslag 11: Utrullning och återställning

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/11-rollout.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc scale deployment/web --replicas=2
oc set env deployment/web APP_VERSION=v2
oc rollout status deployment/web --timeout=180s
oc set image deployment/web web=docker.io/library/python:ex180-does-not-exist
oc rollout status deployment/web --timeout=60s
oc get pods -l app=web
oc get events --sort-by=.metadata.creationTimestamp
oc rollout history deployment/web
oc rollout undo deployment/web
oc rollout status deployment/web --timeout=180s
oc get deployment web -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
```

Verifiera v2 med port-forward. En ändring av `APP_VERSION` ger en revision precis som
ett imagebyte. I denna övning simulerar den en version; den bygger ingen ny image.
Spara dina avsedda ändringar i egen YAML och låt inte den ursprungliga startfilen
skriva över dem av misstag.

## Vanliga fel och vad de betyder

`undo` återställer fel revision: välj uttryckligen `--to-revision=N` efter inspektion.
Utrullning klar men fel konfiguration: kontrollera externa ConfigMaps och miljövärden.
