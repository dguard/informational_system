from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from .base import wait_for, wait_js
from .base import BasePage


class SearchPage(BasePage):
    """
    Class that present available user's actions on search page

    Usage inside test:

    search_page = SearchPage(self)
    search_page.go_to_page()
    search_page.fill_out_discipline_box("Some discipline")
    """

    def go_to_page(self):
        self.test.browser.get(self.test.server_url + '/eumkd/search/')

    def get_number_box(self):
        return self.test.browser.find_element_by_id('id_number')

    def get_discipline_box(self):
        self.test.browser.find_element_by_css_selector('#s2id_id_discipline .select2-choice').click()
        return self.get_select2_input()

    def get_specialty_box(self):
        self.test.browser.find_element_by_css_selector('#s2id_id_specialty .select2-choice').click()
        return self.get_select2_input()

    def clear_discipline_box(self):
        box = self.get_discipline_box()
        box.clear()
        wait_js(lambda: box.send_keys(Keys.ESCAPE))
        wait_js(lambda: self.wait_while_select2_will_hidden())

    def clear_specialty_box(self):
        box = self.get_specialty_box()
        box.clear()
        wait_js(lambda: box.send_keys(Keys.ESCAPE))
        wait_js(lambda: self.wait_while_select2_will_hidden())

    def fill_out_discipline_box(self, text):
        box = self.get_discipline_box()
        box.send_keys(text)
        wait_js(lambda: box.send_keys(Keys.ENTER))
        wait_js(lambda: self.wait_while_select2_will_hidden())

    def fill_out_specialty_box(self, text):
        box = self.get_specialty_box()
        box.send_keys(text)
        wait_js(lambda: box.send_keys(Keys.ENTER))
        wait_js(lambda: self.wait_while_select2_will_hidden())

    def get_submit_button(self):
        return self.test.browser.find_element_by_css_selector('input[type=submit]')

    def clear_all_boxes(self):
        self.get_number_box().clear()
        self.clear_discipline_box()
        self.clear_specialty_box()

    def get_list_table_rows(self):
        return self.test.browser.find_elements_by_css_selector('table#eumkd-grid tr')