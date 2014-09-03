from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.server_url + '/eumkd/search/')
        self.browser.set_window_size(1024, 768)

        # input box in the center of page
        input_box = self.browser.find_element_by_css_selector('#id_number')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width']/2,
            512,
            delta=5
        )

        # input box still in the center of page after filling input
        input_box.send_keys('testing\n')
        input_box = self.browser.find_element_by_css_selector('#id_number')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width']/2,
            512,
            delta=5
        )