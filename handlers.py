from core import AbstractAccountHandler


class InstagramAccountsList(AbstractAccountHandler):
    """Get all instagram business accounts ids for all pages of user whom your
    providing his/her access_token in class initiation
        inputs:
            - access_token
    """

    path = '/me/accounts/'
    fields = ['instagram_business_account']


class InstagramAccountData(AbstractAccountHandler):
    """Get account's data from facebook api for given instagram account id
        inputs:
            - access_token
            - instagram_business_account_id
    """
    fields = (
        'username', 'name', 'biography', 'followers_count', 'follows_count',
        'ig_id', 'media_count', 'profile_picture_url', 'website',
        'recently_searched_hashtags', 'media', 'tags'
    )

    @property
    def path(self):
        return str(self.instagram_business_account_id)


class InstagramAccountInsights(AbstractAccountHandler):
    """To fetch instagram insight from account which account is provided
        inputs:
            - access_token
            - instagram_business_account_id
    """
    metrics = ['impressions', ' reach', ' profile_views']
    period = 'day'

    @property
    def path(self):
        return '{}/insights/'.format(self.instagram_business_account_id)


class InstagramAccountTags(AbstractAccountHandler):
    """Find Instagram posts which provided account tagged in
        inputs:
            - access_token
            - instagram_business_account_id
    """
    fields = (
        'caption', 'comments_count', 'username', 'id', 'like_count',
        'media_type', 'media_url', 'owner', 'permalink', 'timestamp'
    )
    limit = 100

    @property
    def path(self):
        return '{}/tags/'.format(self.instagram_business_account_id)
