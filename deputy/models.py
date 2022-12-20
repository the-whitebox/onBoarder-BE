from django.db import models
from django.conf import settings


class DeputyBaseModel(models.Model):

    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_createdby', null=True, blank=True,
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='%(class)s_modifiedby', null=True, blank=True,
                                    on_delete=models.CASCADE)

    class Meta:
        abstract = True