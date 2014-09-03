import unittest
from unittest.mock import Mock, patch
from django.core.urlresolvers import reverse
from tdata.models import Specialty, Discipline
from eumkd.models import Resource, ResourceType
from eumkd.tests.factories import ResourceFactory

import os
TESTS_UPLOAD_DIR = os.path.join('eumkd', 'tests', 'files')


class ResourceTest(unittest.TestCase):

    def test_can_have_number(self):
        Resource(number='00001')  # should not raise

    def test_can_have_title(self):
        Resource(title='Новый ресурс')  # should not raise

    def test_can_have_file(self):
        Resource(file=Mock())  # should not raise

    def test_can_have_front_file(self):
        Resource(front_file=Mock())  # should not raise

    def test_absolute_url_return_view_url(self):
        res = ResourceFactory.create(title='Новый ресурс')
        self.assertEqual(reverse('eumkd_create'), res.get_absolute_url())

    def test_can_have_discipline(self):
        Resource(discipline=Discipline.objects.first())  # should not raise

    def test_can_have_specialty(self):
        Resource(specialty=Specialty.objects.first())  # should not raise

    def test_can_have_type(self):
        Resource(specialty=ResourceType.objects.first())  # should not raise


class ResourceTypeTest(unittest.TestCase):

    def test_can_have_name(self):
        ResourceType(name='Имя типа')  # should not raise

    def test_can_have_public(self):
        ResourceType(public=True)  # should not raise

    def test_can_have_available(self):
        ResourceType(available=False)  # should not raise

    def test_converts_to_string(self):
        res_type = ResourceType.objects.create(name='Новый тип ресурса')
        self.assertEqual(res_type.name, res_type.__str__())
