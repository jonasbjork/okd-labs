# 11. Utrullning och återställning

**Nivå:** Medel · **Tid:** 40–50 min · **Förkunskaper:** Labb 04, 07

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

En Deployment-revision skapas när Pod-mallen ändras. En utrullning behöver både
nya Pods och tillgänglighet enligt strategin. `rollout undo` återställer Pod-mallen;
externa ConfigMaps, Secrets och PVC-data återställs inte av det kommandot.

## Uppgift

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py --dry-run=client -o yaml | oc apply -f -
oc apply -f assets/app-deployment.yaml
oc apply -f assets/service.yaml
oc rollout status deployment/web --timeout=180s
```

1. Sätt två repliker och vänta på färdig utrullning.
2. Sätt `APP_VERSION=v2`. Följ ReplicaSets och utrullningsstatus.
3. Kontrollera att HTTP-svaret visar v2.
4. Byt image till den avsiktligt felaktiga referensen
   `docker.io/library/python:ex180-does-not-exist`. Undersök vad som händer.
5. Samla events och status som förklarar varför utrullningen inte blir klar.
6. Återställ föregående fungerande Pod-mall. Bekräfta två fungerande repliker med v2.
7. Spara en egen fungerande manifestversion så att nästa `apply` inte återinför fel.

## Verifiera slutresultatet

```sh
oc rollout history deployment/web
oc get deployment web
oc get replicasets
oc get pods -l app=web
```

Sista utrullningen ska vara klar med två tillgängliga repliker och rätt image.
Fel-Pods från tidigare ReplicaSet ska vara nedskalade. HTTP-svar ska visa v2.

## Ledtrådar

`oc rollout status ... --timeout=60s` får avsiktligt misslyckas i felsteget.
Kör inte återställning förrän du förstått felet. Inspektera även gamla ReplicaSets.

## Förklara med egna ord

- Varför kan gamla Pods fortsätta svara under en misslyckad utrullning?
- Vad behöver versionshanteras utöver Deploymentens revisioner?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/11-rollout.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete service web --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code --ignore-not-found
```
