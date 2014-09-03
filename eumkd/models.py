from django.db import models
from django.core.urlresolvers import reverse
UPLOAD_DIR = 'uploads'


class ResourceType(models.Model):
    """
    Class that available types of resources

    Attributes:
        name        The name of type of the resource
        public      Determines that it is public type of resources
        available   Determines that it is available for changes type of resource
    """
    name = models.CharField(max_length=64)
    public = models.BooleanField(default=False)
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Resource(models.Model):
    """
    Class that present resource of informational system

    Attributes:
        number        The number of resource (optional)
        title         The title of resource
        file          The file of resource
        front_file    The front file (title file) of resource
        discipline    The discipline that will use this resource
        specialty     The specialty that will use this resource
        resource_type The type of resource

    """
    number = models.CharField('Номер', max_length=16)
    title = models.CharField('Заголовок', max_length=64)
    file = models.FileField('Файл', upload_to=UPLOAD_DIR)
    front_file = models.FileField('Титул', upload_to=UPLOAD_DIR)

    discipline = models.CharField(max_length=64)
    specialty = models.CharField(max_length=64)
    resource_type = models.ForeignKey(ResourceType)

    @staticmethod
    def get_absolute_url():
        return reverse('eumkd_create')