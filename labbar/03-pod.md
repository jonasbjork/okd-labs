# 03. En Pod från kommando till YAML

**Nivå:** Grund · **Tid:** 35–45 min · **Förkunskaper:** Labb 01–02

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

Pod är Kubernetes minsta schemaläggningsenhet. En fristående Pod har ingen Deployment
som återskapar den när Pod-objektet tas bort. `restartPolicy` gäller omstart av
containrar inom Poden, inte återställning av ett raderat Pod-objekt.

## Uppgift

1. Skapa Pod `first` med Python-imagen och en HTTP-server på port 8080.
2. Undersök Podens tillstånd, IP, nod, containerstatus, loggar och events.
3. Använd port-forward och hämta startsidan.
4. Generera ett Pod-manifest med `--dry-run=client -o yaml` och spara i `.work/pod.yaml`.
5. Byt namnet i manifestet till `second`, tillämpa det och kontrollera Poden.
6. Ta bort `first`. Visa att ingen ersättare skapas. Behåll `second` tills du är klar.

## Verifiera slutresultatet

```sh
oc get pods -o wide
oc describe pod second
oc logs second
oc get events --sort-by=.metadata.creationTimestamp
```

`second` ska vara Running och Ready. Efter radering ska `first` förbli borta.
Visa med ett HTTP-anrop att servern svarar, inte bara att processen kör.

## Ledtrådar

`oc run ... --command -- python -m http.server ...` skiljer körkommando från argument.
Om SCC kräver extra säkerhetsfält, använd containerfält från `assets/basic-deployment.yaml`
i Podens `spec.containers`, inte en privilegierad SCC.

## Förklara med egna ord

- Vilket fält visar noden och vilket visar Podens IP?
- Varför återkommer inte en raderad fristående Pod?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/03-pod.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete pod first second --ignore-not-found
```
