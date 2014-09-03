from django.http import HttpResponse


class AssertMatchesMixin(object):

    def assert_matches(self, response, matches):
        content = self._get_content(response)
        self.assertRegexpMatches(content, '(\s|\S)*?'.join(matches))

    def assert_not_matches(self, response, matches):
        try:
            content = self._get_content(response)
            self.assertRegexpMatches(content, '(\s|\S)*?'.join(matches))
        except AssertionError:
            return
        self.fail('Regex "{regex}" matched string!'.format(
            regex='(\s|\S)*?'.join(matches)
        ))

    def _get_content(self, response):
        if isinstance(response, HttpResponse):
            return response.content.decode()
        else:
            return response