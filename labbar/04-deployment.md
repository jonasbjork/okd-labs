# 04. Deployment, repliker och självläkning

**Nivå:** Grund · **Tid:** 35–45 min · **Förkunskaper:** Labb 03

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

Deployment beskriver önskad Pod-mall och antal repliker. Den hanterar ReplicaSets,
som i sin tur håller rätt antal Pods. Ändringar i Pod-mallen ger en ny revision.
Att ändra repliker ändrar antalet instanser, inte applikationsversionen.

## Uppgift

1. Läs `assets/basic-deployment.yaml` och applicera filen.
2. Visa Deployment, ReplicaSet och Pods samt deras ownerReferences.
3. Skala `web` till tre repliker och vänta tills alla är tillgängliga.
4. Anteckna namnet på en Pod, radera just den och följ hur en ersättare skapas.
5. Skala tillbaka till en replik.
6. Inspektera samma Deployment och dess Pod-mall i webbgränssnittet.

## Verifiera slutresultatet

```sh
oc get deployment,replicaset,pods -l app=web
oc get deployment web -o jsonpath='{.spec.replicas}{" "}{.status.availableReplicas}{"\n"}'
```

Slutläget ska vara `1 1`. Deployment saknar i startfilen en egen `app`-label;
lista därför även `oc get deployment web`. Bevisa att den raderade Podens UID
skiljer sig från ersättarens.

## Ledtrådar

Labels på Deployment och labels i `spec.template.metadata` är skilda saker.
Läs `oc get pod NAMN -o yaml` för ägarreferensen.

## Förklara med egna ord

- Vilken controller skapar ersättnings-Poden?
- Varför är Pod-namn olämpliga som beständig applikationsadress?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/04-deployment.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
```
