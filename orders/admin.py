from django.contrib import admin

from .emails import send_order_status_update_email
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
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

    def save_model(self, request, obj, form, change):
        """
        Override save_model to send email notification when order status changes
        """
        if change:  # If this is an update
            old_obj = self.model.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:  # If status has changed
                super().save_model(request, obj, form, change)
                send_order_status_update_email(obj, request)
            else:
                super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)
