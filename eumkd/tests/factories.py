import factory
from tdata.models import (Specialty, Discipline)
from eumkd.models import ResourceType


class ResourceTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceType
    id = factory.Sequence(lambda n: n)
    name = "Имя типа"


class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'eumkd.Resource'

    title = 'Какое-то имя'
    number = '000001'
    discipline = Discipline.objects.first()
    specialty = Specialty.objects.first()

    resource_type = factory.SubFactory(ResourceTypeFactory)