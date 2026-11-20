from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Categoria, Libro


def inicio(request):
    return render(request, 'catalogo/inicio.html')


def listar_libros(request):
    libros = Libro.objects.select_related('id_categoria_fk').prefetch_related('autores').all()

    contexto = {
        'libros': libros
    }

    return render(request, 'catalogo/libros.html', contexto)


def listar_categorias(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()

        if not nombre:
            messages.error(request, 'El nombre de la categoría es obligatorio.')
        elif Categoria.objects.filter(nombre__iexact=nombre).exists():
            messages.error(request, 'Ya existe una categoría con ese nombre.')
        else:
            Categoria.objects.create(
                nombre=nombre,
                descripcion=descripcion or None
            )
            messages.success(request, 'La categoría se registró correctamente.')
            return redirect('listar_categorias')

    categorias = Categoria.objects.all().order_by('nombre')

    return render(
        request,
        'catalogo/categorias.html',
        {
            'categorias': categorias,
            'nombre_categoria': nombre if request.method == 'POST' else '',
            'descripcion_categoria': descripcion if request.method == 'POST' else '',
        }
    )
