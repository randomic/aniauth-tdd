from django.db import models


class APIKeyPair(models.Model):
    key_id = models.IntegerField(verbose_name='keyID')
    v_code = models.CharField(verbose_name='vCode', max_length=64)
