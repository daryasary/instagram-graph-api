import unittest

from fixtures import *
from graph_api import InstagramGraphHandler
from graph_api.handlers import InstagramAccountsList, InstagramAccountData, \
    InstagramAccountInsights, InstagramAccountTags, InstagramAccountMediaList, \
    InstagramMediaComments, InstagramMediaInsights


class InstagramGraphHandlerTests(unittest.TestCase):

    def setUp(self):
        self.account_handler = InstagramGraphHandler(
            access_token=SAMPLE_ACCESS_TOKEN, account_id=SAMPLE_ACCOUNT_ID
        )
        self.media_handler = InstagramGraphHandler(
            access_token=SAMPLE_ACCESS_TOKEN, media_id=SAMPLE_MEDIA_ID
        )

    def test_main_graph_handler_initiation(self):
        """ Check only one of handlers is initiating and working properly"""
        self.assertIsInstance(self.account_handler.accounts_list, InstagramAccountsList)
        self.assertEqual(self.account_handler.accounts_list.graph.access_token, SAMPLE_ACCESS_TOKEN)
        self.assertIsInstance(self.account_handler.accounts_list, InstagramAccountsList)
        self.assertEqual(self.account_handler.accounts_list.graph.access_token, SAMPLE_ACCESS_TOKEN)

    def test_main_graph_attrs_correctness(self):
        """ Check that all main handler attribute are pointing to correct module handler class"""
        self.assertIsInstance(self.account_handler.accounts_list, InstagramAccountsList)
        self.assertIsInstance(self.account_handler.account_data, InstagramAccountData)
        self.assertIsInstance(self.account_handler.account_insights, InstagramAccountInsights)
        self.assertIsInstance(self.account_handler.account_tag, InstagramAccountTags)
        self.assertIsInstance(self.account_handler.account_media_list, InstagramAccountMediaList)
        self.assertIsInstance(self.account_handler.media_comments, InstagramMediaComments)
        self.assertIsInstance(self.account_handler.media_insights, InstagramMediaInsights)