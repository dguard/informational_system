from django.test import TestCase
from django.http import HttpRequest
import unittest
from unittest import skip
from unittest.mock import Mock, patch
from eumkd.views import search
from eumkd.forms import EumkdSearchForm
from .mixins import AssertMatchesMixin
from eumkd.forms import ERROR_ONE_FIELD_IS_REQUIRED
from tdata.models import Discipline

from eumkd.tests.factories import ResourceFactory


class SearchTest(TestCase, AssertMatchesMixin):

    def test_renders_correct_template(self):
        response = self.client.get('/eumkd/search/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_passes_form_to_template(self):
        response = self.client.get('/eumkd/search/')
        self.assertIsInstance(response.context['form'], EumkdSearchForm)

    def test_passes_resources_to_template(self):
        response = self.client.get('/eumkd/search/')
        self.assertIsNotNone(response.context['resources'])

    def test_renders_resources_on_template(self):
        res1 = ResourceFactory.create(number='0000001')
        res2 = ResourceFactory.create(number='0000002')

        response = self.client.get('/eumkd/search/', {'number': '0000001'})
        self.assertContains(response, res1.number)
        self.assertNotContains(response, res2.number)

    def test_does_not_render_resources_on_template_if_invalid_form(self):
        res1 = ResourceFactory.create(number='0000001')
        res2 = ResourceFactory.create(number='0000002')
        
        response = self.client.get('/eumkd/search/')
        self.assertNotContains(response, res1.number)
        self.assertNotContains(response, res2.number)

    def test_renders_empty_message_if_no_resources(self):
        response = self.client.get('/eumkd/search/')
        self.assertContains(response, 'Ничего не найдено')

    def test_render_errors_on_submit_if_invalid(self):
        response = self.client.get('/eumkd/search/', {'number': ''})
        self.assertContains(response, ERROR_ONE_FIELD_IS_REQUIRED)

    def test_does_not_render_errors_without_submit_if_invalid(self):
        response = self.client.get('/eumkd/search/')
        self.assertNotContains(response, 'This field is required')

    def test_render_name_as_value_if_discipline_is_specified(self):
        discipline = Discipline.objects.first()
        response = self.client.get('/eumkd/search/', {
            'discipline': discipline.Id
        })
        self.assert_matches(response, ['input', 'id="id_discipline"', 'value="{}"'.format(discipline.Name)])

    def test_form_contains_discipline_field(self):
        response = self.client.get('/eumkd/search/')
        self.assertContains(response, 'id_discipline')

    def test_form_contains_specialty_field(self):
        response = self.client.get('/eumkd/search/')
        self.assertContains(response, 'id_specialty')


@patch('eumkd.views.EumkdSearchForm')
class SearchUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.GET['number'] = '00001'
        self.request.method = 'GET'

    def test_passes_get_data_to_form(self, mockForm):
        search(self.request)
        mockForm.assert_called_once_with(self.request.GET)

    def test_form_uses_find_resources_if_form_valid(self, mockForm):
        mock_form = mockForm.return_value
        mock_form.is_valid.return_value = True

        search(self.request)
        self.assertTrue(mock_form.is_valid.called)
        self.assertTrue(mock_form.find_resources.called)

    def test_form_does_not_use_find_resources_if_form_invalid(self, mockForm):
        mock_form = mockForm.return_value
        mock_form.is_valid.return_value = False

        search(self.request)
        self.assertTrue(mock_form.is_valid.called)
        self.assertFalse(mock_form.find_resources.called)