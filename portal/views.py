from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from django.conf import settings

from shop.models import Product, Category, Review, Feedback
from .forms import ProductForm, UserEditForm, ReviewForm, FeedbackStatusForm
from .decorators import staff_required


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('portal:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}.')
            return redirect('portal:dashboard')
        messages.error(request, 'Invalid credentials or insufficient permissions.')

    return render(request, 'portal/login.html', {'title': 'Admin Login | Overclock Admin Portal'})


def admin_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('portal:login')


@staff_required
def dashboard(request):
    context = {
        'title': 'Control Center | Overclock Admin Portal',
        'product_count': Product.objects.count(),
        'user_count': User.objects.count(),
        'review_count': Review.objects.count(),
        'pending_reviews': Review.objects.filter(is_approved=False).count(),
        'feedback_count': Feedback.objects.count(),
        'new_feedback': Feedback.objects.filter(status='new').count(),
        'low_stock': Product.objects.filter(stock__lte=5, in_stock=True).count(),
        'recent_reviews': Review.objects.select_related('product')[:5],
        'recent_feedback': Feedback.objects.all()[:5],
        'recent_products': Product.objects.select_related('category').order_by('-updated_at')[:5],
        'pcshop_url': settings.PCSHOP_URL,
    }
    return render(request, 'portal/dashboard.html', context)


@staff_required
def product_list(request):
    search = request.GET.get('q', '')
    category = request.GET.get('category', '')
    products = Product.objects.select_related('category')

    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(slug__icontains=search)
        )
    if category:
        products = products.filter(category__id_key=category)

    context = {
        'title': 'Products | Overclock Admin Portal',
        'products': products,
        'categories': Category.objects.all(),
        'search': search,
        'selected_category': category,
    }
    return render(request, 'portal/products/list.html', context)


@staff_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('portal:product_list')
    else:
        form = ProductForm()

    return render(request, 'portal/products/form.html', {
        'title': 'Add Product | Overclock Admin Portal',
        'form': form,
        'is_edit': False,
    })


@staff_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{product.name}" updated successfully.')
            return redirect('portal:product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'portal/products/form.html', {
        'title': f'Edit {product.name} | Overclock Admin Portal',
        'form': form,
        'product': product,
        'is_edit': True,
    })


@staff_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect('portal:product_list')

    return render(request, 'portal/products/delete.html', {
        'title': f'Delete {product.name} | Overclock Admin Portal',
        'product': product,
    })


@staff_required
def user_list(request):
    search = request.GET.get('q', '')
    users = User.objects.annotate(review_count=Count('reviews'))

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    context = {
        'title': 'Users | Overclock Admin Portal',
        'users': users,
        'search': search,
    }
    return render(request, 'portal/users/list.html', context)


@staff_required
def user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{user_obj.username}" updated.')
            return redirect('portal:user_list')
    else:
        form = UserEditForm(instance=user_obj)

    return render(request, 'portal/users/form.html', {
        'title': f'Edit User {user_obj.username} | Overclock Admin Portal',
        'form': form,
        'user_obj': user_obj,
        'reviews': Review.objects.filter(user=user_obj).select_related('product')[:10],
        'feedbacks': Feedback.objects.filter(user=user_obj)[:10],
    })


@staff_required
def review_list(request):
    status = request.GET.get('status', 'all')
    selected_category = request.GET.get('category', 'all')
    selected_source = request.GET.get('source', 'all')

    reviews = Review.objects.select_related('product', 'user')

    if status == 'pending':
        reviews = reviews.filter(is_approved=False)
    elif status == 'approved':
        reviews = reviews.filter(is_approved=True)

    if selected_category != 'all':
        reviews = reviews.filter(category=selected_category)
        
    if selected_source != 'all':
        reviews = reviews.filter(source=selected_source)

    # Categories list for choices
    categories = Review.CATEGORY_CHOICES
    sources = Review.SOURCE_CHOICES

    # Calculate breakdowns for categorized overview
    category_stats = []
    total_reviews = Review.objects.count()
    
    for cat_slug, cat_name in categories:
        count = Review.objects.filter(category=cat_slug).count()
        percentage = (count / total_reviews * 100) if total_reviews else 0
        category_stats.append({
            'slug': cat_slug,
            'name': cat_name,
            'count': count,
            'percentage': round(percentage, 1)
        })

    source_stats = []
    for src_slug, src_name in sources:
        count = Review.objects.filter(source=src_slug).count()
        percentage = (count / total_reviews * 100) if total_reviews else 0
        source_stats.append({
            'slug': src_slug,
            'name': src_name,
            'count': count,
            'percentage': round(percentage, 1)
        })

    context = {
        'title': 'Reviews | Overclock Admin Portal',
        'reviews': reviews,
        'status': status,
        'categories': categories,
        'sources': sources,
        'selected_category': selected_category,
        'selected_source': selected_source,
        'category_stats': category_stats,
        'source_stats': source_stats,
        'total_reviews': total_reviews,
    }
    return render(request, 'portal/reviews/list.html', context)


@staff_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            _update_product_rating(review.product)
            messages.success(request, 'Review updated.')
            return redirect('portal:review_list')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'portal/reviews/form.html', {
        'title': 'Edit Review | Overclock Admin Portal',
        'form': form,
        'review': review,
    })


@staff_required
def review_toggle_approve(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.is_approved = not review.is_approved
        review.save()
        _update_product_rating(review.product)
        status = 'approved' if review.is_approved else 'unapproved'
        messages.success(request, f'Review {status}.')
    return redirect('portal:review_list')


@staff_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    product = review.product
    if request.method == 'POST':
        review.delete()
        _update_product_rating(product)
        messages.success(request, 'Review deleted.')
        return redirect('portal:review_list')

    return render(request, 'portal/reviews/delete.html', {
        'title': 'Delete Review | Overclock Admin Portal',
        'review': review,
    })


@staff_required
def feedback_list(request):
    status = request.GET.get('status', 'all')
    feedbacks = Feedback.objects.select_related('user')

    if status != 'all':
        feedbacks = feedbacks.filter(status=status)

    context = {
        'title': 'Feedback | Overclock Admin Portal',
        'feedbacks': feedbacks,
        'status': status,
    }
    return render(request, 'portal/feedback/list.html', context)


@staff_required
def feedback_detail(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if request.method == 'POST':
        form = FeedbackStatusForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback status updated.')
            return redirect('portal:feedback_list')
    else:
        form = FeedbackStatusForm(instance=feedback)

    return render(request, 'portal/feedback/detail.html', {
        'title': f'Feedback: {feedback.subject} | Overclock Admin Portal',
        'feedback': feedback,
        'form': form,
    })


@staff_required
def feedback_delete(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback deleted.')
        return redirect('portal:feedback_list')

    return render(request, 'portal/feedback/delete.html', {
        'title': 'Delete Feedback | Overclock Admin Portal',
        'feedback': feedback,
    })


def _update_product_rating(product):
    approved = product.reviews.filter(is_approved=True)
    count = approved.count()
    if count:
        avg = sum(r.rating for r in approved) / count
        product.rating = round(avg, 1)
        product.reviews_count = count
    else:
        product.rating = 0
        product.reviews_count = 0
    product.save(update_fields=['rating', 'reviews_count'])
