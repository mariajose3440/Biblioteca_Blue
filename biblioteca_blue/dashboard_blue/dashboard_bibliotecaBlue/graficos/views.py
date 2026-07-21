
import json
from collections import Counter
from datetime import date, datetime
 
import requests
from django.shortcuts import render
 
 
def index(request):
    contexto = {
        'error': None,
        'estado_labels': [], 'estado_data': [],
        'libros_labels': [], 'libros_data': [],
        'generos_labels': [], 'generos_data': [],
        'regresion': None,
    }
 
 
    # ── 1. Traer préstamos del WebApplication ───────────────────────
    try:
        resp = requests.get(
            "http://webapp:8000/api/prestamos/",
            timeout=5
        )
        resp.raise_for_status()
        prestamos = resp.json()
 
    except Exception as e:
        contexto['error'] = (
            f"No se pudo conectar al WebApplication. "
            f"Detalle: {e}"
        )
        return render(request, 'reportes/index.html', contexto)
 
 
    # ── 2. Traer catálogo del WebService ────────────────────────────
    try:
        resp = requests.get(
            "http://webservice:8001/ws/ejemplares/",
            timeout=5
        )
        resp.raise_for_status()
        ejemplares = resp.json()
 
    except Exception as e:
        contexto['error'] = (
            f"No se pudo conectar al WebService. "
            f"Detalle: {e}"
        )
        return render(request, 'reportes/index.html', contexto)
 
 
    # Mapear id_ejemplar -> {titulo, generos}
    ejemplares_por_id = {}
 
    for e in ejemplares:
        libro = e.get('isbn_libro') or {}
        generos = libro.get('generos') or []
 
        nombres_generos = [
            g.get('nombre_genero')
            for g in generos
        ] or ['Sin género']
 
 
        ejemplares_por_id[str(e.get('id_ejemplar'))] = {
            'titulo': libro.get('titulo', 'Desconocido'),
            'generos': nombres_generos,
        }
 
 
    hoy = date.today()
 
    estado_counter = Counter()
    libro_counter = Counter()
    genero_counter = Counter()
    prestamos_por_mes = Counter()
 
 
    for p in prestamos:
 
        # ── Estado del préstamo ──
        fecha_dev = p.get('fecha_devolucion')
        fecha_est = p.get('fecha_estimada')
 
 
        if fecha_dev:
            estado_counter['Devuelto'] += 1
 
        elif fecha_est and _parse_fecha(fecha_est) < hoy:
            estado_counter['Vencido'] += 1
 
        else:
            estado_counter['Activo'] += 1
 
 
 
        # ── Popularidad libros / géneros ──
        info = ejemplares_por_id.get(
            str(p.get('id_ejemplar'))
        )
 
 
        if info:
 
            libro_counter[info['titulo']] += 1
 
            for g in info['generos']:
                genero_counter[g] += 1
 
 
 
        # ── Agrupar préstamos por mes ──
        fecha_p = p.get('fecha_prestamo')
 
        if fecha_p:
 
            f = _parse_fecha(fecha_p)
 
            prestamos_por_mes[
                f.strftime('%Y-%m')
            ] += 1
 
 
 
    contexto['estado_labels'] = list(
        estado_counter.keys()
    )
 
    contexto['estado_data'] = list(
        estado_counter.values()
    )
 
 
    top_libros = libro_counter.most_common(10)
 
    contexto['libros_labels'] = [
        t for t, _ in top_libros
    ]
 
    contexto['libros_data'] = [
        c for _, c in top_libros
    ]
 
 
 
    top_generos = genero_counter.most_common(10)
 
    contexto['generos_labels'] = [
        g for g, _ in top_generos
    ]
 
    contexto['generos_data'] = [
        c for _, c in top_generos
    ]
 
 
 
    # ── 3. Regresión lineal ──────────────────────────
 
    meses_ordenados = sorted(
        prestamos_por_mes.keys()
    )
 
 
    if len(meses_ordenados) >= 2:
 
        xs = list(range(len(meses_ordenados)))
 
        ys = [
            prestamos_por_mes[m]
            for m in meses_ordenados
        ]
 
 
        pendiente, intercepto = _regresion_lineal(
            xs,
            ys
        )
 
 
        meses_futuros = 3
 
 
        meses_totales = (
            meses_ordenados +
            _siguientes_meses(
                meses_ordenados[-1],
                meses_futuros
            )
        )
 
 
        proyeccion = [
            round(
                pendiente * x + intercepto,
                2
            )
            for x in range(
                len(meses_totales)
            )
        ]
 
 
        reales = ys + [
            None
        ] * meses_futuros
 
 
 
        contexto['regresion'] = {
 
            'meses': meses_totales,
 
            'reales': reales,
 
            'proyectados': proyeccion,
 
            'pendiente': round(
                pendiente,
                3
            ),
 
            'intercepto': round(
                intercepto,
                3
            ),
        }
 
 
 
    # JSON para Chart.js
 
    for clave in [
        'estado_labels',
        'estado_data',
        'libros_labels',
        'libros_data',
        'generos_labels',
        'generos_data'
    ]:
 
        contexto[
            clave + '_json'
        ] = json.dumps(
            contexto[clave]
        )
 
 
    contexto['regresion_json'] = json.dumps(
        contexto['regresion']
    )
 
 
    return render(
        request,
        'reportes/index.html',
        contexto
    )
 
 
 
def _parse_fecha(valor):
 
    if isinstance(valor, str):
 
        return datetime.strptime(
            valor[:10],
            '%Y-%m-%d'
        ).date()
 
    return valor
 
 
 
def _regresion_lineal(xs, ys):
 
    n = len(xs)
 
    sum_x = sum(xs)
    sum_y = sum(ys)
 
    sum_xy = sum(
        x*y
        for x, y in zip(xs, ys)
    )
 
    sum_x2 = sum(
        x*x
        for x in xs
    )
 
 
    denominador = (
        n * sum_x2 -
        sum_x ** 2
    )
 
 
    if denominador == 0:
        return 0, sum_y / n
 
 
    pendiente = (
        n * sum_xy -
        sum_x * sum_y
    ) / denominador
 
 
    intercepto = (
        sum_y -
        pendiente * sum_x
    ) / n
 
 
    return pendiente, intercepto
 
 
 
def _siguientes_meses(
    ultimo_mes,
    cantidad
):
 
    anio, mes = map(
        int,
        ultimo_mes.split('-')
    )
 
 
    resultado = []
 
 
    for _ in range(cantidad):
 
        mes += 1
 
        if mes > 12:
 
            mes = 1
            anio += 1
 
 
        resultado.append(
            f"{anio:04d}-{mes:02d}"
        )
 
 
    return resultado
