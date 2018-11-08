from urllib.parse import urlencode, urljoin


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

    def __prepare_query_params(self, query_dict):
        query_dict['access_token'] = self.access_token
        return urlencode(query_dict)

    def __prepare_path(self, path_list):
        versioned_path = [self.version]
        versioned_path.extend(path_list)
        return '/'.join(versioned_path)

    def __prepare_url(self):
        return urljoin(self.base_url, '?'.join([self.path, self.query_params]))

    def get(self):
        # TODO: get self._url, curl, parse response and return python dict()
        pass

    class Meta:
        abstract = True


class AbstractAccountHandler:
    """One major type of graph API nodes is Account, and AbstractAccountHandler
    if parent for all other classes to aggregate required tools, each child
    class should define following variables:
        - path: the node path you are going to read data from, type:str()
        - fields: needed fields your are going from given node: type: list()
        - limit: limit of objects per page (optional), type: int() or str()

    and the following fields required in class initiation:
        - access_token: user access token which comes from facebook"""

    fields = None
    limit = None
    path = ''

    def __init__(self, access_token, *args, **kwargs):
        self.graph = BaseGraphRequestHandler(
            access_token=access_token,
            query_dict=self.build_query_params(),
            path_list=self.build_path_list()
        )

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
        return query_dict

    def build_path_list(self):
        return self.path.split('/')

    class Meta:
        abstract = True
