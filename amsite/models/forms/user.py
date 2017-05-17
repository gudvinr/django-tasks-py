from django.forms import ModelForm, CharField, EmailField
from .. import User


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'region', 'phone']

    action = CharField(max_length=16, required=False)
    password = CharField(max_length=128, required=False)
    password_confirm = CharField(max_length=128, required=False)
    email = EmailField(required=False)
