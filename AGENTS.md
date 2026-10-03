# Base44 Dev Environment

## Project
A minimal C project with a single source file `The start.c` that prints "Hello World".

## Setup
- `Dockerfile.dev` — based on `python:3.12-slim`, installs `gcc` (no source baked in).
- `dev_server.py` — a Python HTTP server on port 3000 that recompiles `The start.c` on every request and serves the output as HTML.
- Source is bind-mounted via compose; edits to `The start.c` are reflected on the next page reload (no rebuild needed).

## Verify
```sh
docker compose -f docker-compose.base44.yml up -d --build
curl localhost:3000   # returns HTML with the program output
```
