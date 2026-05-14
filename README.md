# Insecure Bank Corporation

You can find the application live [mighy-muffin.io](http://www.mighy-muffin.io).

## Running the application locally

1. Build and run the application:

   ```bash
   uv venv .venv --python 3.10 && source .venv/bin/activate
   uv sync --all-extras --dev --frozen
   uv run python src/manage.py migrate
   uv run python src/manage.py runserver
   ```

2. You can then access the bank application here: [localhost:8000](http://localhost:8000)

## Running with Docker

1. Build and run the application with Docker.

   ```bash
   docker build \
     --build-arg GIT_COMMIT=$(git rev-parse --short HEAD) \
     --build-arg REPO_URL=$(git config --get remote.origin.url | sed 's/git@/https:\/\//; s/.com:/.com\//; s/\.git$//') \
     --file Dockerfile --no-cache --tag ibc .
   docker stop ibc && docker rm ibc
   docker run --detach --publish 8000:8000 --name ibc ibc
   docker logs ibc
   ```

2. Open the application here: [localhost:8000](http://localhost:8000)ww

## Login credentials

```text
Username: guillaume
Password: timinou
```
