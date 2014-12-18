# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import random

from fxapom.fxapom import FxATestAccount

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceLoginFromAppDetailsPage(MarketplaceGaiaTestCase):

    def test_marketplace_login_from_app_details_page(self):
        APP_NAME = 'SoundCloud'
        acct = FxATestAccount(use_prod=False).create_account()

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        marketplace.launch()
        details_page = marketplace.navigate_to_app(APP_NAME)

        ff_accounts = details_page.tap_write_review(logged_in=False)
        ff_accounts.login(acct.email, acct.password)

        # switch back to Marketplace
        marketplace.switch_to_marketplace_frame()
        marketplace.wait_for_notification_message_displayed()
        marketplace.wait_for_notification_message_not_displayed()

        current_time = str(time.time()).split('.')[0]
        rating = random.randint(1, 5)
        body = 'This is a test %s' % current_time
        from marketplacetests.marketplace.regions.review_box import AddReview
        review_box = AddReview(self.marionette)

        review_box.write_a_review(rating, body)
        marketplace.wait_for_notification_message_displayed()

        # Check if review was added correctly
        self.assertEqual(marketplace.notification_message, "Your review was posted")
        self.assertEqual(details_page.first_review_rating, rating)
        self.assertEqual(details_page.first_review_body, body)
