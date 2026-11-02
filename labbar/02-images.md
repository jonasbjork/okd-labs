# 02. Inspektera images och kör en Linuxcontainer

**Nivå:** Grund · **Tid:** 30–45 min · **Förkunskaper:** Labb 01 och Podman

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

Denna övning körs lokalt. Imageinspektionen med `oc image info` kontaktar registry och skapar inga projektresurser.

## Varför och hur det fungerar

En image är paketet med filsystem och startmetadata. En container är en körande
instans med en egen skrivbar del. En tagg är ett flyttbart namn; en digest identifierar
innehåll. Containerporten publiceras inte automatiskt på din dator.

## Uppgift

1. Hitta Python Official Image i Docker Hub och välj `docker.io/library/python:3.12-slim`.
2. Hämta bilden. Inspektera operativsystem, arkitektur, användare, Entrypoint och Cmd.
3. Inspektera även registry-metadata med `oc image info`.
4. Starta en container `ex180-local` som serverar `/tmp` på port 8080.
   Publicera den som `127.0.0.1:18082` och kör processen med UID 10001.
5. Hämta ett HTTP-svar, visa loggar och kör `id` inuti containern.
6. Skapa `/tmp/marker` i containern. Starta om samma container och kontrollera filen.
7. Ta bort containern, skapa en ny med samma image och kontrollera att filen saknas.

## Verifiera slutresultatet

```sh
curl -fsS http://127.0.0.1:18082/
podman logs ex180-local
podman exec ex180-local id
```

HTTP ska svara med en kataloglista. UID ska vara 10001. Markören ska överleva
omstart av samma container men försvinna när containern tas bort och ersätts.

## Ledtrådar

`podman image inspect`, `podman run --help`, `podman exec` och `podman restart`.
På macOS: kontrollera `podman machine list` om motorn inte går att nå.

## Förklara med egna ord

- Vad är skillnaden mellan att starta om och att återskapa en container?
- Vilken plattformsdigest skulle du dokumentera för reproducerbarhet?

## Lösning och städning

Öppna [lösningsförslaget](../losningar/02-images.md) efter ditt eget försök.

Denna labb skapar inga projektresurser. Ta bort den lokala Podman-containern enligt lösningsförslaget.
