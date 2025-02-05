from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Main product list
    path('', views.product_list, name='product_list'),

    # Product list by category
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),

    # Product detail
    path('<slug:product_slug>/', views.product_detail, name='product_detail'),

    # Search products (optional)
    # path('search/', views.product_search, name='product_search'),
]