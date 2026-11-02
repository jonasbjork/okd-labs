# 17. Samla diagnostik och klusterunderlag

**Nivå:** Avancerad · **Tid:** 40–60 min · **Förkunskaper:** Labb 03, 16

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

Applikationsdiagnostik inom ett projekt och klusterinsamling har olika omfattning.
Loggar visar processen, events visar plattformshändelser och manifest visar deklarerat
tillstånd. Must-gather samlar ett bredare underlag som administratören kan analysera.
Här övar vi insamling lokalt utan att ladda upp något.

## Uppgift

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py --dry-run=client -o yaml | oc apply -f -
oc apply -f assets/app-deployment.yaml
oc apply -f assets/service.yaml
oc rollout status deployment/web --timeout=180s
```

**Del A – projektbehörighet**

1. Skapa en kort diagnostikrapport med tid, projekt, resursstatus, events och apploggar.
2. Visa även Podens containerstatus och Deploymentens conditions.
3. Öppna Podens loggar och events i webbgränssnittet och jämför.
4. Spara underlaget under `.work/diagnostik-17/`, utan Secret-värden eller kubeconfig.

**Del B – analysera lärarens klusterunderlag**

5. Läraren demonstrerar must-gather och ger dig ett granskat, avgränsat utdrag med
   exempel på resursdefinitioner och loggar. Du använder ditt vanliga elevkonto hela tiden.
6. Identifiera projekt, resursnamn, tidsstämplar och ett symptom i utdraget.
7. Jämför med projektinsamlingen i del A. Vilken ytterligare information behövdes?
8. Skriv vad du själv kan undersöka i projektet och vilken fråga du behöver lämna till läraren.

Om utdrag saknas genomför du del A och markerar del B som ej genomförd.
Insamling av klusterunderlag är ett EX180-mål, men elevkontot kan här bara träna analysen.
Själva insamlingskommandot demonstreras av läraren enligt
[lärarhandledningen](../docs/lararhandledning.md).

## Verifiera slutresultatet

Underlaget ska innehålla läsbara resursdefinitioner, events och loggar från del A.
I del B ska du kunna förklara innehållet i lärarens utdrag och behovet av eskalering.
Detta verifierar analysen, inte att du själv har kört klusterinsamlingen.
Ingen uppladdning eller supportärende ingår.

## Ledtrådar

Läs [OKD:s insamlingsinstruktion](https://docs.okd.io/4.22/support/gathering-cluster-data.html).
Skilj mellan uppgifter du får läsa i ditt projekt och underlag som läraren samlar från klustret.

## Förklara med egna ord

- När räcker applikationsloggar inte för att hitta orsaken?
- Varför ska insamlingsunderlag granskas innan det delas?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/17-diagnostik.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete service web --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code --ignore-not-found
```
