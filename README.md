# Simple backend with htmx

## 1. Clone project

```sh
git clone git@github.com:zimkaa/test_only_backend.git && cd test_only_backend
```

## 2. Start project

```sh
docker compose -f compose.yaml up --build
```

## 3. Query from console

### Success query

```sh
curl -sv -XPOST -H 'Content-Type: application/json' -d '{"first_name": "Ivan", "last_name": "Ivanov", "date": "2025-01-02"}' http://localhost:8000/api/submit
```

### Fail query

```sh
curl -sv -XPOST -H 'Content-Type: application/json' -d '{"first_name": "Ivan Ivanov", "last_name": "Ivanov", "date": "2025-01-02"}' http://localhost:8000/api/submit
```

## 4. Query from browser

Open your browser

[http://localhost:8000/](http://localhost:8000/)
