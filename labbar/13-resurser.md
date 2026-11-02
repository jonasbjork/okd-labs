# 13. Requests, limits och ett minnesfel

**Nivå:** Medel+ · **Tid:** 45–60 min · **Förkunskaper:** Labb 04, 12

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

Requests används för schemaläggning och resursfördelning. En CPU-limit begränsar
CPU-tid genom throttling; en minneslimit kan leda till OOMKill. En Pending Pod är
inte samma feltyp som en körande container som startas om efter minnesbrist.

## Uppgift

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py --dry-run=client -o yaml | oc apply -f -
oc apply -f assets/app-deployment.yaml
oc apply -f assets/service.yaml
oc rollout status deployment/web --timeout=180s
```

1. Sätt requests `cpu=100m,memory=64Mi` och limits `cpu=250m,memory=128Mi` för `web`.
2. Kontrollera resurserna i Pod-specifikationen och QoS-klassen.
3. Skapa en fristående Pod `memory-test` som håller mer än 32 MiB allokerat men har
   minneslimit 32 MiB och restartPolicy Never. Använd lösningens manifest först om du behöver hjälp.
4. Observera termination reason och exitkod. Skilj OOMKilled från andra fel.
5. Ta bort test-Poden. Skapa en tillfällig `schedule-test` med cpu request och limit
   100000 (CPU-kärnor), minne 32 MiB/64 MiB och kommandot `sleep 300`.
6. Undersök schemaläggningsfelet och ta bort test-Poden direkt efter observationen.
   Om ResourceQuota/LimitRange nekar skapandet, dokumentera det utfallet i stället.

## Verifiera slutresultatet

`web` ska vara Ready med begärda resurser. `memory-test` ska visa OOMKilled i
terminerad containerstatus (vanligen exit 137). `schedule-test` ska visa Insufficient cpu
om den antagits av API. Inga test-Pods ska finnas kvar i slutläget.

## Ledtrådar

`oc set resources deployment/web ...`, `oc describe pod ...` och
`status.containerStatuses[].state.terminated`. 100m är en tiondels CPU-kärna.

## Förklara med egna ord

- Varför kan en liten request och stor minnesanvändning vara problematisk på en full nod?
- Hur skiljer du admission-avslag, Pending och OOMKilled åt?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/13-resurser.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete deployment web --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete pod memory-test schedule-test --ignore-not-found
oc -n "$LAB_PROJECT" delete service web --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code --ignore-not-found
```
