import phonenumbers as pn

from django.forms import ModelForm, CharField, IntegerField, EmailField, ValidationError
from django.utils.translation import ugettext_lazy as _

from .. import User

# TODO: this should be set to user country
PHONE_DEF_LC = 'RU'


def _phone_validator(phone: str):
    try:
        if not pn.is_valid_number(pn.parse(phone, PHONE_DEF_LC)):
            raise pn.NumberParseException(pn.NumberParseException.NOT_A_NUMBER, 'invalid')

    except pn.NumberParseException:
        raise ValidationError(_('Invalid phone number'), code='invalid')


def _action_validator(action: str):
    if action and action not in ['login', 'register']:
        raise ValidationError(_('Invalid action'), code='invalid')


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'region', 'phone']

    action = CharField(required=False, validators=[_action_validator])

    password = CharField(max_length=128, required=False)
    password_confirm = CharField(max_length=128, required=False)
    email = EmailField(required=False)

    phone = CharField(validators=[_phone_validator], required=False)
    age = IntegerField(min_value=12, max_value=228, required=False)

    def clean(self):
        '''
        Redefine default clean to normalize fields
        '''

        cleaned_data = super().clean()

        phone = cleaned_data.get('phone')

        if phone:
            cleaned_data['phone'] = pn.format_number(pn.parse(phone, PHONE_DEF_LC), pn.PhoneNumberFormat.E164)

        return cleaned_data
