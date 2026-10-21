from django.shortcuts import render, redirect
from .models import Category, MenuItem, BookTable


# Create your views here.
def home(request):
    categories = Category.objects.all()

    # Satışda olan bütün məhsulları çəkirik
    # .prefetch_related('categories') - çoxdan-çoxa əlaqələrdə performansı artırır
    menu_items = MenuItem.objects.filter(is_available=True).prefetch_related('categories')

    # İndeks səhifəsində də istifadəçi rezervasiya göndərə bilər (homepage formu varsa)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email') or ''
        date = request.POST.get('date')
        time = request.POST.get('time')
        persons = request.POST.get('persons') or 2
        message = request.POST.get('message') or ''

        # Try to convert persons to int
        try:
            persons = int(persons)
        except (TypeError, ValueError):
            persons = 2

        # Create reservation
        BookTable.objects.create(
            name=name,
            phone=phone,
            email=email,
            date=date,
            time=time,
            persons=persons,
            message=message,
        )
        # Redirect back with success flag
        return redirect(request.path + '?success=1')

    context = {
        'categories': categories,
        'menu_items': menu_items,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')

def menu(request):
    categories = Category.objects.all()

    # Satışda olan bütün məhsulları çəkirik
    # .prefetch_related('categories') - çoxdan-çoxa əlaqələrdə performansı artırır
    menu_items = MenuItem.objects.filter(is_available=True).prefetch_related('categories')

    context = {
        'categories': categories,
        'menu_items': menu_items,
    }
    return render(request, 'menu.html', context)
def book(request):
    # Form submission handling
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email') or ''
        date = request.POST.get('date')
        time = request.POST.get('time')
        persons = request.POST.get('persons') or 2
        message = request.POST.get('message') or ''

        # Create reservation
        BookTable.objects.create(
            name=name,
            phone=phone,
            email=email,
            date=date,
            time=time,
            persons=persons,
            message=message,
        )
        # Redirect back with success flag
        from django.shortcuts import redirect
        return redirect(request.path + '?success=1')

    # GET: render form
    return render(request, 'book.html', {'request': request})
    
