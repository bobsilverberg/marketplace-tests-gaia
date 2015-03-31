# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import random

from fxapom.fxapom import FxATestAccount

from marketplacetests.marketplace.regions.add_review import AddReview
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceLoginFromAppDetailsPage(MarketplaceGaiaTestCase):

    def test_marketplace_login_from_app_details_page(self):
        acct = FxATestAccount(base_url=self.base_url).create_account()

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        popular_apps_page = home_page.popular_apps_page
        app_name = popular_apps_page.popular_apps[0].name
        details_page = popular_apps_page.navigate_to_app(app_name)

        ff_accounts = details_page.tap_write_review(logged_in=False)
        ff_accounts.login(acct.email, acct.password)

        # switch back to Marketplace
        marketplace.switch_to_marketplace_frame()

        current_time = str(time.time()).split('.')[0]
        rating = random.randint(1, 5)
        body = 'This is a test %s' % current_time
        review_page = AddReview(self.marionette)

        details_page = review_page.write_a_review(rating, body)
        details_page.wait_for_notification_message_displayed('Your review was successfully posted. Thanks!')

        # Check if review was added correctly
        self.assertEqual(details_page.first_review_rating, rating)
        self.assertEqual(details_page.first_review_body, body)
