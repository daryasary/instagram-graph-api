from graph_api.core import AbstractAccountHandler, AbstractMediaHandler, \
    AbstractHashtagHandler


class InstagramAccountsList(AbstractAccountHandler):
    """Get all instagram business accounts ids for all pages of user whom your
    providing his/her access_token in class initiation
        inputs:
            - access_token
    """
    path = '/me/accounts/'
    fields = ['instagram_business_account']

    @staticmethod
    def parse_response(data):
        """Filter accounts and show pages which linked with instagram account"""
        return [ac for ac in data if 'instagram_business_account' in ac.keys()]


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
    metric = ['impressions', ' reach', ' profile_views']
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


class InstagramAccountMediaList(AbstractAccountHandler):
    """Get paginated instagram media list for account which id is provided
        inputs:
            - access_token
            - instagram_business_account_id
            - limit
    """
    fields = (
        'caption', 'comments_count', 'id', 'ig_id', 'is_comment_enabled',
        'like_count', 'media_type', 'media_url', 'owner', 'permalink',
        'shortcode', 'thumbnail_url', 'timestamp', 'username'
    )
    limit = 100

    @property
    def path(self):
        return '{}/media'.format(self.instagram_business_account_id)


class InstagramMediaComments(AbstractMediaHandler):
    """Fetch comments for media which media_id is given"""
    fields_pattern = "comments"
    sub_fields = "{like_count,media,id,text,hidden, timestamp,user,username," \
                 "replies{like_count,media,text, timestamp,id,user,username}}"
    limite = 20

    @property
    def path(self):
        return "/{}/".format(self.instagram_media_id)

    @property
    def fields(self):
        if self.limit is None:
            return "{}{}".format(self.fields_pattern, self.sub_fields)
        return "{}.limit({}){}".format(self.fields_pattern, self.limit, self.sub_fields)


class InstagramMediaInsights(AbstractMediaHandler):
    """Read one specific media's insights"""
    metric = ['engagement', 'impressions', 'reach']

    @property
    def path(self):
        return "{}/insights".format(self.instagram_media_id)


class InstagramHashtagSearch(AbstractHashtagHandler):
    """Search hashtag through instagram and return hashtag_id and name"""

    path = "ig_hashtag_search"

    @property
    def extra_params(self):
        params = dict(user_id=self.instagram_business_account_id, q=self.q)
        return params
