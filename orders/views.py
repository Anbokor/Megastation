from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cart.cart import Cart
from .emails import send_order_confirmation_email
from .forms import OrderCreateForm
from .models import OrderItem


@login_required
def order_create(request):
    """
    View for creating new orders
    Requires authentication
    """
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Clear the cart
            cart.clear()

            # Send confirmation email
            send_order_confirmation_email(order)

            return render(request,
                          'orders/order_created.html',
                          {'order': order})
    else:
        # Pre-fill form with user data if available
        initial_data = {}
        if request.user.first_name:
            initial_data['first_name'] = request.user.first_name
        if request.user.last_name:
            initial_data['last_name'] = request.user.last_name
        if request.user.email:
            initial_data['email'] = request.user.email

        form = OrderCreateForm(initial=initial_data)

    return render(request,
                  'orders/order_create.html',
                  {'cart': cart, 'form': form})


@login_required
def order_list(request):
    """
    View for displaying user's orders
    Requires authentication
    """
    orders = request.user.orders.all()
    return render(request,
                  'orders/order_list.html',
                  {'orders': orders})


@login_required
def order_detail(request, order_id):
    """
    View for displaying order details
    Requires authentication and order ownership
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request,
                  'orders/order_detail.html',
                  {'order': order})