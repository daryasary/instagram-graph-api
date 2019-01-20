import requests

try:
    from urllib.parse import urlencode, urljoin
except ImportError:
    from urllib import urlencode
    from urlparse import urljoin


class BaseGraphRequestHandler:
    """Base request handler of facebook graph API, all Account and Media handlers
    are inherit this class to read and retrieve data from facebook API"""
    base_url = "https://graph.facebook.com/"

    def __init__(self, access_token, query_dict=None, path_list='', version='v3.2'):
        self.access_token = access_token
        self.version = version
        self.query_params = self.__prepare_query_params(query_dict)
        self.path = self.__prepare_path(path_list)
        self._url = self.__prepare_url()
        self._next = None
        self._previous = None
        self._cursor_after = None
        self._cursor_before = None
        self._data = None
        self._cached_response = None

    def __prepare_query_params(self, query_dict):
        query_dict['access_token'] = self.access_token
        return urlencode(query_dict)

    def __prepare_path(self, path_list):
        versioned_path = [self.version]
        versioned_path.extend(path_list)
        return '/'.join(versioned_path)

    def __prepare_url(self):
        return urljoin(self.base_url, '?'.join([self.path, self.query_params]))

    def __prepare_partial_url(self, query):
        params = self.__prepare_query_params(query)
        return urljoin(self.base_url, '?'.join([self.path, params]))

    def __reset_cursor(self):
        self._next = None
        self._previous = None
        self._cursor_after = None
        self._cursor_before = None

    def __set_pages(self, response):
        if 'paging' in response.keys():
            paging = response.get('paging')
            cursors = paging.get('cursors')
            if 'after' in cursors.keys():
                self._cursor_after = cursors.get('after')
                self._next = self.__prepare_partial_url(
                    {'after': self._cursor_after}
                )
            if 'before' in cursors.keys():
                self._cursor_before = cursors.get('before')
                self._previous = self.__prepare_partial_url(
                    {'after': self._cursor_before}
                )
            if 'data' in response.keys():
                self._data = response.get('data')
        else:
            self._data = response

    def _parse_response(self, response):
        # return self._previous, response, self._next
        return response

    def has_next(self):
        return bool(self._next)

    def get(self):
        url = self._next if self.has_next() else self._url
        response = requests.get(url)
        self._cached_response = response.text
        self.__reset_cursor()
        if response.status_code//100 == 2:
            self.__set_pages(response.json())
            return True, self._data
        return False, response

    class Meta:
        abstract = True


class CommonAbstractHandler:
    """Aggregate some common methods of account and media handlers together
    to avoid DRY methodology"""
    fields = None
    sub_fields = None
    limit = None
    metrics = None
    period = None
    path = ''

    @property
    def fields_str(self):
        return ','.join(self.fields)

    @property
    def wrapped_path(self):
        if self.path.startswith('/'):
            self.path = self.path[1:]

        if self.path.endswith('/'):
            self.path = self.path[:-1]
        return self.path

    def build_query_params(self):
        query_dict = dict()
        if self.fields is not None:
            query_dict['fields'] = self.fields_str
        if self.limit:  # Is None or 0
            query_dict['limit'] = self.limit
        if self.metrics is not None:
            query_dict['metrics'] = self.metrics
        if self.period is not None:
            query_dict['period'] = self.period
        return query_dict

    def build_path_list(self):
        return self.path.split('/')

    def get(self):
        result, response = self.graph.get()
        if not result:
            return response
        if not hasattr(self, 'parse_response'):
            setattr(self, 'parse_response', self.graph._parse_response)
        return self.parse_response(response)

    class Meta:
        abstract = True


class AbstractAccountHandler(CommonAbstractHandler):
    """One major type of graph API nodes is Account, and AbstractAccountHandler
    if parent for all other classes to aggregate required tools, each child
    class should define following variables:
        - path: the node path you are going to read data from, type:str()
        - fields: needed fields your are going from given node: type: list()
        - limit: limit of objects per page (optional), type: int() or str()

    and the following fields required in class initiation:
        - access_token: user access token which comes from facebook
        - instagram_business_account_id: account id given from facebook"""

    def __init__(self, access_token, instagram_business_account_id=None ,*args, **kwargs):
        self.instagram_business_account_id = instagram_business_account_id
        self.graph = BaseGraphRequestHandler(
            access_token=access_token,
            query_dict=self.build_query_params(),
            path_list=self.build_path_list()
        )


class AbstractMediaHandler(CommonAbstractHandler):
    """One major type of graph API nodes is Media, and AbstractMediaHandler
    if parent for all other classes to aggregate required tools, each child
    class should define following variables:
        - path: the node path you are going to read data from, type:str()
        - fields: needed fields your are going from given node: type: list()
        - limit: limit of objects per page (optional), type: int() or str()

    and the following fields required in class initiation:
        - access_token: user access token which comes from facebook
        - instagram_media_id: media object id which we are going to read data"""

    def __init__(self, access_token, instagram_media_id=None, *args, **kwargs):
        self.instagram_media_id= instagram_media_id
        self.graph = BaseGraphRequestHandler(
            access_token=access_token,
            query_dict=self.build_query_params(),
            path_list=self.build_path_list()
        )

    @property
    def fields_str(self):
        if isinstance(self.fields, str):
            return self.fields
        return ','.join(self.fields)
