from django.db import models


class APIKeyPair(models.Model):
    key_id = models.IntegerField(verbose_name=' keyID')
    v_code = models.CharField(
        verbose_name=' vCode',
        max_length=64
    )
    is_valid = models.BooleanField(blank=False, default=True)

    class Meta:
        unique_together = ('key_id', 'v_code')
