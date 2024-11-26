# Somfy fake api

Api des tests pour la formation 3h de Somfy sur les api.

L'API ne dispose pas de base de données et gère le stockage en mémoire.

## Installation

### En local

- Installer uv: https://docs.astral.sh/uv/getting-started/installation/
- Lancer l'application:

  ```bash
  uv run fastapi dev api.py
  ```

- L'api est servie sur `http://localhost:8000`

### Docker

```bash
docker compose up
```
