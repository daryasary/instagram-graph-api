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
        media_insights=InstagramMediaInsights
    )

    def __init__(self, access_token, account_id=None, media_id=None):
        self.access_token = access_token
        self.account_id = account_id
        self.media_id = media_id
        credentials = dict(
            access_token=self.access_token,
            instagram_media_id=self.media_id,
            instagram_business_account_id=self.account_id
        )
        for attr in self.end_points.keys():
            setattr(self, attr, self.end_points[attr](**credentials))
