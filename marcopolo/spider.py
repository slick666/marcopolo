import base64
from datetime import datetime

import requests


class Spider(object):
    """ Spider:
    Look for .polo files in a github endpoint and return a dictionary of url/yml files.
    """

    def __init__(self, api_endpoint, oauth_token, start_time=None):
        """
        Creates the spider, calls the get_polos function

        :param api_endpoint: https url to github api base  (api.github.com or github.domain.com/api/)
        :param oauth_token: github oauth token with roles: ?
        :param start_time: datetime string and strptime format tuple
        :return:
        """

        self.endpoint = api_endpoint
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token ' + oauth_token

        self.polos = []
        self.get_polos(start_time=start_time)

    def get_polos(self, start_time=None):
        """

        :param start_time: datetime string and strptime format tuple
        :return:
        """
        links = "{}/search/code?q=filename:polo%20extension:polo".format(self.endpoint)
        if start_time is not None:
            links += "%20pushed:<{date_time}".format(date_time=datetime(*start_time).isoformat())
        while links:
            raw_results = self.session.get(links)
            try:
                raw_results.raise_for_status()
            except:
                raise
            if 'next' in raw_results.links.keys():
                links = raw_results.links['next']
            else:
                links = False
            items = raw_results.json()['items']
            for item in items:
                self.polos.append(item['url'])

    def retrieve_polos(self):
        """
        retrieve_polos is a generator that returns urls and polo file strings

        yields tuples of (url, polo_data)
        """
        for polo in self.polos:
            raw_result = self.session.get(polo)
            try:
                raw_result.raise_for_status()
            except:
                raise
            polo = base64.b64decode(raw_result.json()['content'])
            url = raw_result.json()['url']
            yield (url, polo)
