# Biblioteca Blue
 
Sistema de gestión bibliotecaria compuesto por tres proyectos independientes que se comunican entre sí vía API REST.
 
**Anteriormente fue:** Proyecto final de la Segunda Unidad de Base de Datos hasta el commit del 24 de junio del 2026 xd.
**Ahora es:** Proyecto Final de la Tercera Unidad :D
 
## Arquitectura
 
- **WebApplication**: gestiona lectores y préstamos. Patrón MVC, se conecta al WebService vía API para obtener el catálogo de libros/ejemplares. Expone su propio API (`/api/lectores/`, `/api/prestamos/`) para que el Dashboard lo consuma.
- **WebService**: expone el catálogo (libros, autores, editoriales, géneros, ejemplares) vía API REST (Django REST Framework). Devuelve JSON.
- **Dashboard**: consume datos del WebApplication y del WebService, y genera informes, gráficos (Chart.js) y un modelo de regresión lineal sobre la tendencia de préstamos.
## Tecnologías
 
| Componente     | Framework    | Base de datos | Puerto |
|----------------|--------------|----------------|--------|
| WebApplication | Django (MVC) + mongoengine | MongoDB | 8000 |
| WebService     | Django + DRF | PostgreSQL     | 8001   |
| Dashboard      | Django + Chart.js | — (consume API) | 8002 |
 
## Infraestructura (Docker)
 
Todo el sistema —WebApplication, WebService, Dashboard y las bases de datos replicadas (MongoDB replica set y PostgreSQL streaming replication)— corre en contenedores, orquestados desde un único `docker-compose.yml` en la raíz:
 
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
| WebApplication (Django) | `webapp` | 8000 |
| WebService (Django) | `webservice` | 8001 |
| Dashboard (Django) | `dashboardblue` | 8002 |
 
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
 
Todo el sistema se levanta con un solo comando desde la raíz del proyecto:
 
```bash
docker compose up -d
```
 
Esto construye e inicia MongoDB (replica set), PostgreSQL (primaria + réplica), el WebApplication (`:8000`), el WebService (`:8001`) y el Dashboard (`:8002`).
 
Para reconstruir un servicio puntual tras un cambio de código (por ejemplo el Dashboard):
 
```bash
docker compose up -d --build dashboardblue
```
 
## Estado del proyecto
 
- [x] WebService: modelos, serializers, endpoints de listado/detalle/búsqueda
- [x] Replicación homogénea PostgreSQL (WebService)
- [x] Migración de WebApplication a MongoDB
- [x] Replicación homogénea MongoDB (WebApplication)
- [x] Dockerización completa del WebService (Django + Postgres primaria/réplica)
- [x] Autenticación y usuarios en MongoDB
- [x] Endpoints JSON del WebApplication para el Dashboard
- [x] Dockerización del WebApplication y del Dashboard
- [x] Dashboard: 4 gráficos (estado de préstamos, libros más prestados, géneros más solicitados, tendencia)
- [x] Modelo de regresión lineal (proyección de préstamos a 3 meses)
## Modelo Entidad-Relación
 
Ver `Modelo_ER/Sistema Bibliotecario.drawio`
