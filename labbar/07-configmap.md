# 07. Konfiguration med ConfigMap

**Nivå:** Medel · **Tid:** 45–60 min · **Förkunskaper:** Labb 04–06

Läs [förberedelserna](../docs/forberedelser.md) först. Kör från repots rot.
Använd användaren och projektet som läraren tilldelat dig. Sätt `LAB_PROJECT` enligt
[förberedelserna](../docs/forberedelser.md) och kontrollera projektvalet:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc project "$LAB_PROJECT"
oc whoami
```

Gör klart och städa föregående labb innan du börjar. Samma resursnamn återanvänds;
kör en labb åt gången i projektet.

## Varför och hur det fungerar

ConfigMap skiljer inställningar från image och Pod-mall. Miljövariabler kopieras
vid containerstart. Monterade ConfigMap-filer kan uppdateras efter en fördröjning,
men applikationen måste läsa om dem. En fil monterad med `subPath` får inte dessa
löpande volymuppdateringar.

## Uppgift

Starta övningsappen enligt appstarten:

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py --dry-run=client -o yaml | oc apply -f -
oc apply -f assets/app-deployment.yaml
oc apply -f assets/service.yaml
oc rollout status deployment/web --timeout=180s
```

1. Skapa ConfigMap `web-config` med `MESSAGE=Hej från ConfigMap` och `message=Filversion 1`.
2. Låt `MESSAGE` komma från ConfigMap som miljövariabel.
3. Montera hela ConfigMap-volymen skrivskyddat på `/etc/lab-config`, utan `subPath`.
4. Anropa `/` och observera `message` och `file_message`.
5. Ändra båda värdena till version 2. Anropa igen tills filvärdet uppdaterats.
6. Starta om Deploymentens Pods kontrollerat och observera miljövärdet.

## Verifiera slutresultatet

Svaret ska först visa båda version 1-värdena. Före omstart ska filvärdet kunna bli
version 2 medan miljövärdet är kvar. Efter omstart ska båda visa version 2.
Använd port-forward enligt förberedelserna och starta om tunneln efter Pod-byte.

## Ledtrådar

`oc set env deployment/web --from=configmap/web-config --keys=MESSAGE`.
`oc set volume --help` har stöd för ConfigMap-volymer och mount-path.

## Förklara med egna ord

- Varför räcker det inte alltid att ändra en ConfigMap?
- Vad skiljer programkodens `lab-code` från inställningarnas `web-config` i den här labben?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/07-configmap.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete service web --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code web-config --ignore-not-found
```
