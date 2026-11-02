# Underlag och avgränsning

Kontrollerat 2026-11-02 mot [Red Hats publika EX180-sida](https://www.redhat.com/en/services/training/ex180-red-hat-certified-technologist-in-openshift-exam).
Den anger namnet **Red Hat Certified Technologist in OpenShift** och basversionen
**OpenShift Container Platform 4.22**. Den anger också att flera examensversioner används;
kontrollera din bokade version i Red Hats LMS. Äldre material med EX180 i titeln kan
ha annan inriktning.

| Sammanfattat publikt mål | Labb |
| --- | --- |
| CLI-installation och resursinspektion i CLI och webb | 01, 03–18 |
| Samla klusterunderlag för support | 17: elevanalys + lärardemonstration |
| Skapa Linuxcontainrar och Pods, hitta och inspektera images | 02–03 |
| Starta applikation från image och Template | 04, 10 |
| Skala och ge extern åtkomst | 04–06, 14–15 |
| Separera konfiguration och ordna beständig lagring | 07–09, 15 |
| Hälsokontroller, compute requests/limits och autoskalning | 12–14 |

Elever arbetar med projektbehörighet och kan inte själva utföra klusterinsamling.
Den delen visas av läraren; analys av ett utdrag ersätter inte egen praktisk träning
på insamlingskommandot. Övriga elevmoment körs i det tilldelade projektet.

Labb 11, felsökningsfallen och slutprovet förstärker dessa färdigheter.
Den pedagogiska uppdelningen i namngivna resurser är vår egen. Vi hävdar inte att
varje resurs eller feltyp uttryckligen nämns i mållistan. Övningarna är egenproducerade;
de är inte frågor från certifieringsprovet. Det avslutande tvåtimmarspasset är träning.

Målplattformen här är **OKD 4.22**. Provet gäller Red Hat OpenShift Container Platform.
Kubernetes-resurserna och OpenShift-API:erna tränas på OKD, men imageåtkomst,
webbgränssnitt, tillägg och supportvägar kan skilja sig. OKD-labben för supportdata
skickar ingenting till Red Hat och förutsätter inget Red Hat-supportavtal.

## Tekniska referenser

Använd [OKD 4.22-dokumentationen](https://docs.okd.io/4.22/welcome/index.html) och
`oc explain`/`oc ... --help` parallellt med laborationerna.

- [CLI](https://docs.okd.io/4.22/cli_reference/openshift_cli/getting-started-cli.html)
- [Hälsokontroller](https://docs.okd.io/4.22/applications/application-health.html)
- [HPA](https://docs.okd.io/4.22/nodes/pods/nodes-pods-autoscaling.html)
- [Klusterdiagnostik](https://docs.okd.io/4.22/support/gathering-cluster-data.html)

## Valideringsstatus

Materialet är skrivet för 4.22 och granskas lokalt för filstruktur, manifest och
övningsapp. Lokal validering ersätter inte en körning i ditt OKD-kluster.
Versionsnummer på en image-tagg kan ändras över tid. För identiska omkörningar kan
läraren dokumentera en verifierad image-digest för klustrets CPU-arkitektur efter labb 02.
