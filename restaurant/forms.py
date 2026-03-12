from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from .models import Food

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        exclude = ['added_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('name_of_food', css_class="form-control mb-3", placeholder="Ovqat nomi"),
            Field('description', css_class="form-control mb-3", placeholder="Tavsif"),
            Field('type', css_class="form-control mb-3"),
            Row(
                Column(Field('price', css_class="form-control"), css_class="col-md-6"),
                Column(Field('image', css_class="form-control"), css_class="col-md-6"),
            ),
            Field('published', css_class="form-check-input mt-3"),
        )