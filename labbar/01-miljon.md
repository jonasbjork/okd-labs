# 01. CLI, projekt och webbgränssnitt

**Nivå:** Grund · **Tid:** 30–45 min · **Förkunskaper:** Grundläggande terminalvana

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

Ditt tilldelade projekt avgränsar dina applikationsresurser och rättigheter. `oc` har ett aktuellt
kluster, en användare och ett namespace i sin kontext. Webbgränssnittet och CLI
visar samma API-resurser; en vald projektvy påverkar vad du ser.

Att skilja klientversion från serverversion hjälper dig använda rätt dokumentation.

## Uppgift

1. Installera `oc` enligt förberedelserna och kontrollera versionen.
2. Logga in och välj ditt tilldelade projekt enligt ovan. Visa användare, API-adress och aktivt projekt.
3. Lista Pods, Deployments, Services, Routes, ConfigMaps, Secrets och PVC:er separat.
4. Öppna webbgränssnittet, välj projektet och hitta dess resursvyer. Menynamn kan variera.
5. Skapa ConfigMap `orientation` med nyckeln `course=ex180`. Hitta samma objekt i webbgränssnittet.
6. Ändra värdet till `okd-4.22` i webbgränssnittets YAML-editor och läs tillbaka det med CLI.
7. Läs hjälpen för `oc get` och fältbeskrivningen för `pod.spec.containers`.

## Verifiera slutresultatet

```sh
oc whoami
oc whoami --show-server
oc project
oc get configmap orientation -o jsonpath='{.data.course}{"\n"}'
```

Sista kommandot ska ge `okd-4.22`. Anteckna klient- och serverversion och var i webb-
gränssnittet du hittade objektet. Tomma listor är normala i ett nytt projekt.

## Ledtrådar

`oc get all` visar inte alla resurskategorier. Använd uttryckliga typer.
`oc explain pod.spec.containers` ger fälthjälp.

## Förklara med egna ord

- Hur märker du att du är i fel projekt?
- Varför är en tom Pod-lista inte ett klusterfel?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/01-miljon.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete configmap orientation --ignore-not-found
```
