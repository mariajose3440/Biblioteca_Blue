from django.shortcuts import render, redirect
from modelo.models import Lector, Prestamo
import requests

def guardar(request):
    lectores = Lector.objects.all()


    ejemplares = []
    libros_por_isbn = {}
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

    # ------------------ PROCESAR POST PRIMERO ------------------
    mensaje = None
    error = None

    if request.method == 'POST':
        try:
            lector = Lector.objects.get(id=request.POST.get('lector_id'))

            Prestamo.objects.create(
                lector=lector,
                id_ejemplar=request.POST.get('id_ejemplar'),
                fecha_prestamo=request.POST.get('fecha_prestamo'),
                fecha_estimada=request.POST.get('fecha_estimada') or None,
            )
            mensaje = 'Préstamo guardado correctamente.'
        except Exception as e:
            error = str(e)

    ejemplares_por_id = {ej['id_ejemplar']: ej for ej in ejemplares}
    prestamos = []
    for p in Prestamo.objects.order_by('-fecha_prestamo'):
        ejemplar_info = ejemplares_por_id.get(int(p.id_ejemplar)) if str(p.id_ejemplar).isdigit() else None
        prestamos.append({
            'id_prestamo': str(p.id),          # <--- ¡corregido!
            'lector': p.lector.nombres,
            'id_ejemplar': p.id_ejemplar,
            'titulo': ejemplar_info['titulo'] if ejemplar_info else None,
            'fecha_prestamo': p.fecha_prestamo,
            'fecha_estimada': p.fecha_estimada,
            'fecha_devolucion': p.fecha_devolucion,
        })

    contexto = {
        'lectores': lectores,
        'libros': libros,
        'ejemplares': ejemplares,
        'prestamos': prestamos,
        'mensaje': mensaje,
        'error': error,
    }

    return render(request, 'index.html', contexto)

def marcar_devuelto(request, prestamo_id):
    if request.method == 'POST':
        try:
            prestamo = Prestamo.objects.get(id=prestamo_id)
            fecha = request.POST.get('fecha_devolucion')
            if fecha:
                prestamo.fecha_devolucion = fecha
                prestamo.save()
        except Prestamo.DoesNotExist:
            pass
    return redirect('guardar_prestamo')
