# 08. Secret som miljö och fil

**Nivå:** Medel · **Tid:** 40–50 min · **Förkunskaper:** Labb 07

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

Secret är en separat resurstyp för känsliga värden och kan begränsas med behörigheter.
Base64 i YAML är kodning, inte kryptering. Åtkomstkontroll och klustrets kryptering i vila
är separata frågor. Använd endast de fiktiva kursvärdena här.

## Uppgift

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py --dry-run=client -o yaml | oc apply -f -
oc apply -f assets/app-deployment.yaml
oc apply -f assets/service.yaml
oc rollout status deployment/web --timeout=180s
```

1. Skapa Secret `web-secret` med nyckeln `token=training-token-v1`.
2. Tillför nyckeln som miljövariabeln `LAB_TOKEN` med en `secretKeyRef`.
3. Kontrollera att `/` ger `secret_loaded: true`, utan att token visas.
4. Ta bort miljövariabeln och montera i stället Secret skrivskyddat på `/etc/lab-secret`.
5. Kontrollera funktionen och byt tokenvärde i Secret till `training-token-v2`.
6. Undersök volymreferensen utan att skriva ut värdet i din rapport.
7. Förklara hur du skulle kontrollera att en arbetslast får läsa rätt Secret.

## Verifiera slutresultatet

```sh
oc describe secret web-secret
oc get deployment web -o yaml
```

Slutläget ska ha en Secret-volym men ingen `LAB_TOKEN`-miljövariabel.
Appens `/` ska ge `secret_loaded: true`. I labb 09 provar du att rätt token faktiskt
krävs vid skrivning; här kontrollerar du hur värdet tillförs.

## Ledtrådar

Använd `oc set env deployment/web LAB_TOKEN-` för att ta bort miljövariabeln.
En `secretKeyRef` kan läggas in med `oc edit deployment web` eller i en egen manifestfil.

## Förklara med egna ord

- Vad kan en användare som får läsa Secret-objektet göra med base64-värdet?
- Varför kan en användare som får skapa Pods också få indirekt åtkomst till ett Secret?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/08-secret.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete service web --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code --ignore-not-found
oc -n "$LAB_PROJECT" delete secret web-secret --ignore-not-found
```
