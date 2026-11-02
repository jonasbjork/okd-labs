# Lösningsförslag 07: Konfiguration med ConfigMap

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/07-configmap.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc create configmap web-config --from-literal='MESSAGE=Hej från ConfigMap' --from-literal='message=Filversion 1'
oc set env deployment/web --from=configmap/web-config --keys=MESSAGE
oc set volume deployment/web --add --name=config --type=configmap --configmap-name=web-config --mount-path=/etc/lab-config --read-only=true
oc rollout status deployment/web --timeout=180s
```

Kör port-forward och anropa `/`. Ändra därefter:

```sh
oc patch configmap web-config --type=merge -p '{"data":{"MESSAGE":"Hej version 2","message":"Filversion 2"}}'
```

Kontrollera återkommande HTTP-svar. Filuppdatering är asynkron; vänta några minuter
innan du felsöker volymen. Gör sedan:

```sh
oc rollout restart deployment/web
oc rollout status deployment/web --timeout=180s
```

Starta om port-forward och verifiera igen. `rollout restart` ändrar Pod-mallen med
en tidsstämpel så att nya processer får den aktuella miljön.

## Vanliga fel och vad de betyder

`CreateContainerConfigError`: finns ConfigMap och nyckeln MESSAGE i rätt projekt?
Tomt filvärde: kontrollera nyckeln `message`, monteringsvägen och skillnaden på gemener/versaler.
