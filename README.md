# Biblioteca Blue

Anteriormente fue:Proyecto final de la Segunda Unidad de Base de Datos hasta el commit del 24 de junio del 2026 xd.
Ahora es: Proyecto FInal de la Tercera Unidad :D
Sistema de gestión bibliotecaria compuesto por tres proyectos independientes que se comunican entre sí vía API REST.

- **WebApplication**: gestiona lectores y préstamos. Patrón MVC, se conecta al WebService vía API para obtener el catálogo de libros/ejemplares.
- **WebService**: expone el catálogo (libros, autores, editoriales, géneros, ejemplares) vía API REST (Django REST Framework). Devuelve JSON.
- **Dashboard**: consume datos del WebApplication y genera informes, gráficos y un modelo de regresión lineal.

## Tecnologías

| Componente     | Framework | Base de datos | Puerto |
|----------------|--------------|----------------|--------|
| WebApplication | Django (MVC) | MongoDB | 8000 |
| WebService     | Django + DRF | PostgreSQL | 8001 |
| Dashboard      | Django | — (consume API) | 8002 |

## Replicación

El WebService cuenta con **replicación homogénea de PostgreSQL** (streaming replication):
- Primaria: puerto `5432`
- Réplica (standby, solo lectura): puerto `5433`

## Cómo levantar el proyecto

### WebService (puerto 8001)
```bash
cd ws_LibrosBlue/ws_blue
source ../bin/activate
python manage.py runserver 8001
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
- [ ] Migración de WebApplication a MongoDB
- [ ] Replicación homogénea MongoDB (WebApplication)
- [ ] Dashboard: gráficos e informes
- [ ] Modelo de regresión lineal

## Modelo Entidad-Relación

Ver `Modelo_ER/Sistema Bibliotecario.drawio`
