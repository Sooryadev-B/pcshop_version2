from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    id_key = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id_key:
            self.id_key = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, blank=True, help_text='Static image filename without extension')
    image_upload = models.ImageField(upload_to='products/', null=True, blank=True)
    badge = models.CharField(max_length=50, blank=True)
    stock = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=True)
    # Specs
    cpu = models.CharField(max_length=200, blank=True)
    gpu = models.CharField(max_length=200, blank=True)
    ram = models.CharField(max_length=200, blank=True)
    storage = models.CharField(max_length=200, blank=True)
    mobo = models.CharField(max_length=200, blank=True)
    psu = models.CharField(max_length=200, blank=True)
    cooler = models.CharField(max_length=200, blank=True)
    case = models.CharField(max_length=200, blank=True)
    # Meta
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    reviews_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Review(models.Model):
    CATEGORY_CHOICES = [
        ('performance', 'Performance'),
        ('design', 'Design'),
        ('value', 'Value'),
        ('support', 'Support'),
        ('general', 'General'),
    ]
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('verified', 'Verified Purchase'),
        ('external', 'External'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    author_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='website')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author_name} on {self.product.name}'


class Feedback(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('resolved', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} — {self.name}'
