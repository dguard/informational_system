import sys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerCase
import os
from datetime import datetime
import time
from selenium.common.exceptions import WebDriverException

SCREEN_DUMP_LOCATION = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'screendumps')
)
DEFAULT_WAIT = 5


def wait_for(function_with_assertion, timeout=DEFAULT_WAIT):
    """
    Wait until function_with_assertion will be successfully asserted or raise function's assertion error

    Keyword arguments:
        function_with_assertion -- function that makes assertion
        timeout -- time for wait without raising error (default defined in DEFAULT_WAIT constant)
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            return function_with_assertion()
        except (AssertionError, WebDriverException):
            time.sleep(0.1)
    # one more try for raising errors if they still exists
    return function_with_assertion()


class BasePage(object):
    """
    Class that present base actions on page

    Attributes:
        test     The instance of functional test
    """
    def __init__(self, test):
        self.test = test

    def get_select2_input(self):
        """
        Returns active select2 input element that can be filled out
        """
        wait_for(
            lambda: self.test.assertIn(True, [
                el.is_displayed() for el in self.test.browser.find_elements_by_css_selector('.select2-input')
            ])
        )
        for el in self.test.browser.find_elements_by_css_selector('.select2-input'):
            if el.is_displayed():
                return el

    def wait_while_select2_will_hidden(self):
        """
        Waits while active select2 input element will disappeared
        """
        wait_for(lambda: self.test.assertNotIn(True, [
            elem.is_displayed() for elem in self.test.browser.find_elements_by_css_selector('.select2-input')
        ]))


class FunctionalTest(StaticLiveServerCase):
    """
    Class that present base functionality for any functional test

    Attributes:
        browser          The instance of webdriver
        server_host      The name of server host without protocol
        server_url       The name of server host with protocol
        against_staging  Detects that it is testing on real server
    """

    @classmethod
    def setUpClass(cls):
        """
        Prepares class to begin testing

        Changes info of server if was provided arg "liveserver" in command line
        """
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                cls.against_staging = True
                return
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        """
        Ends testing for class

        Does not call parent implementation if it test on real server
        """
        if not cls.against_staging:
            super().tearDownClass()

    def setUp(self):
        """
        Prepares browser to begin of testing
        """
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def tearDown(self):
        """
        Makes screenshot and dump of page if test has failed
        And quit browser
        """
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        """
        Returns True if test has failed; False in other case
        """
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def take_screenshot(self):
        """
        Takes screenshot for active browser window
        """
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        """
        Prints to file source code of active browser window
        """
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        """
        Generates and returns filename for current test
        """
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )