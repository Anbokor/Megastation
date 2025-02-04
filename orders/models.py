from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User

class Order(models.Model):
    """
    Order model:
    - Contains order information and delivery details
    - Links to user if authenticated
    - Tracks order status
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'En proceso'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Usuario'
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Nombre'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Apellido'
    )
    email = models.EmailField(
        verbose_name='Correo electrónico'
    )
    address = models.CharField(
        max_length=250,
        verbose_name='Dirección'
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name='Código postal'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Ciudad'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Estado'
    )
    note = models.TextField(
        blank=True,
        verbose_name='Nota adicional'
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'Pedido {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    """
    OrderItem model:
    - Links products to orders
    - Stores quantity and price at time of purchase
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Pedido'
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='Producto'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Cantidad'
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity