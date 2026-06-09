from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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
    COMPONENT_TYPES = [
        ('', 'Not a builder part'),
        ('cpu', 'Processor (CPU)'),
        ('mobo', 'Motherboard'),
        ('gpu', 'Graphics Card (GPU)'),
        ('ram', 'System Memory (RAM)'),
        ('storage', 'Storage (SSD)'),
        ('psu', 'Power Supply (PSU)'),
        ('cooler', 'CPU Cooler'),
        ('case', 'Chassis Case'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    component_type = models.CharField(
        max_length=20, choices=COMPONENT_TYPES, blank=True, default='',
        help_text='PC Builder slot — only used when "Show in PC Builder" is enabled',
    )
    is_builder_part = models.BooleanField(default=False, help_text='Include this product in the PC Builder')
    wattage = models.PositiveIntegerField(default=0, help_text='Power draw in watts (PSU = total capacity)')
    socket = models.CharField(max_length=50, blank=True, help_text='CPU/Motherboard socket, e.g. AM5, LGA1700')
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

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int((1 - float(self.price) / float(self.old_price)) * 100)
        return 0

    @property
    def is_on_sale(self):
        return bool(self.old_price and self.old_price > self.price)


class Deal(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    discount_label = models.CharField(max_length=50, blank=True, help_text='e.g. 15% OFF')
    badge = models.CharField(max_length=50, blank=True, help_text='e.g. FLASH SALE')
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, related_name='deals', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-starts_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_current(self):
        now = timezone.now()
        return self.is_active and self.starts_at <= now <= self.ends_at


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
