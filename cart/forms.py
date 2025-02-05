from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product, Stock

class CartAddProductForm(forms.Form):
    """
    Form for adding products to cart
    """
    quantity = forms.TypedChoiceField(
        choices=[],  # Choices will be set dynamically in __init__
        coerce=int,
        label='Cantidad'
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        self.sales_point = kwargs.pop('sales_point', None)
        super().__init__(*args, **kwargs)

        if self.product and self.sales_point:
            try:
                stock = Stock.objects.get(product=self.product, sales_point=self.sales_point)
                max_quantity = min(stock.quantity, 20)  # Limit to 20 or available stock
                self.fields['quantity'].choices = [(i, str(i)) for i in range(1, max_quantity + 1)]
            except Stock.DoesNotExist:
                self.fields['quantity'].choices = [(0, 'No disponible')]

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if self.product and self.sales_point:
            try:
                stock = Stock.objects.get(product=self.product, sales_point=self.sales_point)
                if quantity > stock.quantity:
                    raise ValidationError('No hay suficiente stock disponible.')
            except Stock.DoesNotExist:
                raise ValidationError('El producto no está disponible en este punto de venta.')
        return quantity