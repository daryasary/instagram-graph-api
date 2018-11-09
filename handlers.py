from core import AbstractAccountHandler


class InstagramAccountsList(AbstractAccountHandler):
    """Get all instagram business accounts ids for all pages of user whom your
    providing his/her access_token in class initiation"""

    path = '/me/accounts/'
    fields = ['instagram_business_account']


class InstagramAccountData(AbstractAccountHandler):
    """Get account's data from facebook api for given instagram account id"""
    fields = (
        'username', 'name', 'biography', 'followers_count', 'follows_count',
        'ig_id', 'media_count', 'profile_picture_url', 'website',
        'recently_searched_hashtags', 'media', 'tags'
    )

    @property
    def path(self):
        return str(self.instagram_bussines_account_id)
