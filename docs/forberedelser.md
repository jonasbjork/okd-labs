# Förberedelser och arbetssätt

## Miljö

Du behöver ett redan installerat OKD 4.22-kluster, inloggningsuppgifter, `oc` 4.22,
`curl`, Python 3 och en terminal med bash eller zsh. Podman används lokalt i labb 02.
På macOS måste en Podman-machine vara startad. Klusterinstallation ingår inte.

Hämta `oc` via klustrets webbkonsolemeny för kommandoradsverktyg eller den
[officiella CLI-instruktionen](https://docs.okd.io/4.22/cli_reference/openshift_cli/getting-started-cli.html).
Välj rätt operativsystem och arkitektur, packa upp och placera binären i din PATH.
Kontrollera med `oc version --client`. Använd klustrets URL och inloggningsmetod:

```sh
oc login https://api.DITT-KLUSTER:6443
oc whoami
oc version
```

Kontrollera att servern är 4.22. Om klusterinformationen kräver extra behörighet
kan administratören bekräfta versionen. Kopiera inte token till rapporter eller Git.

Läraren ger dig **en användare och ett befintligt projekt**. Alla klusterövningar
körs i det projektet. Du har rätt att hantera övningsresurser inom projektet, men
behöver inte kunna skapa eller radera projekt, administrera noder eller ändra SCC/RBAC.
Klusterförberedelser och must-gather hanteras i [lärarhandledningen](lararhandledning.md).

Övriga förutsättningar:

- Klusternoderna behöver nå `docker.io/library/python:3.12-slim`. Spegla vid behov
  bilden och byt image-referens i kursfiler och kommandon. Docker Hub kan ha pull-begränsningar.
- Fungerande ingress, apps-DNS och klientåtkomst krävs för Routes.
- Labb 09, 15 och 18 behöver en dynamisk StorageClass och minst 1 GiB tillgängligt för elevens PVC.
- Labb 14 behöver fungerande resource metrics API och kapacitet för tre små webb-Pods.
- Lokala Podman-containern ska nås på localhost. Klustrets NetworkPolicies måste
  tillåta övningarnas kommunikation inom projektet och från ingress.


## Kör från repots rot

Alla sökvägar i kommandon utgår från mappen med README.md. Spara eget arbete i
`.work/`, som ignoreras av Git. Använd samma terminal för variabler i en övning.

```sh
mkdir -p .work
# Ersätt elevprojekt med exakt det projektnamn läraren har gett dig.
export LAB_PROJECT=elevprojekt
oc project "$LAB_PROJECT"
oc whoami
```

Kontrollera användarnamnet mot det läraren tilldelat dig. Sätt samma variabel i varje
ny terminal där du använder städkommandon. Projektet ska redan finnas; be läraren
kontrollera tilldelningen om projektvalet misslyckas.

**Kör en labb åt gången.** Städa föregående labbs namngivna resurser innan nästa start.
Övningarna återanvänder bland annat `web`, `lab-code` och `web-data`. Kvarvarande
miljövariabler, volymer, probes och HPA kan annars påverka nästa övning.
Ett nytt `oc apply` av startfilen är inte en fullständig återställning.

Projektet ska användas för kursen. Behåll lärarens resurser, exempelvis ResourceQuota,
LimitRange, RoleBindings och NetworkPolicies. Varje labb har städning med uttryckliga
resursnamn; städningen tar inte bort projektet eller alla resurser i det.
Du kan repetera valfri labb efter att ha städat den tidigare övningen.

## Kontrollera dina projekträttigheter

```sh
oc auth can-i create pods
oc auth can-i create deployments.apps
oc auth can-i create services
oc auth can-i create routes.route.openshift.io
oc auth can-i create persistentvolumeclaims
oc auth can-i create configmaps
oc auth can-i create secrets
oc auth can-i create jobs.batch
oc auth can-i create horizontalpodautoscalers.autoscaling
```

Kontrollerna ovan gäller ditt nu valda projekt. Svar `no` för en nödvändig
resurs eller ett `Forbidden` i övningen ska tas upp med läraren. Läraren anger
StorageClass och bekräftar metrics; elever behöver inte lista klusterresurser.
Kontrollera egna Pod-mätvärden med `oc adm top pods` i labb 14. Kommandots namn
innehåller `adm`, men projektets Pod-mätvärden kan läsas utan klusteradmin om rättigheten tilldelats.

## Två startpaket

**Basic** i labb 04–06 är Python-standardbibliotekets filserver på port 8080.
Rotadressen ger en kataloglista för `/tmp`; det är ett korrekt HTTP-svar.

**Övningsappen** i labb 07–18 finns i `assets/server.py`. Starta den när en labb
hänvisar till appstarten:

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py --dry-run=client -o yaml | oc apply -f -
oc apply -f assets/app-deployment.yaml
oc apply -f assets/service.yaml
oc rollout status deployment/web --timeout=180s
```

`lab-code` levererar redan färdig programkod. Du behöver inte skriva Python.
I labb 07 skapar du en annan ConfigMap för applikationens inställningar.
Appen skriver inte ut sin token. Den har följande gränssnitt:

| Sökväg | Funktion |
| --- | --- |
| `GET /` | JSON: hälsning, filkonfiguration, version, Pod-namn och om token finns |
| `GET /ready` | 503 om `/tmp/not-ready` finns, annars 200 |
| `GET /live` | 503 om `/tmp/fail-live` finns, annars 200 |
| `GET /work` | Begränsat CPU-arbete per anrop för HPA-labben |
| `GET /state` | Läser `/data/state.txt`, tom sträng om fil saknas |
| `POST /state` | Sparar högst 4096 byte i `/data/state.txt`; kräver `X-Lab-Token` |
| `GET /backend` | Anropar URL från `BACKEND_URL` och visar svaret |

`MESSAGE` och `APP_VERSION` läses från processens miljö. Filen
`/etc/lab-config/message` och tokenfilen `/etc/lab-secret/token` läses per anrop.
`LAB_TOKEN` har företräde framför tokenfilen. Appen är ett utbildningshjälpmedel.

## Verifiera utan Route

I en terminal:

```sh
oc port-forward service/web 18080:80
```

I en annan terminal: `curl -fsS http://127.0.0.1:18080/`.
Avsluta port-forward med Ctrl-C innan du städar eller börjar nästa labb. Den lokala tunneln kan behöva
startas om efter Pod-byte; Service och Route är de beständiga åtkomstvägarna.

Om en instruktion ber dig välja en Pod:

```sh
POD=$(oc get pods -l app=web -o jsonpath='{.items[0].metadata.name}')
oc get pod "$POD"
```

Gör det efter färdig utrullning, när en enda replik används. Använd `oc exec "$POD" -- ...`
för att träffa just den Pod du observerar.

## YAML, rättigheter och städning

`apiVersion` anger API, `kind` resurstyp, `metadata` identitet och `spec` önskat tillstånd.
`status` beskriver observerat tillstånd och ska normalt inte skrivas i dina manifest.
`oc apply` skickar en deklaration; en controller arbetar sedan mot det önskade tillståndet.
`oc explain deployment.spec.template.spec` hjälper dig hitta rätt fält.

Manifesten använder en icke privilegierad container, port 8080 och inget fast UID.
OKD:s SCC tilldelar ett UID för projektet. Be inte om `anyuid` för att kringgå ett image-
eller filrättighetsproblem. Kontrollera loggar, events och skrivrättigheter först.

Varje labb visar sin städning med `-n "$LAB_PROJECT"` och uttryckliga resursnamn.
Controllers tas bort före deras volymer; foreground-radering väntar in ägda Pods.
I lagringslabbarna raderas övningens PVC först när beständighetstestet är färdigt.
Datalagringens slutliga livscykel beror på PV:ns reclaim policy, som läraren hanterar.
Spara observationsanteckningar före städning och radera inte lärarens grundkonfiguration.

## Bedöm ditt arbete

Anteckna för varje labb: vilket slutkrav du bevisat, vilket kommando som bevisar det,
vad du först trodde och vad observationen visade. Försök först själv, använd sedan
ledtrådar och öppna lösningsförslaget sist. YAML-filer i `assets/` är startmaterial;
för senare labbar behöver du själv kombinera och ändra dem.
