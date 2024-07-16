# Migracion de base de datos de metabase


## si es windows
```bash
docker exec -it metabase-db bash -c "pg_dump -h localhost -p 5432 -U mtb -d mtb -F p -E UTF-8 --no-comments -f /tmp/mydatabase.sql"
```

## si es linux
```bash
docker exec -it metabase-db bash -c pg_dump -h localhost -p 5432 -U mtb -d mtb -F p -E UTF-8 --no-comments -f /tmp/mydatabase.sql
```

## Luego se copia el archivo a la maquina local
```bash
docker cp metabase-db:/tmp/mydatabase.sql ./metabaseDBMig/
```