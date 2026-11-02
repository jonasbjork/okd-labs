# 09. PVC och data efter Pod-byte

**Nivå:** Medel · **Tid:** 50–60 min · **Förkunskaper:** Labb 08 och dynamisk lagring

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

En PVC begär lagring; en PV representerar tilldelad lagring. StorageClass styr
provisioneringen. `ReadWriteOnce` betyder skrivbar montering på en nod, inte
nödvändigtvis en enda Pod. En enskild skrivare med Recreate-strategi gör detta
övningsfall enklare att förstå.

## Uppgift

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py --dry-run=client -o yaml | oc apply -f -
oc apply -f assets/app-deployment.yaml
oc apply -f assets/service.yaml
oc rollout status deployment/web --timeout=180s
```

1. Skapa Secret `web-secret` med `token=training-token-v1` och montera på `/etc/lab-secret`.
2. Skapa PVC `web-data`, 1 GiB, ReadWriteOnce. Använd default StorageClass eller
   ange din fungerande klass i en egen kopia av `assets/pvc.yaml`.
3. Sätt Deploymentens strategi till `Recreate` och behåll en replik.
4. Montera PVC på `/data`.
5. Spara texten `Min beständiga anteckning` med `POST /state` och korrekt token.
   Visa att fel token nekas.
6. Läs tillbaka texten, anteckna Podens UID och radera Poden.
7. Vänta på ersättaren och läs tillbaka samma text utan att skapa om den.

## Verifiera slutresultatet

```sh
oc get pvc web-data
oc get deployment web -o jsonpath='{.spec.strategy.type}{"\n"}'
```

PVC ska bli Bound när en konsument finns. Skrivningen ska ge 200 med korrekt token,
403 med fel token. `GET /state` ska ge samma text före och efter Pod-byte, medan UID ändras.

## Ledtrådar

`WaitForFirstConsumer` kan hålla en PVC Pending tills en Pod använder den.
Byt strategi och montera lagringen innan du väntar på färdig utrullning.

## Förklara med egna ord

- Vad skulle hända med data i containerns egen `/tmp` vid Pod-byte?
- Varför är detta inte en lämplig modell för tre samtidiga skrivande repliker?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/09-pvc.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete service web --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code --ignore-not-found
oc -n "$LAB_PROJECT" delete secret web-secret --ignore-not-found
oc -n "$LAB_PROJECT" delete pvc web-data --ignore-not-found
```

Detta tar bort övningens PVC och dess lagrade data kan försvinna. Gör beständighetstestet före städning.
