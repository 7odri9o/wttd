from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


def make_validated_form(**kwargs):
    valid = dict(name='Nome Sobrenome', cpf='12345678901',
                email='nome.sobrenome@email.com.br', phone='987654321')
    data = dict(valid, **kwargs)
    form = SubscriptionForm(data)
    form.is_valid()
    return form


class SubscriptionFormTest(TestCase):
    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = SubscriptionForm()
        expected = ["name", "cpf", "email", "phone"]
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digits(self):
        """CPF must only accept digits"""
        form = make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_name_must_be_capitalized(self):
        """Name must be capitalized"""
        # NOME sobrenome -> Nome Sobrenome
        form = make_validated_form(name='NOME sobrenome')
        self.assertEqual('Nome Sobrenome', form.cleaned_data['name'])

    def test_cpf_has_11_digits(self):
        """CPF must have 11 digitis."""
        form = make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_phone_is_optional(self):
        """Phone is optional"""
        form = make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        """Email and phone are optional, but one must be informed."""
        form = make_validated_form(email='', phone='')
        self.assertListEqual(['__all__'], list(form.errors))

    def test_email_is_optional(self):
        """Email is optional"""
        form = make_validated_form(email='')
        self.assertFalse(form.errors)

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)
