from graph_api.handlers import *


class InstagramGraphHandler:
    """Complete parent handler of instagram API, contains all handlers
    developed separately and all of is accessible by calling proper
    attribute of this class object"""
    end_points = dict(
        accounts_list=InstagramAccountsList,
        account_data=InstagramAccountData,
        account_insights=InstagramAccountInsights,
        account_tag=InstagramAccountTags,
        account_media_list=InstagramAccountMediaList,
        media_comments=InstagramMediaComments,
        media_insights=InstagramMediaInsights,
        hashtag_search=InstagramHashtagSearch,
        hashtag_top_media=InstagramHashtagTopMedia,
        hashtag_recent_media=InstagramHashtagRecentMedia
    )

    def __init__(self, access_token, account_id=None, media_id=None, hashtag_id=None):
        self.access_token = access_token
        self.account_id = account_id
        self.media_id = media_id
        self.hashtag_id = hashtag_id
        credentials = self._build_credentials(
            self.access_token, self.media_id, self.hashtag_id, self.account_id
        )
        for attr in self.end_points.keys():
            setattr(self, attr, self.end_points[attr](**credentials))

    def _build_credentials(self, access_token=None, media_id=None,
                           hashtag_id=None, account_id=None):
        if access_token is None:
            access_token = self.access_token
        if media_id is None:
            media_id = self.media_id
        if hashtag_id is None:
            hashtag_id = self.hashtag_id
        if account_id is None:
            account_id = self.account_id
        credentials = dict(
            access_token=access_token, instagram_business_account_id=account_id,
            instagran_hashtag_id=hashtag_id, instagram_media_id=media_id,
        )
        return credentials

    def renew(self, attrs, **kwargs):
        if not isinstance(attrs, list):
            attrs = [attrs]
        credentials = self._build_credentials(**kwargs)
        for attr in attrs:
            if hasattr(self, attr):
                setattr(self, attr, self.end_points[attr](**credentials))
