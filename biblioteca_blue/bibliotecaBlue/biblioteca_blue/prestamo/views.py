from django.shortcuts import render
from modelo.models import Lector, Prestamo
import requests


def guardar(request):
    lectores = Lector.objects.all()

    # Obtener ejemplares desde el servicio externo (webserviceLibros)
    # (se cargan tanto para GET como para POST)
    ejemplares = []
    libros_por_isbn = {}  # agrupa ejemplares por ISBN para mostrar "libros" únicos
    try:
        response = requests.get("http://localhost:8001/ws/ejemplares/")
        if response.status_code == 200:
            data = response.json()
            for e in data:
                libro = e.get('isbn_libro') or {}
                autores = libro.get('autores') or []
                autor = autores[0].get('seudononimo', '') if autores else ''
                editorial = (libro.get('codigo_editorial') or {}).get('nombre', '')
                isbn = libro.get('isbn')
                titulo = libro.get('titulo', '')

                ejemplares.append({
                    'id_ejemplar': e.get('id_ejemplar'),
                    'isbn': isbn,
                    'titulo': titulo,
                    'autor': autor,
                    'anio': libro.get('anio_publicacion', ''),
                    'editorial': editorial,
                    'descripcion': libro.get('descripcion', ''),
                })

                # Agrupar por ISBN: un "libro" único con su cantidad de ejemplares
                if isbn not in libros_por_isbn:
                    libros_por_isbn[isbn] = {
                        'isbn': isbn,
                        'titulo': titulo,
                        'autor': autor,
                        'anio': libro.get('anio_publicacion', ''),
                        'editorial': editorial,
                        'descripcion': libro.get('descripcion', ''),
                        'cantidad_ejemplares': 0,
                    }
                libros_por_isbn[isbn]['cantidad_ejemplares'] += 1
    except Exception as e:
        print("Error al obtener ejemplares:", e)

    libros = list(libros_por_isbn.values())

    # Préstamos realizados, con el lector y el título del ejemplar prestado
    ejemplares_por_id = {ej['id_ejemplar']: ej for ej in ejemplares}
    prestamos = []
    for p in Prestamo.objects.select_related('lector').order_by('-fecha_prestamo'):
        ejemplar_info = ejemplares_por_id.get(int(p.id_ejemplar)) if str(p.id_ejemplar).isdigit() else None
        prestamos.append({
            'id_prestamo': p.id_prestamo,
            'lector': p.lector.nombres,
            'id_ejemplar': p.id_ejemplar,
            'titulo': ejemplar_info['titulo'] if ejemplar_info else None,
            'fecha_prestamo': p.fecha_prestamo,
            'fecha_estimada': p.fecha_estimada,
        })

    contexto = {
        'lectores': lectores,
        'libros': libros,
        'ejemplares': ejemplares,
        'prestamos': prestamos,
    }

    if request.method == 'POST':
        try:
            # Lector seleccionado en el formulario
            lector = Lector.objects.get(id=request.POST.get('lector_id'))

            Prestamo.objects.create(
                lector=lector,
                id_ejemplar=request.POST.get('id_ejemplar'),
                fecha_prestamo=request.POST.get('fecha_prestamo'),
                fecha_estimada=request.POST.get('fecha_estimada') or None,
            )
            contexto['mensaje'] = 'Préstamo guardado correctamente.'
        except Exception as e:
            contexto['error'] = str(e)

    return render(request, 'index.html', contexto)
