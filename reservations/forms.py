from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from reservations.models import Table, Reservations


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'capacity', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('number', css_class="form-control mb-3", placeholder="Stol nomeri"),
            Field('capacity', css_class="form-control mb-3", placeholder="Stol sig'imi"),
            Field('is_active', css_class="form-check-input mt-3"),
        )


class ReservationsForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ['name', 'email', 'phone', 'table', 'number_of_guests', 'date', 'time', 'special_requests']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            # 1-qator: Ism, Email, Telefon
            Row(
                Column(Field('name', placeholder='Your Name', css_class='form-control'), css_class='col-md-4 mb-3'),
                Column(Field('email', placeholder='Your Email', css_class='form-control'), css_class='col-md-4 mb-3'),
                Column(Field('phone', placeholder='Your Phone', css_class='form-control'), css_class='col-md-4 mb-3'),
            ),
            # 2-qator: Table tanlash (to'liq kenglik)
            Row(
                Column(Field('table', css_class='form-select'), css_class='col-12 mb-3'),
            ),
            # 3-qator: Mehmonlar soni, Sana, Vaqt
            Row(
                Column(Field('number_of_guests', placeholder='Number of guests', css_class='form-control'), css_class='col-md-4 mb-3'),
                Column(Field('date', css_class='form-control date-input', id='id_date'), css_class='col-md-4 mb-3'),
                Column(Field('time', css_class='form-control time-input', id='id_time'), css_class='col-md-4 mb-3'),
            ),
            # 4-qator: Maxsus istaklar
            Row(
                Column(Field('special_requests', rows='4', placeholder='Special Requests (Optional)', css_class='form-control'), css_class='col-12 mb-3'),
            ),
        )