# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceFeedback(MarketplaceGaiaTestCase):

    def test_marketplace_feedback_anonymous(self):
        feedback_submitted_message = u'Feedback submitted. Thanks!'
        test_comment = 'This is a test comment.'

        # launch marketplace dev and go to marketplace
        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        # go to settings page
        settings = home_page.tap_settings()
        settings.select_setting_feedback()

        # enter and submit your feedback
        settings.enter_feedback(test_comment)
        settings.submit_feedback()

        # wait for the notification
        settings.wait_for_notification_message_displayed(feedback_submitted_message)
