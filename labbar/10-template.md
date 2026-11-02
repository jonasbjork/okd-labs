# 10. Skapa applikationer med Template

**Nivå:** Medel · **Tid:** 35–45 min · **Förkunskaper:** Labb 07

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

En OpenShift Template innehåller parametrar och objekt som kan bearbetas till
vanliga API-resurser. Bearbetning och skapande är två olika steg. En ändrad Template
uppdaterar inte automatiskt redan skapade Deployments.

## Uppgift

1. Skapa kod-ConfigMap enligt appstarten, men applicera inte app-deployment.yaml.
2. Läs `assets/template.yaml`. Lista parametrarna med CLI.
3. Bearbeta mallen lokalt med `NAME=demo` och `MESSAGE=Skapad från mall`.
4. Spara resultatet i `.work/template-result.yaml`, läs det och skapa resurserna.
5. Visa att Deploymentens selector, Pod-label och Service-selector stämmer överens.
6. Skapa en andra instans `demo2` med en annan hälsning i samma projekt.
7. Kontrollera båda instanserna utan att de kopplas till varandras Pods.

## Verifiera slutresultatet

```sh
oc get deployment demo demo2
oc get service demo demo2
oc get pods --show-labels
oc get endpointslices -l kubernetes.io/service-name=demo -o yaml
```

Port-forward respektive Service på olika lokala portar. Svaret ska innehålla rätt
hälsning för respektive instans. Resultatfilen ska innehålla färdiga resurser.

## Ledtrådar

`oc process --local -f assets/template.yaml --parameters`.
Namnet används i flera fält; ändra parametern i stället för ett enstaka objekt.

## Förklara med egna ord

- Varför räcker det inte att bara skapa Template-objektet?
- Hur kan två instanser använda samma kod-ConfigMap men olika inställningar?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/10-template.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment demo demo2 --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete service demo demo2 --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code --ignore-not-found
```
