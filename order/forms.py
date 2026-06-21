from django import forms
from django.forms.models import inlineformset_factory
from django.db.models import Q
from order.models import Order, OrderItem
from reservations.models import Table


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_table_id = getattr(self.instance.table, 'id', None) if self.instance else None
        self.fields['table'].queryset = Table.objects.filter(Q(is_active=True)|Q(id=current_table_id))
        self.fields['table'].empty_label = '-- Stolni Tanlang --'


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['food_item', 'quantity']

OrderFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form = OrderItemForm,
    extra=2,
    can_order=True
)





