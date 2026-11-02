# 14. Autoskalning med kontrollerad belastning

**Nivå:** Avancerad · **Tid:** 50–60 min · **Förkunskaper:** Labb 12–13 och resource metrics

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

En HPA justerar önskat replikantal från observerade mätvärden. CPU-utilization är
relativ till CPU-request, inte limit. Här innebär 50 procent av 100m ett mål kring
50m per Pod. Metrics behöver tid att visas; stabilisering dämpar snabb nedskalning.

## Uppgift

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py --dry-run=client -o yaml | oc apply -f -
oc apply -f assets/app-deployment.yaml
oc apply -f assets/service.yaml
oc rollout status deployment/web --timeout=180s
```

1. Sätt samma requests/limits som i labb 13 och HTTP readiness mot `/ready`.
2. Kontrollera att `oc adm top pods` får mätvärden efter uppstart.
3. Skapa HPA `web`, CPU-mål 50 procent, min 1/max 3 och nedskalningsfönster 60 sekunder.
4. Starta den medföljande last-Jobben. Den kör högst fem minuter och begränsar sin egen CPU.
5. Följ HPA, Pods och mätvärden. Bekräfta uppskalning över en replik.
6. Ta bort last-Jobben, vänta på stabilisering och observera nedskalning.
7. Dokumentera tidsförlopp och HPA conditions. Sätt inte repliker manuellt medan HPA arbetar.

## Verifiera slutresultatet

```sh
oc get hpa web
oc describe hpa web
oc adm top pods
```

Mätvärdet ska inte förbli `<unknown>`. Under last ska fler än en replik bli Ready,
högst tre. Efter avslutad last och stabilisering ska antalet kunna återgå till en.
Det kan ta flera minuter utöver fönstret på grund av mätning och controllercykler.

## Ledtrådar

`assets/hpa.yaml`, `assets/load-job.yaml` och `assets/load.py` är startmaterial.
Lasten går direkt mot Service, så extern ingress behövs inte.

## Förklara med egna ord

- Vad händer med procenttalet om CPU-request fördubblas för samma faktiska användning?
- Varför är `<unknown>` något annat än noll procents belastning?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/14-hpa.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete hpa web --ignore-not-found
oc -n "$LAB_PROJECT" delete job load --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete service web --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code load-code --ignore-not-found
```
