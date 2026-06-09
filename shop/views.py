from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, F
from django.utils import timezone

from .models import Product, Category, Deal, Feedback


def _active_deals():
    now = timezone.now()
    return Deal.objects.filter(
        is_active=True,
        starts_at__lte=now,
        ends_at__gte=now,
    ).prefetch_related('products')


def home(request):
    featured = Product.objects.filter(is_featured=True, in_stock=True)[:6]
    trending = Product.objects.filter(is_trending=True, in_stock=True)[:4]
    categories = Category.objects.annotate(count=Count('products'))
    active_deals = _active_deals()[:3]
    spotlight_deal = active_deals.first()
    deal_products = Product.objects.filter(
        in_stock=True,
        old_price__isnull=False,
        old_price__gt=F('price'),
    )[:4]
    return render(request, 'shop/home.html', {
        'featured_products': featured,
        'trending_products': trending,
        'categories': categories,
        'active_deals': active_deals,
        'spotlight_deal': spotlight_deal,
        'deal_products': deal_products,
    })


def deals(request):
    active_deals = _active_deals()
    on_sale = Product.objects.filter(
        in_stock=True,
        old_price__isnull=False,
        old_price__gt=F('price'),
    ).select_related('category')
    return render(request, 'shop/deals.html', {
        'active_deals': active_deals,
        'on_sale_products': on_sale,
        'spotlight_deal': active_deals.first(),
    })


def catalog(request):
    products = Product.objects.select_related('category')
    categories = Category.objects.annotate(count=Count('products'))
    search_query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(cpu__icontains=search_query) |
            Q(gpu__icontains=search_query)
        )
    if selected_category and selected_category != 'all':
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


BUILDER_STEPS = ['cpu', 'mobo', 'gpu', 'ram', 'storage', 'psu', 'cooler', 'case']


def builder(request):
    builder_products = Product.objects.filter(
        is_builder_part=True,
        in_stock=True,
    ).exclude(component_type='').order_by('component_type', 'price')

    parts = {step: [] for step in BUILDER_STEPS}
    for product in builder_products:
        if product.component_type in parts:
            parts[product.component_type].append(product)

    return render(request, 'shop/builder.html', {'parts': parts})


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
