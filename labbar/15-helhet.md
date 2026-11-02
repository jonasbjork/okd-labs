# 15. Bygg en sammanhängande applikation

**Nivå:** Avancerad · **Tid:** 75–100 min · **Förkunskaper:** Labb 01–14

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

Du kombinerar nu två Deployments med olika ansvar. Frontend får extern trafik,
backend har beständig data och en enda skrivare. Intern Service-DNS kopplar ihop dem.
En fungerande kedja behöver korrekta selectors, portar, konfiguration och readiness
på varje del. Backend får ingen extern Route.

## Uppgift

Skapa egna manifest i `.work/15/`. `lab-code` från `assets/server.py` får användas färdig.

1. Skapa ConfigMap `site-config`: `MESSAGE=Välkommen till min portal`,
   `BACKEND_MESSAGE=Backend är redo`, `BACKEND_URL=http://backend/`.
2. Skapa Deployment och Service `web`. Tillför MESSAGE och BACKEND_URL från ConfigMap.
3. Skapa Deployment och Service `backend`. Tillför MESSAGE från BACKEND_MESSAGE.
4. Båda kör övningsappen på 8080. Services använder port 80, targetPort http.
5. Backend ska ha en replik, Recreate-strategi, PVC `web-data` på `/data` och
   Secret `web-secret` med token `training-token-v1` på `/etc/lab-secret`.
6. Båda ska ha requests 100m/64Mi, limits 250m/128Mi och readiness/liveness/startup
   enligt labb 12. Frontend ska börja med två repliker.
7. Skapa edge-Route `web` till frontend med HTTP→HTTPS-omdirigering.
8. Testa frontend `/` och `/backend` externt. Spara `integration-marker` i backend via
   dess Service och autentiserad POST. Radera backend-Poden och verifiera beständighet.
9. Radera en frontend-Pod och visa att tjänsten återhämtar sig utan manuella reparationer.
10. Kontrollera samma resurser i webbgränssnittet.

## Verifiera slutresultatet

Slutläget ska ha två frontend-Pods och en backend-Pod som är Ready. Endast frontend
ska ha en Route. `/backend` ska innehålla backendens hälsning. `/state` på backend ska
bevara markören efter Pod-byte. Bevisa även att fel token ger 403.

## Ledtrådar

Utgå från app-deployment.yaml och service.yaml. När du kopierar till backend måste
metadata.name, Deployment-selector, Pod-label och Service-selector ändras tillsammans.
`oc diff -f ...` kan visa skillnaden före en uppdatering.

## Förklara med egna ord

- Varför kan frontend skalas medan just denna backend behålls som en replik?
- Vilka fel skulle kunna orsaka 502 från `/backend`?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/15-helhet.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web backend --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete route web --ignore-not-found
oc -n "$LAB_PROJECT" delete service web backend --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code site-config --ignore-not-found
oc -n "$LAB_PROJECT" delete secret web-secret --ignore-not-found
oc -n "$LAB_PROJECT" delete pvc web-data --ignore-not-found
```

Detta tar bort övningens PVC och dess lagrade data kan försvinna. Gör beständighetstestet före städning.
