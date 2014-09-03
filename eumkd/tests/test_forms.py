from unittest.mock import Mock, patch
from eumkd.forms import EumkdSearchForm
from eumkd.models import Resource
import unittest
from django.conf import settings
from django import forms
from eumkd.forms import EumkdCreateForm
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.test import TestCase
from eumkd.models import UPLOAD_DIR, ResourceType
from eumkd.forms import ERROR_ONE_FIELD_IS_REQUIRED
from tdata.models import Discipline, Specialty
from eumkd.tests.factories import ResourceFactory


class EumkdSearchFormTest(TestCase):

    def test_find_resources_returns_list_of_Resource(self):
        res = ResourceFactory.create(
            number='00001', resource_type=ResourceType.objects.create()
        )
        form = EumkdSearchForm({'number': '00001'})
        form.is_valid()
        resources = form.find_resources()

        self.assertEqual(res, resources.first())

    def test_can_have_field_number(self):
        form = EumkdSearchForm()
        self.assertIsNotNone(form.fields['number'])  # should not raise

    def test_can_have_discipline_field(self):
        form = EumkdSearchForm()
        self.assertIsNotNone(form.fields['discipline'])  # should not raise

    def test_can_have_specialty_field(self):
        form = EumkdSearchForm()
        self.assertIsNotNone(form.fields['specialty'])  # should not raise

    def test_validate_is_valid_if_one_attribute_exist(self):
        form = EumkdSearchForm({})
        form.is_valid()
        self.assertIn(ERROR_ONE_FIELD_IS_REQUIRED, form.errors['number'])  # should not raise

    def test_number_is_not_required(self):
        self.assertFalse(EumkdSearchForm().fields['number'].required)  # should not raise

    def test_specialty_is_not_required(self):
        self.assertFalse(EumkdSearchForm().fields['specialty'].required)  # should not raise

    def test_discipline_is_not_required(self):
        self.assertFalse(EumkdSearchForm().fields['discipline'].required)  # should not raise