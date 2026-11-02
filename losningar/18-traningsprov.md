# Lösningsförslag 18: Praktiskt träningsprov

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/18-traningsprov.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

1. Genomför imageinspektion enligt labb 02 och skapa `inspector` enligt labb 03, med
   `--command -- sleep 3600`. `oc exec inspector -- id` visar körande UID.
2. Skapa `lab-code`, rendera och skapa Template-resurserna:

```sh
mkdir -p .work/prov-18
oc create configmap lab-code --from-file=server.py=assets/server.py
oc process --local -f assets/template.yaml -p NAME=web -p 'MESSAGE=Prov klart' -o yaml > .work/prov-18/rendered.yaml
oc apply -f .work/prov-18/rendered.yaml
```

3. Utgå från [15-stack.yaml](15-stack.yaml) och spara en egen kopia. Ändra
   site-configs MESSAGE till `Prov klart` och BACKEND_MESSAGE till `Lagring redo`.
   Ta bort det fasta MESSAGE-värdet från den mallskapade Deploymenten innan du
   applicerar stacken, så att en valueFrom-referens kan ersätta det:

```sh
oc set env deployment/web MESSAGE-
```

4. Applicera din stackfil, invänta båda utrullningarna och testa kedjan enligt labb 15.
   Använd texten `exam-marker` i lagringstestet. Använd `--cacert` om klustret har egen CA.
5. Lägg till HPA och kör sedan lasten enligt labb 14. Stacken börjar med två frontend-
   repliker; efter HPA kan antalet bli 1–3 beroende på last. Observera en faktisk ökning.
6. Samla underlag enligt del A i labb 17, men till `.work/prov-18/`.
7. Bryt och reparera selector:

```sh
oc patch service web --type=merge -p '{"spec":{"selector":{"app":"wrong"}}}'
oc get endpointslices -l kubernetes.io/service-name=web -o yaml > .work/prov-18/broken-endpoints.yaml
oc patch service web --type=merge -p '{"spec":{"selector":{"app":"web"}}}'
```

Verifiera Route på nytt och läs de faktiska Pod-specifikationerna för probes/resurser.
Skriv inte in HPA:s aktuella replicaantal som ett fast slutkrav i din rapport.
Radera last-Jobben och sammanställ bevis mot tabellen innan timern stoppas.

## Vanliga fel och vad de betyder

Att ett objekt finns är inte samma sak som att dess funktion är bevisad. En PVC
utan sparad/återläst data bevisar inte beständighet. En skapad HPA utan mätvärden och
skalning bevisar inte fungerande autoskalning. Be om miljöåtgärd om en nödvändig
tjänst saknas; markera det momentet som ej verifierat.
