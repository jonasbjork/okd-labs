# 06. Route, HTTP och TLS

**Nivå:** Medel · **Tid:** 40–50 min · **Förkunskaper:** Labb 05 och fungerande ingress

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

En Route kopplar ett externt värdnamn till en Service via ingressroutern.
Vid edge-terminering avslutas TLS vid routern och trafiken till appen är HTTP.
Certifikatet måste vara giltigt för Route-värdnamnet och betrott av klienten.

## Uppgift

```sh
oc apply -f assets/basic-deployment.yaml
oc rollout status deployment/web --timeout=180s
```

```sh
oc apply -f assets/service.yaml
```

1. Exponera Service `web` med en HTTP-Route `web`.
2. Hämta värdnamnet från API och verifiera åtkomst från din dator.
3. Skapa edge-Route `web-tls` med samma Service, port `http` och HTTP→HTTPS-omdirigering.
   Låt ingressens standardcertifikat användas.
4. Verifiera HTTPS och omdirigering separat.
5. Rita eller beskriv flödet klient → ingress → Route/Service → Pod.

## Verifiera slutresultatet

```sh
oc get routes
oc get route web-tls -o yaml
```

HTTP-Route ska svara. TLS-Routen ska ha `termination: edge`,
`insecureEdgeTerminationPolicy: Redirect` och vara admitted. HTTPS ska ge 200;
HTTP till TLS-värdnamnet ska ge omdirigering med Location till HTTPS.

## Ledtrådar

`oc expose service web`, `oc create route edge --help`.
Om ingress använder egen CA, be administratören om CA-filen och använd
`curl --cacert /sokvag/ca.pem`. Ett certifikatfel ska inte döljas som lyckad TLS-verifiering.

## Förklara med egna ord

- Var finns TLS-certifikatet vid edge-terminering?
- Vilken del skulle du undersöka om intern HTTP fungerar men Route inte gör det?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/06-route.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete route web web-tls --ignore-not-found
oc -n "$LAB_PROJECT" delete service web --ignore-not-found
```
