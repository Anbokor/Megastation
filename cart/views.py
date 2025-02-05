from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from catalog.models import Product, SalesPoint
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart or update its quantity.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)
    sales_point_id = request.session.get('selected_sales_point')
    sales_point = get_object_or_404(SalesPoint, id=sales_point_id) if sales_point_id else None

    if not sales_point:
        messages.error(request, 'Por favor, selecciona un punto de venta antes de añadir productos al carrito.')
        return redirect('catalog:product_list')

    form = CartAddProductForm(request.POST, product=product, sales_point=sales_point)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override'],
            sales_point=sales_point
        )
        messages.success(request, f'"{product.name}" ha sido añadido al carrito.')
    else:
        messages.error(request, 'No se pudo añadir el producto al carrito.')

    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    """
    Remove a product from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'"{product.name}" ha sido eliminado del carrito.')
    return redirect('cart:cart_detail')

def cart_detail(request):
    """
    Display the cart details.
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True
            }
        )
    return render(request, 'cart/detail.html', {'cart': cart})