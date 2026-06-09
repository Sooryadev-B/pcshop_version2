from django.contrib import admin
from .models import Product, Category, Deal, Review, Feedback


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'component_type', 'price', 'is_builder_part', 'in_stock')
    list_filter = ('category', 'component_type', 'is_builder_part', 'in_stock')
    search_fields = ('name', 'slug')


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_label', 'starts_at', 'ends_at', 'is_active')
    filter_horizontal = ('products',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Feedback)
