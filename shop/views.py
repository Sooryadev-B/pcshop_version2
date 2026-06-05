from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Product, Category, Feedback


def home(request):
    featured = Product.objects.filter(is_featured=True, in_stock=True)[:6]
    trending = Product.objects.filter(is_trending=True, in_stock=True)[:4]
    categories = Category.objects.all()
    return render(request, 'shop/home.html', {
        'featured_products': featured,
        'trending_products': trending,
        'categories': categories,
    })


def catalog(request):
    products = Product.objects.select_related('category')
    categories = Category.objects.all()
    search_query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(cpu__icontains=search_query) |
            Q(gpu__icontains=search_query)
        )
    if selected_category:
        products = products.filter(category__id_key=selected_category)

    return render(request, 'shop/catalog.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.filter(is_approved=True)
    related = Product.objects.filter(category=product.category, in_stock=True).exclude(pk=product.pk)[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related_products': related,
    })


def cart(request):
    return render(request, 'shop/cart.html')


def checkout(request):
    return render(request, 'shop/checkout.html', {'total': 0})


def builder(request):
    categories = Category.objects.prefetch_related('products').all()
    components = Product.objects.filter(in_stock=True)
    return render(request, 'shop/builder.html', {
        'categories': categories,
        'components': components,
    })


@login_required
def dashboard(request):
    return render(request, 'shop/dashboard.html', {
        'order_history': [],
        'saved_builds': [],
        'wishlist': [],
    })


def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and email and subject and message_text:
            Feedback.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                subject=subject,
                message=message_text,
            )
            messages.success(request, 'Feedback transmitted successfully. Our team will review it shortly.')
            return redirect('shop:feedback')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'shop/feedback.html')
