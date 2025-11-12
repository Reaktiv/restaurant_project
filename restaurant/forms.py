from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from .models import Food

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class FoodForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = Food
        fields = ['name_of_food', 'description', 'price', 'published', 'type', 'images']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Field('name_of_food', css_class="form-control mb-3", placeholder="Ovqat nomi kiriting"),
            Field('description', css_class="form-control mb-3", placeholder="Ovqat haqida qisqacha yozing"),
            Row(
                Column(Field('price', css_class="form-control"), css_class="col-md-6"),
                Column(Field('images', css_class="form-control"), css_class="col-md-6"),
            ),
            Field('published', css_class="form-check-input mt-3"),
        )