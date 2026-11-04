# OKD 4.22 – laborationer med EX180 som ram

18 praktiska laborationer på svenska, med stegvis ökande svårighet, förklaringar,
kontroller och separata lösningsförslag. Börja med
[förberedelser och arbetssätt](docs/forberedelser.md). Läs även
[examensmål, källor och avgränsningar](docs/examensmal.md).

Underlaget är Red Hats publika mål för **EX180 – Red Hat Certified Technologist
in OpenShift**, som vid kontroll 2026-11-02 anger OpenShift Container Platform 4.22.
Här utförs träningen på **OKD 4.22**. Detta är eget utbildningsmaterial.

> Laborationerna är framtagna av [Jonas Björk](https://jonasbjork.me/) på [Karoshi AB](https://karoshi.se) med hjälp av [Codex](https://openai.com/sv-SE/codex/).
> 
> Vill du stödja mitt arbete? Bjud mig på en kaffe!

<center><a href="https://www.buymeacoffee.com/jonasbjork"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" style="width: 200px"/></a></center>

## Välj laboration

| Nr | Laboration | Nivå | Ungefärlig tid |
| --- | --- | --- | --- |
| 01 | [CLI, projekt och webbgränssnitt](labbar/01-miljon.md) | Grund | 30–45 min |
| 02 | [Inspektera images och kör en Linuxcontainer](labbar/02-images.md) | Grund | 30–45 min |
| 03 | [En Pod från kommando till YAML](labbar/03-pod.md) | Grund | 35–45 min |
| 04 | [Deployment, repliker och självläkning](labbar/04-deployment.md) | Grund | 35–45 min |
| 05 | [Service, selectors och intern DNS](labbar/05-service.md) | Grund+ | 40–50 min |
| 06 | [Route, HTTP och TLS](labbar/06-route.md) | Medel | 40–50 min |
| 07 | [Konfiguration med ConfigMap](labbar/07-configmap.md) | Medel | 45–60 min |
| 08 | [Secret som miljö och fil](labbar/08-secret.md) | Medel | 40–50 min |
| 09 | [PVC och data efter Pod-byte](labbar/09-pvc.md) | Medel | 50–60 min |
| 10 | [Skapa applikationer med Template](labbar/10-template.md) | Medel | 35–45 min |
| 11 | [Utrullning och återställning](labbar/11-rollout.md) | Medel | 40–50 min |
| 12 | [Readiness, liveness och startup](labbar/12-probes.md) | Medel+ | 50–60 min |
| 13 | [Requests, limits och ett minnesfel](labbar/13-resurser.md) | Medel+ | 45–60 min |
| 14 | [Autoskalning med kontrollerad belastning](labbar/14-hpa.md) | Avancerad | 50–60 min |
| 15 | [Bygg en sammanhängande applikation](labbar/15-helhet.md) | Avancerad | 75–100 min |
| 16 | [Felsökningsverkstad med förberedda fel](labbar/16-felsokning.md) | Avancerad | 60–90 min |
| 17 | [Samla diagnostik och klusterunderlag](labbar/17-diagnostik.md) | Avancerad | 40–60 min |
| 18 | [Praktiskt träningsprov](labbar/18-traningsprov.md) | Självständig | 120 min |

Tiderna avser aktivt övningsarbete; installation och klustrets starttid ingår inte.
Varje elev använder en tilldelad användare och ett tilldelat projekt under hela kursen.
Kör en labb åt gången och använd dess städning före nästa. Eleverna behöver ingen
klusteradminbehörighet. Se [lärarhandledningen](docs/lararhandledning.md) för miljöförberedelser
och lärarens demonstration av klusterinsamling.

## Så använder du materialet

1. Läs förklaringen och slutkraven.
2. Utför uppgiften och spara ditt arbete i `.work/`.
3. Verifiera funktion och anteckna bevis.
4. Läs ledtrådar vid behov, sedan lösningsförslaget.
5. Besvara reflektionsfrågorna och städa projektet när du är klar.

Labb 01–06 ger mycket stöd. Labb 07–14 kräver fler egna ändringar. Labb 15–18
kombinerar resurser och lägger större vikt vid självständig felsökning.

## Filer och lokal kontroll

- `labbar/`: uppgifter, teori, verifiering och städning.
- `losningar/`: kommenterade lösningsförslag och komplett integrationsmanifest.
- `assets/`: startmanifest, övningsserver och avsiktliga fel för labb 16.
- `docs/`: förutsättningar och målkoppling.
- `scripts/`: lokal kontroll av filer, YAML och övningsserver.

Kör `python3 scripts/validate.py` för lokal kontroll. Den använder Python 3 samt
Ruby med standardbiblioteket YAML; den kontaktar inte klustret.
Se [valideringsrapporten](docs/validering.md) för vad som kontrollerats och vad som återstår.
