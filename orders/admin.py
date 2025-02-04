from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """
    Inline view for order items
    """
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin view for orders
    """
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
        'status',
        'created',
        'updated'
    ]
    list_filter = ['status', 'created', 'updated']
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'address'
    ]
    inlines = [OrderItemInline]
    list_per_page = 20

    fieldsets = (
        ('Información personal', {
            'fields': (
                'user',
                ('first_name', 'last_name'),
                'email',
            )
        }),
        ('Dirección de envío', {
            'fields': (
                'address',
                ('postal_code', 'city'),
            )
        }),
        ('Estado del pedido', {
            'fields': (
                'status',
                'note',
            )
        }),
    )