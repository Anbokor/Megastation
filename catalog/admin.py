from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, SalesPoint, Stock

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_preview', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Vista previa'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'image_preview', 'is_available']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Vista previa'

@admin.register(SalesPoint)
class SalesPointAdmin(admin.ModelAdmin):
    """
    Admin interface for SalesPoint model
    """
    list_display = ['name', 'address', 'phone', 'email', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'address', 'email']
    readonly_fields = ['created_at', 'updated_at']

class StockInline(admin.TabularInline):
    """
    Inline admin for Stock model to be used in Product and SalesPoint admin
    """
    model = Stock
    extra = 1

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """
    Admin interface for Stock model
    """
    list_display = ['product', 'sales_point', 'quantity', 'last_updated']
    list_filter = ['sales_point', 'last_updated']
    search_fields = ['product__name', 'sales_point__name']
    readonly_fields = ['last_updated']

# Add StockInline to Product and SalesPoint admin
ProductAdmin.inlines = [StockInline]
SalesPointAdmin.inlines = [StockInline]