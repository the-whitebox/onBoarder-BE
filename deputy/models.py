from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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

# class Document(DeputyBaseModel):
#     image = models.ImageField(upload_to='images/', blank=True, null=True)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

# class ENUMS(DeputyBaseModel):
#     name = models.CharField(max_length=450, null=True,blank=True)
#     reference_id = models.PositiveIntegerField()
#     group = models.CharField(max_length=255, null=True,blank=True)

#     def __str__(self):
#         return str(self.name)