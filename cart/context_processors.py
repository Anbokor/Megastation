from .cart import Cart

def cart_processor(request):
    """
    Context processor for cart
    Makes cart available in all templates
    """
    return {'cart': Cart(request)}