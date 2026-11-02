# Validering

## Lokal kontroll

Genomförd 2026-11-02: samtliga lokala kontroller passerade med `oc` 4.22.18.
Det omfattade 18 uppgifter och 18 lösningar, syntaxkontroll av shellblock, 15 YAML-filer med
22 objekt, sju lokala CLI-transformeringar, Template-bearbetning och HTTP-kontroller.
HTTP-kontrollen kördes på datorns Python, inte i den angivna containerimagen.

Kommandot är `python3 scripts/validate.py`. Det ändrar inte klustret.
Kontrollen omfattar:

- Att alla 18 uppgifter har lösningsförslag, att lokala länkar finns och att shellblock går att syntaxkontrollera.
- Att elevmaterialet använder tilldelat projekt, saknar projektadministration och klusterinsamling som elevkommando samt städar explicit namngivna resurser.
- YAML-tolkning, grundläggande objektrelationer och integrationsmanifestets selectors,
  portar, probes och referenser till ConfigMap, Secret och PVC.
- Template-bearbetning och exempel på volym-, probe- och resursändringar med `oc --local`.
- Övningsappens faktiska HTTP-svar, filkonfiguration, hälsoflaggor, tokenrotation,
  godkända/nekade skrivningar, datalagring, backend-anrop och CPU-endpoint.

Kontrollen är inte fullständig Kubernetes-schema- eller servervalidering.
Avsiktliga fel i `assets/fel/` är inte avsedda att fungera som applikationer.

## Kvar att verifiera i OKD 4.22

Ingen laboration har här körts mot ett OKD-kluster. Ingen aktiv kubeconfig har använts
för att skapa, ändra eller radera klusterresurser. Följande behöver verifieras i målmiljön:

- Image-pull, vald arkitektur och SCC/admission med elevens faktiska projekträttigheter.
- Resursskapande från kommandon och manifest samt uppdateringar i webbgränssnittet.
- Service/DNS, Route admission, HTTPS-certifikat och nätverkspolicy.
- ConfigMap-/Secret-projektionens fördröjning och omstartsbeteende.
- PVC-provisionering, skrivrättigheter och datans överlevnad vid Pod-byte.
- Probe-förlopp, OOMKilled, schemaläggningsfall och rollback.
- Resource metrics, upp-/nedskalning under last och tillgänglig klusterkapacitet.
- Lärarens behörigheter, image och lokala beroenden för must-gather.

För första klustergenomgången: kör i ordning, spara observerade avvikelser i `.work/`,
notera klustrets version och StorageClass och dokumentera en fungerande image-digest.
