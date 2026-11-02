# 16. Felsökningsverkstad med förberedda fel

**Nivå:** Avancerad · **Tid:** 60–90 min · **Förkunskaper:** Labb 01–15

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

Felsök från observation till hypotes, kontroll och minsta motiverade ändring.
Skilj API-konfiguration från körande process, readiness och trafikväg. Gör en ändring
åt gången och bevisa sedan effekten. Att radera allt tar bort viktiga ledtrådar.

## Uppgift

Starta övningsappen och en HTTP-Route, samt readiness-probe mot `/ready`.

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py --dry-run=client -o yaml | oc apply -f -
oc apply -f assets/app-deployment.yaml
oc apply -f assets/service.yaml
oc rollout status deployment/web --timeout=180s
```

```sh
oc expose service web --port=http
oc set probe deployment/web --readiness --get-url=http://:8080/ready --period-seconds=5
oc rollout status deployment/web --timeout=180s
```

Be gärna en övningspartner applicera en fel-fil åt gången utan att berätta vilken.
Filerna i `assets/fel/` är avsiktligt felaktiga och ska bara användas i detta projekt.
Om du övar ensam: välj en fil och felsök utan att läsa lösningen direkt.

För varje fall:

1. Applicera en av `assets/fel/01.yaml` till `05.yaml`.
2. Dokumentera symptom och minst två observationer som avgränsar felet.
3. Åtgärda grundorsaken, inte bara symptomet. Verifiera HTTP och Ready.
4. Återställ baslinjen med kommandona nedan innan nästa fall.

```sh
oc apply -f assets/app-deployment.yaml
oc apply -f assets/service.yaml
oc set probe deployment/web --readiness --get-url=http://:8080/ready --period-seconds=5
oc rollout status deployment/web --timeout=180s
oc -n "$LAB_PROJECT" delete configmap missing-config --ignore-not-found
```

Använd `oc apply -f assets/fel/01.yaml` som exempel på hur ett fall startas.
Baslinjen kan återställa Deploymentens kända fält; kontrollera specifikt readiness
med kommandot ovan eftersom `oc set` och `apply` kan förvalta olika fält.

## Verifiera slutresultatet

Efter varje reparation: Deployment ska rulla klart, Pod vara Ready och nytt HTTP-anrop
via Route ge 200. Rapportera per fall: symptom → bevis → orsak → ändring → verifiering.
Målet är att kunna förklara varför just din åtgärd var rimlig.

## Ledtrådar

Börja med `oc get`, fortsätt med `oc describe`, events och `oc logs`.
Använd sedan Service/EndpointSlice och till sist extern Route. Jämför önskat och faktiskt tillstånd.

## Förklara med egna ord

- Vilket fall gav en Running Pod som ändå inte fungerade genom Service?
- Vilken observation uteslöt ett DNS-problem?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/16-felsokning.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete route web --ignore-not-found
oc -n "$LAB_PROJECT" delete service web --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code missing-config --ignore-not-found
```
