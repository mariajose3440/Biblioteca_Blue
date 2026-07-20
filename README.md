# Biblioteca Blue
Sistema de gestión bibliotecaria compuesto por tres proyectos independientes que se comunican entre sí vía API REST.

**Anteriormente fue:** Proyecto final de la Segunda Unidad de Base de Datos hasta el commit del 24 de junio del 2026 xd.
**Ahora es:** Proyecto Final de la Tercera Unidad :D

## Arquitectura

- **WebApplication**: gestiona lectores y préstamos. Patrón MVC, se conecta al WebService vía API para obtener el catálogo de libros/ejemplares. Expone su propio API (`/api/lectores/`, `/api/prestamos/`) para que el Dashboard lo consuma.
- **WebService**: expone el catálogo (libros, autores, editoriales, géneros, ejemplares) vía API REST (Django REST Framework). Devuelve JSON.
- **Dashboard**: consume datos del WebApplication y genera informes, gráficos y un modelo de regresión lineal.

## Tecnologías

| Componente     | Framework    | Base de datos | Puerto |
|----------------|--------------|----------------|--------|
| WebApplication | Django (MVC) + mongoengine | MongoDB | 8000 |
| WebService     | Django + DRF | PostgreSQL     | 8001   |
| Dashboard      | Django       | — (consume API)| 8002   |

## Infraestructura (Docker)

Todo el WebService (Django + PostgreSQL primaria y réplica) y la base de datos del WebApplication (MongoDB replica set) corren en contenedores, orquestados desde un único `docker-compose.yml` en la raíz:

```bash
docker compose up -d
```

| Servicio | Contenedor | Puerto |
|---|---|---|
| MongoDB primaria | `biblioteca_blue` | 27018 |
| MongoDB réplica 1 | `replica_biblioteca_blue` | 27019 |
| MongoDB réplica 2 | `replica_biblioteca_blue2` | 27020 |
| PostgreSQL primaria | `postgres_webservice` | 5434 |
| PostgreSQL réplica | `postgres_webservice_replica` | 5435 |
| WebService (Django) | `webservice` | 8001 |

El WebApplication (Django + mongoengine) sigue corriendo nativo, conectándose al replica set de Mongo en Docker.

## Replicación

Ambos motores tienen **replicación homogénea** (streaming/replica set nativo del motor, sin herramientas externas):

- **PostgreSQL** (WebService): streaming replication, primaria (`5434`) → réplica de solo lectura (`5435`)
- **MongoDB** (WebApplication): replica set `rs0` de 3 nodos, con `biblioteca_blue` (`27018`) como primary

## Usuarios y permisos de BD

| Componente | Usuario | Motor | Permisos |
|---|---|---|---|
| WebService | `bluebul_web` | PostgreSQL | Todos los procesos |
| Dashboard | `lector_replica` | PostgreSQL | SELECT |
| WebApplication | `webapp_user` | MongoDB | readWrite |
| Dashboard | `dashboard_user` | MongoDB | read |
| Admin | `bluebul_admin` | MongoDB | root |

## Cómo levantar el proyecto

### Infraestructura (Mongo + Postgres + WebService)
```bash
docker compose up -d
```

### WebApplication (puerto 8000)
```bash
cd bibliotecaBlue/biblioteca_blue
source ../bin/activate
python manage.py runserver 8000
```

### Dashboard (puerto 8002)
```bash
cd dashboard
python manage.py runserver 8002
```

## Estado del proyecto
- [x] WebService: modelos, serializers, endpoints de listado/detalle/búsqueda
- [x] Replicación homogénea PostgreSQL (WebService)
- [x] Migración de WebApplication a MongoDB
- [x] Replicación homogénea MongoDB (WebApplication)
- [x] Dockerización completa del WebService (Django + Postgres primaria/réplica)
- [x] Autenticación y usuarios en MongoDB
- [x] Endpoints JSON del WebApplication para el Dashboard
- [ ] Dashboard: gráficos e informes
- [ ] Modelo de regresión lineal

## Modelo Entidad-Relación
Ver `Modelo_ER/Sistema Bibliotecario.drawio`
