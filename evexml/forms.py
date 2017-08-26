from django import forms
from django.forms.fields import IntegerField, CharField

import evelink.account


class AddAPIForm(forms.Form):
    keyID = IntegerField()
    vCode = CharField(max_length=64, min_length=1)

    def clean(self):
        self._clean()
        return super(AddAPIForm, self).clean()

    def _clean(self):
        """Check the access mask and characters of the supplied keypair.

        """
        api_key = (self.cleaned_data['keyID'], self.cleaned_data['vCode'])
        api = evelink.api.API(api_key=api_key)
        account = evelink.account.Account(api)
        try:
            key_info = account.key_info().result
        except evelink.api.APIError as error:
            self.add_error(None, error.message)
            return

        if key_info['type'] != 'account':
            self.add_error(None, 'The API key should select Character: All')
