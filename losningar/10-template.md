# Lösningsförslag 10: Skapa applikationer med Template

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/10-template.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
oc create configmap lab-code --from-file=server.py=assets/server.py
oc process --local -f assets/template.yaml --parameters
mkdir -p .work
oc process --local -f assets/template.yaml -p NAME=demo -p 'MESSAGE=Skapad från mall' -o yaml > .work/template-result.yaml
oc apply -f .work/template-result.yaml
oc process --local -f assets/template.yaml -p NAME=demo2 -p 'MESSAGE=Andra instansen' | oc apply -f -
oc rollout status deployment/demo --timeout=180s
oc rollout status deployment/demo2 --timeout=180s
oc port-forward service/demo 18080:80
```

Testa `curl -fsS http://127.0.0.1:18080/`, avsluta och gör samma sak med
`service/demo2`. Resursernas labels gör att de inte delar trafik trots samma image.

## Vanliga fel och vad de betyder

Parametrar lämnas oersatta: använd `oc process`, inte `oc apply` direkt för att starta
objekten i en Template. En Template är inte en Deployment-controller.
