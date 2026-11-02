# 18. Praktiskt träningsprov

**Nivå:** Självständig · **Tid:** 120 min · **Förkunskaper:** Labb 01–17

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

Du får nu slutkrav och ett applikationskontrakt. Välj själv ordning, kommandon och
manifest. Använd officiell dokumentation och CLI-hjälp. Vänta med lösningsförslaget
för att mäta vad du kan utföra och verifiera själv.

## Uppgift

Starta en timer på 120 minuter. Använd den medföljande serverkoden utan att ändra dess API.
Förslag på tidsbudget: inspektion/Pod 15 min, mall och appkedja 50 min, tillförlitlighet
20 min, HPA 15 min, verifiering och rapport 20 min.

**Krav**

1. Dokumentera användare, projekt, serverversion och image-metadata för Python-imagen.
2. Skapa en fristående Pod `inspector` med samma image och kommandot `sleep 3600`.
   Verifiera dess UID och visa loggkommandot även om loggen är tom.
3. Bearbeta `assets/template.yaml` lokalt med NAME=web och MESSAGE=Prov klart.
   Spara det renderade resultatet och skapa applikationen från det. Kod-ConfigMap får levereras separat.
4. Bygg vidare till frontend `web` och backend `backend` med Services port 80→8080.
5. ConfigMap `site-config` ska styra frontends hälsning `Prov klart`,
   backendhälsning `Lagring redo` och BACKEND_URL=http://backend/.
6. Secret `web-secret` ska innehålla den fiktiva token `training-token-v1` och monteras
   som fil endast i backend. Ingen token får visas i HTTP-svaret.
7. Backend ska ha PVC `web-data` på 1 GiB, en replik och Recreate. Spara texten
   `exam-marker` genom autentiserad POST; bevisa 403 med fel token och bevarad text efter Pod-byte.
8. Ge endast frontend extern åtkomst med edge-Route och HTTP→HTTPS-omdirigering.
9. Båda Deployments ska ha de tre hälsokontrollerna enligt labb 12 samt requests
   100m/64Mi och limits 250m/128Mi.
10. Frontend ska ha HPA min 1/max 3, mål 50 procent CPU. Visa uppskalning med last-Jobben
    och stoppa sedan lasten. Backend ska inte ha HPA.
11. Samla projektets resursstatus, events och loggar i `.work/prov-18/`.
12. Gör en egen ändring som tillfälligt bryter frontend-Service-selector. Diagnostisera
    felet, spara bevis och reparera det. Kontrollera resurserna även i webbgränssnittet.

Lärardemonstrationen av klusterinsamling från labb 17 och lokal containerkörning
från labb 02 bedöms här inte på nytt. Elevkontot kan inte själv träna klusterinsamlingen;
se måltäckningens avgränsning i examensmålsdokumentet.

## Verifiera slutresultatet

| Kontroll | Poäng |
| --- | ---: |
| Rätt kontext, imageinspektion och fristående Pod | 10 |
| Renderad Template och fungerande frontend/backend via Services | 20 |
| ConfigMap och Secret rätt refererade, ingen token i HTTP | 15 |
| PVC, korrekt/nekad skrivning och beständighet efter Pod-byte | 15 |
| Fungerande HTTPS-Route och omdirigering | 10 |
| Tre probes och rätt requests/limits på båda | 10 |
| HPA med mätvärden och observerad uppskalning | 10 |
| Diagnostik, reparerat selectorfel och webbkontroll | 10 |

Sätt bara poäng där du har bevis. Detta är en egen träningsskala, ingen uppgift om
Red Hats bedömning eller godkäntgräns. Skriv gärna ned tid och ledtrådar du behövde.
Slutläget ska fungera även efter att apparnas Pods ersatts.

## Ledtrådar

Använd `oc explain`, dokumentationen och dina tidigare observationsanteckningar.
Om du behöver läsa ett lösningsförslag, markera momentet som utfört med hjälp.

## Förklara med egna ord

- Vilket steg tog längst tid och vilken kunskapslucka avslöjade det?
- Vilka krav verifierade du genom funktion och vilka enbart genom konfiguration?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/18-traningsprov.md) efter ditt eget försök.

Spara dina observationer och avsluta port-forward/watch. Radera sedan endast
övningens namngivna resurser i ditt tilldelade projekt:

```sh
: "${LAB_PROJECT:?Sätt LAB_PROJECT till ditt tilldelade projektnamn}"
oc -n "$LAB_PROJECT" delete hpa web --ignore-not-found
oc -n "$LAB_PROJECT" delete job load --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete deployment web backend --ignore-not-found --cascade=foreground
oc -n "$LAB_PROJECT" delete pod inspector --ignore-not-found
oc -n "$LAB_PROJECT" delete route web --ignore-not-found
oc -n "$LAB_PROJECT" delete service web backend --ignore-not-found
oc -n "$LAB_PROJECT" delete configmap lab-code site-config load-code --ignore-not-found
oc -n "$LAB_PROJECT" delete secret web-secret --ignore-not-found
oc -n "$LAB_PROJECT" delete pvc web-data --ignore-not-found
```

Detta tar bort övningens PVC och dess lagrade data kan försvinna. Gör beständighetstestet före städning.
