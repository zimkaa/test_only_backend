# Simple backend with htmx

## Usage

### 1. Clone project

```sh
git clone git@github.com:zimkaa/test_only_backend.git && cd test_only_backend
```

### 2. Start project

```sh
docker compose -f compose.yaml up --build
```

### 3. Query from console

#### Success query

```sh
curl -sv -XPOST -H 'Content-Type: application/json' -d '{"first_name": "Ivan", "last_name": "Ivanov", "date": "2025-01-02"}' http://localhost:8000/api/submit
```

#### Fail queries

```sh
curl -sv -XPOST -H 'Content-Type: application/json' -d '{"first_name": "Ivan Ivanov", "last_name": "Ivanov", "date": "2025-01-02"}' http://localhost:8000/api/submit
```

```sh
curl -sv -XPOST -H 'Content-Type: application/json' -d '{"first_name": "Ivan", "last_name": "Ivanov", "date": "2025-55-02"}' http://localhost:8000/api/submit
```

### 4. Query from browser

Open your browser

[http://localhost:8000/](http://localhost:8000/)

## Develop

### Using devcontainer and devpod

#### Start

```sh
devpod up .
```

##### Install dependency inside container

```sh
pip install -r requirements-test.txt
```

##### Run tests

```sh
pytest -vvv
```

#### Stop

```sh
devpod stop
```
