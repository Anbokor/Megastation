from django.shortcuts import render, get_object_or_404
from .models import Category, Product, SalesPoint, Stock
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    """
    Display list of products, optionally filtered by category and sales point
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    sales_points = SalesPoint.objects.filter(is_active=True)
    selected_sales_point = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Filter by sales point if selected
    sales_point_id = request.GET.get('sales_point')
    if sales_point_id:
        selected_sales_point = get_object_or_404(SalesPoint, id=sales_point_id)
        products = products.filter(stocks__sales_point=selected_sales_point,
                                   stocks__quantity__gt=0)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'sales_points': sales_points,
        'selected_sales_point': selected_sales_point
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, product_slug):
    """
    Display single product details with stock information
    """
    product = get_object_or_404(Product, slug=product_slug, is_available=True)
    sales_points = SalesPoint.objects.filter(is_active=True)

    # Add cart form
    cart_add_form = CartAddProductForm()  # добавьте эту строку

    # Get stock information for each sales point
    stock_info = []
    for point in sales_points:
        stock_info.append({
            'sales_point': point,
            'quantity': point.get_stock_for_product(product)
        })

    context = {
        'product': product,
        'stock_info': stock_info,
        'cart_add_form': cart_add_form,
    }
    return render(request, 'catalog/product_detail.html', context)