# Lösningsförslag 02: Inspektera images och kör en Linuxcontainer

Utgå från projektet och förutsättningarna i [uppgiften](../labbar/02-images.md).
Kommandon körs från repots rot. Detta är ett möjligt arbetssätt.

```sh
podman pull docker.io/library/python:3.12-slim
podman image inspect docker.io/library/python:3.12-slim
oc image info docker.io/library/python:3.12-slim
podman run -d --name ex180-local --user 10001:10001 -p 127.0.0.1:18082:8080 docker.io/library/python:3.12-slim python -m http.server 8080 --bind 0.0.0.0 --directory /tmp
curl -fsS http://127.0.0.1:18082/
podman logs ex180-local
podman exec ex180-local id
podman exec ex180-local touch /tmp/marker
podman restart ex180-local
podman exec ex180-local ls /tmp/marker
podman rm -f ex180-local
podman run -d --name ex180-local --user 10001:10001 -p 127.0.0.1:18082:8080 docker.io/library/python:3.12-slim python -m http.server 8080 --bind 0.0.0.0 --directory /tmp
podman exec ex180-local test ! -f /tmp/marker
podman rm -f ex180-local
```

Vänta tills servern startat innan HTTP-testet. Sista `test` ska lyckas (exitkod 0).
Image-användaren kan vara tom i metadata: det betyder normalt root som standard.
Här anger vi UID uttryckligen; OKD använder projektets tilldelade UID.

## Vanliga fel och vad de betyder

Upptagen lokal port: välj en ledig värdport. `ImagePull`/registry-fel: kontrollera
nätåtkomst och registry-begränsningar. Arkitektur i en multiarch-image måste passa körmiljön.
