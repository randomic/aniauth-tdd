import evelink.account
from django.forms.models import ModelForm

from evexml.models import APIKeyPair


class AddAPIForm(ModelForm):
    class Meta:
        model = APIKeyPair
        fields = '__all__'

    def full_clean(self):
        """Check the access mask and characters of the supplied keypair.

        """
        super(AddAPIForm, self).full_clean()
        key_id = self.cleaned_data.get('key_id')
        v_code = self.cleaned_data.get('v_code')
        if not (key_id and v_code):
            return

        api = evelink.api.API(api_key=(key_id, v_code))
        account = evelink.account.Account(api)
        try:
            self.key_info = account.key_info().result
        except evelink.api.APIError as error:
            self.add_error(None, error.message)
            return

        self.save()

        if self.key_info['type'] != 'account':
            self.add_error(None, 'The API key should select Character: All')
        if self.key_info['access_mask'] != 4294967295:
            self.add_error(None, 'The API key should have full access')
        if self.key_info['expire_ts']:
            self.add_error(None, 'The API key should have no expiry checked')
