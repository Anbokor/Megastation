from django.db import models
from django.utils.text import slugify
import os
from django.urls import reverse

def get_default_image_path():
    """
    Returns the path to default product image
    """
    return 'products/default/default.jpg'

def product_image_path(instance, filename):
    """
    Generate file path for product images
    Format: products/<category_slug>/<product_slug>/<filename>
    """
    ext = filename.split('.')[-1]
    new_filename = f"{instance.slug}.{ext}"
    return os.path.join('products', instance.category.slug, instance.slug, new_filename)

class Category(models.Model):
    """
    Product category model:
    - Contains basic category information
    - Has one default image
    - Auto-generates slug from name
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre de categoría'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    image = models.ImageField(
        upload_to='categories',
        default=get_default_image_path,
        verbose_name='Imagen'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override save method to:
        - Auto-generate slug from name if not provided
        - Handle image deletion on update
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product_list_by_category', args=[self.slug])

class Product(models.Model):
    """
    Product model:
    - Links to Category
    - Contains product details and pricing
    - Handles image storage and default image
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Categoría'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Nombre del producto'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL'
    )
    description = models.TextField(
        verbose_name='Descripción'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio'
    )
    image = models.ImageField(
        upload_to=product_image_path,
        default=get_default_image_path,
        verbose_name='Imagen'
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Disponible'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override save method to:
        - Auto-generate slug from name if not provided
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.slug])


class SalesPoint(models.Model):
    """
    Store/Sales point model:
    - Represents physical or virtual store locations
    - Contains contact and address information
    - Tracks active status
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre del punto de venta'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Dirección'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Teléfono'
    )
    email = models.EmailField(
        verbose_name='Correo electrónico'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )

    class Meta:
        verbose_name = 'Punto de venta'
        verbose_name_plural = 'Puntos de venta'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_stock_for_product(self, product):
        """
        Returns stock quantity for specific product
        """
        try:
            stock = self.stocks.get(product=product)
            return stock.quantity
        except Stock.DoesNotExist:
            return 0

class Stock(models.Model):
    """
    Stock model:
    - Links Products to SalesPoints
    - Tracks quantity of products at each location
    - Maintains history of updates
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stocks',
        verbose_name='Producto'
    )
    sales_point = models.ForeignKey(
        SalesPoint,
        on_delete=models.CASCADE,
        related_name='stocks',
        verbose_name='Punto de venta'
    )
    quantity = models.IntegerField(
        default=0,
        verbose_name='Cantidad'
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        unique_together = ('product', 'sales_point')
        ordering = ['product', 'sales_point']

    def __str__(self):
        return f"{self.product.name} - {self.sales_point.name}: {self.quantity}"