# 05. Service, selectors och intern DNS

**Nivå:** Grund+ · **Tid:** 40–50 min · **Förkunskaper:** Labb 04

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

En Service ger ett stabilt namn till en föränderlig grupp Pods. Selector väljer
Pods via labels. Service-porten är klientens port; targetPort är mottagarens port.
EndpointSlices beskriver de valda adresserna och deras readiness.

## Uppgift

Starta grundservern:

```sh
oc apply -f assets/basic-deployment.yaml
oc rollout status deployment/web --timeout=180s
```

1. Skapa en Service `web` med port 80 till Podens namngivna port `http` (8080).
2. Starta en tillfällig klient-Pod och nå `http://web` inifrån projektet.
3. Visa Service och dess EndpointSlices.
4. Ändra Service-selector till `app=missing`. Förklara och verifiera felet.
5. Återställ selector, skala Deploymenten till två och kontrollera de två endpoint-adresserna.
6. Kontrollera DNS-namnet `web.PROJEKT.svc.cluster.local` från klienten.

## Verifiera slutresultatet

```sh
oc get service web -o yaml
oc get endpointslices -l kubernetes.io/service-name=web -o yaml
```

HTTP ska fungera inifrån projektet. Selector ska vara `app: web` och två Pods ska
vara redo. Vid fel selector ska Service finnas kvar men sakna valda fungerande endpoints.

## Ledtrådar

Kopiera inte Pod-IP till Service-selector. Använd `assets/service.yaml` vid behov.
Klientkommandot i lösningen använder Python, så `curl` behövs inte i imagen.

## Förklara med egna ord

- Varför kan DNS-uppslag fungera samtidigt som HTTP misslyckas?
- Vad händer om `targetPort` pekar på fel port?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/05-service.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete pod client --ignore-not-found
oc -n "$LAB_PROJECT" delete service web --ignore-not-found
```
