from core import AbstractAccountHandler


class GetInstagramAccounts(AbstractAccountHandler):
    """Get all instagram business accounts ids for all pages of user whom your
    providing his/her access_token in class initiation"""

    path = '/me/accounts/'
    fields = ['instagram_business_account']
