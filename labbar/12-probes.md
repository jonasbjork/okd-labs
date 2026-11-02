# 12. Readiness, liveness och startup

**Nivå:** Medel+ · **Tid:** 50–60 min · **Förkunskaper:** Labb 05, 11

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

Readiness styr om en Pod normalt ska ta emot Service-trafik. Liveness kan starta
om containern. Startup-proben skjuter upp de två andra kontrollerna tills uppstarten
lyckats. En process kan vara Running men samtidigt inte Ready.

## Uppgift

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py --dry-run=client -o yaml | oc apply -f -
oc apply -f assets/app-deployment.yaml
oc apply -f assets/service.yaml
oc rollout status deployment/web --timeout=180s
```

1. Lägg till HTTP readiness mot `/ready`, liveness mot `/live` och startup mot `/live`.
   Använd port 8080, period 5 sekunder och timeout 2 sekunder. Sätt failureThreshold
   till 1, 3 respektive 30.
2. Vänta på utrullning och välj dess enda Pod. Notera UID och restartCount.
3. Skapa `/tmp/not-ready` i Poden. Följ Ready och Service-endpoints.
4. Verifiera att appen fortfarande svarar via direkt Pod-port-forward men inte är
   en redo backend för Service. Ta bort flaggan och invänta Ready.
5. Skapa `/tmp/fail-live`. Observera en containeromstart och kontrollera UID samt restartCount.
6. Förklara varför flaggan försvinner i det här fallet.

## Verifiera slutresultatet

```sh
oc get pods -l app=web
oc get endpointslices -l kubernetes.io/service-name=web -o yaml
```

Readiness-felet ska inte i sig öka restartCount. Liveness-felet ska öka den, medan
Podens UID är samma. Slutläget ska vara Ready och Service-trafik ska fungera.

## Ledtrådar

Markörerna ligger i containerns skrivbara lager, inte i en volym. Välj Pod efter
färdig utrullning. `oc port-forward pod/NAMN` testar processen utan Service-urval.

## Förklara med egna ord

- Varför är databasåtkomst ofta ett dåligt villkor för liveness?
- När behöver en långsam uppstart en startup-probe?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/12-probes.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete service web --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code --ignore-not-found
```
