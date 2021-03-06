# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase

from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceLogin(MarketplaceGaiaTestCase):

    def setUp(self):
        MarketplaceGaiaTestCase.setUp(self)

        self.marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        self.marketplace.launch()

    def test_login_marketplace(self):
        # https://moztrap.mozilla.org/manage/case/4134/
        username = self.testvars['marketplace']['username']
        password = self.testvars['marketplace']['password']

        settings = self.marketplace.tap_settings()
        ff_accounts = settings.tap_sign_in()

        ff_accounts.login(username, password)

        # switch back to Marketplace
        self.marketplace.switch_to_marketplace_frame()

        # wait for signed-in notification at the bottom of the screen to clear
        settings.wait_for_sign_out_button()
        self.marketplace.wait_for_notification_message_not_displayed()

        # Verify that user is logged in
        self.assertEqual(username, settings.email)

        # Sign out, which should return to the Marketplace home screen
        settings.tap_sign_out()

        # Verify that user is signed out
        settings.wait_for_sign_in_displayed()
