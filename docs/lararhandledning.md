# Lärarhandledning: tilldelad användare och ett projekt per elev

## Förbered elevmiljön

Skapa användare, projekt och behörighet enligt klustrets ordinarie rutiner. Eleven får
exakt användarnamn, projektnamn, API-/konsoladress och inloggningsinstruktion. Eleven
sätter `LAB_PROJECT` till projektnamnet och använder samma projekt genom hela kursen.
Ett projekt förutsätts vara avsett för en elevs övningar, inte delat mellan flera elever
som samtidigt kör olika labbar med samma resursnamn.

Elever ska kunna hantera applikationsresurser i projektet, inklusive get/list/watch,
create/update/patch/delete för de typer som används: Pods, Deployments, Services,
Routes, ConfigMaps, Secrets, PVC:er, Jobs och HPA. De behöver även läsa ReplicaSets,
EndpointSlices och events samt använda Pod-loggar, exec och port-forward. Kontrollera
även åtkomst till det egna projektets Pod-mätvärden inför labb 14.

Tilldela detta via er vanliga projektroll. Elever behöver inte skapa eller radera
projekt, hantera noder, ändra SCC, StorageClass eller kluster-RBAC. Kontrollera med
elevens faktiska konto; ett administratörskonto kan annars dölja behörighetsproblem.
Template bearbetas lokalt i kursen, så en mall behöver inte installeras globalt.

Ge eleven en StorageClass som fungerar med dynamisk provisionering, ReadWriteOnce,
1 GiB och skrivning med projektets tilldelade UID/fsGroup. Om klassen inte är default
får eleven ange `storageClassName` i sin kopia av PVC-filen. Integrationslösningen
`losningar/15-stack.yaml` behöver då samma ändring. Eleven ska inte skapa PV eller
ändra StorageClass för att lösa övningen.

Kontrollera även:

- Klusterversion 4.22 och rätt klientversion.
- Tillgång till kursens Python-image för nodernas arkitektur samt lokal Podman-miljö för labb 02.
- Ingress, apps-DNS, Route-policy och betrott ingresscertifikat eller en utdelad CA-fil.
- NetworkPolicies som medger trafik inom projektet och från ingress till övningsapparna.
- Fungerande resource metrics och att eleven får läsa projektets mätvärden.
- Kvoter för Pods, Deployments, Services, Routes, ConfigMaps, Secrets, Jobs, PVC och HPA.
- CPU/minneskvoter med marginal för rullande uppdateringar och last-Jobben.

En praktisk budget för de fungerande övningsapparna är minst sex samtidiga Pods,
1 CPU och 512 MiB i summerade requests samt 2 CPU och 1 GiB i summerade limits.
Det inkluderar marginal för tre frontend-repliker, backend, last och provets inspector.
Rullande uppdateringar kan behöva ytterligare utrymme. Detta är en kursbudget,
inte ett exakt minimikrav för alla kluster.

Tidiga labbar anger inga requests/limits. Om ResourceQuota kräver dessa behöver en
lämplig LimitRange lägga till standardvärden, eller startmaterialet kompletteras före
utdelning. Labb 13:s extrema CPU-request kan och får nekas av kvoten; uppgiften tar
höjd för det. Eleven ska förklara avslaget, inte få högre kvot för just det testet.

## Återställning mellan laborationer

Eleven kör städningen i slutet av varje labb innan nästa start. Den använder explicita
resursnamn och `-n "$LAB_PROJECT"`. Projektet och dess grundkonfiguration finns kvar.
Spara inte lärarägda resurser med kursens namn, exempelvis `web`, `backend`, `lab-code`,
`site-config`, `web-config`, `web-secret` eller `web-data`.

I städningen tas controllers bort med foreground-radering före PVC. Efter lagringstestet
raderas elevens PVC och dess data kan försvinna beroende på reclaim policy.
Tillåt inte att eleven delar denna PVC med andra uppgifter som ska behållas.

Kvarvarande kvoter, LimitRange, RoleBindings och NetworkPolicies är normala och ska
behållas. Om eleven avbröt en labb kan den labbens städning köras igen eftersom den
använder `--ignore-not-found`. Städningen för en annan labb är ingen generell återställning.

## Labb 17: lärarens demonstration av must-gather

Det publika EX180-underlaget har med insamling av klusterdata. Elevernas projektroll
räcker inte för att själva köra den klusterinsamlingen. Visa den som lärare och ge dem
ett granskat utdrag att analysera. Det är en uttrycklig begränsning av elevens praktiska
måltäckning; höga projekträttigheter ersätter inte klusterbehörighet.

Följ [OKD 4.22:s insamlingsinstruktion](https://docs.okd.io/4.22/support/gathering-cluster-data.html)
med ett separat administratörskonto i labbklustret. Exempel för läraren:

```sh
oc whoami
oc whoami --show-server
mkdir -p .work/larare-17
oc adm must-gather --dest-dir=.work/larare-17/must-gather
echo $?
```

Kontrollera exitstatus och insamlingsloggen. Lista innehållet lokalt:

```sh
find .work/larare-17/must-gather -type f
du -sh .work/larare-17/must-gather
```

Använd en ny katalog vid nästa körning. Lokalt kan `rsync` behövas. Verktyget skapar
tillfälliga klusterresurser; inspektera avslutningsloggen och hantera eventuella rester
från just den körningen om insamlingen misslyckas.

Välj ett litet utdrag med exempel på resursdefinitioner och loggar för elevens
analysfrågor. Granska och maskera känsliga värden och andra elevers data före utdelning.
Dela inte hela insamlingen automatiskt. Inget laddas upp till extern support i denna labb.
