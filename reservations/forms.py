from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from reservations.models import Table, Reservations
from django.db.models import Q


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'capacity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('number', css_class="form-control mb-3", placeholder="Stol nomeri"),
            Field('capacity', css_class="form-control mb-3", placeholder="Stol sig'imi"),
        )


class ReservationsForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ['name', 'email', 'phone', 'table', 'number_of_guests', 'date', 'time', 'special_requests', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('users', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        is_edit = bool(self.instance.id)
        if is_edit:
            self.fields['table'].queryset = Table.objects.filter(
                Q(is_active=True)|Q(id=self.instance.table.id)
            ).order_by('number')
        else:
            self.fields['table'].queryset = Table.objects.filter(is_active=True).order_by('number')
        self.fields['table'].empty_label = "-- Stol tanlang --"

        core_layout = [
            Row(
                Column(Field('name', placeholder='Your Name', css_class='form-control'), css_class='col-md-4 mb-3'),
                Column(Field('email', placeholder='Your Email', css_class='form-control'), css_class='col-md-4 mb-3'),
                Column(Field('phone', placeholder='Your Phone', css_class='form-control'), css_class='col-md-4 mb-3'),
            ),
            Row(
                Column(Field('table', css_class='form-select'), css_class='col-12 mb-3'),
            ),
            Row(
                Column(Field('number_of_guests', placeholder='Number of guests', css_class='form-control'),
                       css_class='col-md-4 mb-3'),
                Column(Field('date', css_class='form-control date-input', id='id_date'), css_class='col-md-4 mb-3'),
                Column(Field('time', css_class='form-control time-input', id='id_time'), css_class='col-md-4 mb-3'),
            ),
            Row(
                Column(Field('special_requests', rows='4', placeholder='Special Requests (Optional)',
                             css_class='form-control'), css_class='col-12 mb-3'),
            ),
        ]

        user_role = getattr(user, 'role', None)
        is_edit = self.instance and self.instance.pk  # ← Asosiy tekshiruv

        if user and user_role in ['admin', 'manager'] and is_edit:
            core_layout.append(
                Row(
                    Column(Field('status', css_class='form-select'), css_class='col-12 mb-3'),
                )
            )
        else:
            if 'status' in self.fields:
                del self.fields['status']

        self.helper.layout = Layout(*core_layout)
