from .base import FunctionalTest
from .search_page import SearchPage
from eumkd.models import Resource, ResourceType


class SearchTest(FunctionalTest):

    def test_can_search_resource(self):
        # prepend to test on server side
        self.load_data_for_test_can_search_resource()

        # He goes on search_page
        search_page = SearchPage(self)
        search_page.go_to_page()

        # He fills out number of resource and send form
        number_box = search_page.get_number_box()
        self.assertEqual(
            number_box.get_attribute('placeholder'),
            'Номер'
        )
        number_box.send_keys('00001')
        search_page.get_submit_button().submit()

        # Resource appeared in table
        rows = search_page.get_list_table_rows()
        self.assertEqual(len(rows), 1)

        # He clears all boxes
        search_page.clear_all_boxes()
        # He fills out discipline and send form
        search_page.fill_out_discipline_box('Физика')
        search_page.get_submit_button().submit()

        # Resource appeared in table
        rows = search_page.get_list_table_rows()
        self.assertEqual(len(rows), 1)

        # He clears all boxes
        search_page.clear_all_boxes()
        # He fills out specialty and send form
        search_page.fill_out_specialty_box('081100 Государственное и муниципальное управление')
        search_page.get_submit_button().submit()

        # Resource appeared in table
        rows = search_page.get_list_table_rows()
        self.assertEqual(len(rows), 1)

    def load_data_for_test_can_search_resource(self):
        from tdata.models import Discipline, Specialty
        res_type = ResourceType.objects.create()

        Resource.objects.create(title="Ресурс для номера", number='00001', resource_type=res_type)

        discipline = Discipline.objects.get(Name="Физика")
        Resource.objects.create(title="Ресурс для физики", number='00002', discipline=discipline,
                                resource_type=res_type)

        specialty = Specialty.objects.get(Name__startswith="Государственное и муниципальное управление")
        Resource.objects.create(title="Ресурс для специальности", number='00002', specialty=specialty,
                                resource_type=res_type)