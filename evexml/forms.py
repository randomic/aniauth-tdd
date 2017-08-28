import evelink.account
from django.forms.models import ModelForm

from evexml.models import APIKeyPair


class AddAPIForm(ModelForm):
    class Meta:
        model = APIKeyPair
        fields = '__all__'

    def clean(self):
        super(AddAPIForm, self).clean()
        self._clean()
        return self.cleaned_data

    def _clean(self):
        """Check the access mask and characters of the supplied keypair.

        """
        key_id = self.cleaned_data.get('key_id')
        v_code = self.cleaned_data.get('v_code')
        if not (key_id and v_code):
            return

        api = evelink.api.API(api_key=(key_id, v_code))
        account = evelink.account.Account(api)
        try:
            self.cleaned_data['key_info'] = account.key_info().result
        except evelink.api.APIError as error:
            self.add_error(None,
                           "API Error: %s (%s)" % (error.message, error.code))
            return

    def full_clean(self):
        super(AddAPIForm, self).full_clean()
        if not self.is_valid():
            return

        self.save()

        key_info = self.cleaned_data.get('key_info')
        if key_info['type'] != 'account':
            self.add_error(None, 'The API key should select Character: All')
        if key_info['access_mask'] != 4294967295:
            self.add_error(None, 'The API key should have full access')
        if key_info['expire_ts']:
            self.add_error(None, 'The API key should have no expiry checked')
