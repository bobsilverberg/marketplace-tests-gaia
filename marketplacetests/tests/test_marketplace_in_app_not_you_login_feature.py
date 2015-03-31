# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import Wait
from fxapom.fxapom import FxATestAccount

from marketplacetests.firefox_accounts.app import FirefoxAccounts
from marketplacetests.payment.app import InAppPayment
from marketplacetests.in_app_payments.in_app import InAppPaymentTester
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase


class TestNotYouLinkInAppPayment(MarketplaceGaiaTestCase):

    test_data = {
        'app_name': 'Testing In-App-Payments',
        'app_title': 'In-App-Payments',
        'product': 'test 0.99 USD'}

    def test_not_you_link_in_app_payment(self):

        homescreen = self.install_in_app_payments_test_app(self.test_data['app_name'])

        # Verify that the app icon is visible on one of the homescreen pages
        self.assertTrue(
            homescreen.is_app_installed(self.test_data['app_name']),
            'App %s not found on homescreen' % self.test_data['app_name'])

        # Click icon and wait for h1 element displayed
        homescreen.installed_app(self.test_data['app_name']).tap_icon()
        Wait(self.marionette).until(lambda m: m.title == self.test_data['app_title'])

        acct = FxATestAccount(base_url=self.base_url).create_account()

        tester_app = InAppPaymentTester(self.marionette)
        fxa = tester_app.tap_buy_product(self.test_data['product'])
        fxa.login(acct.email, acct.password)

        payment = InAppPayment(self.marionette)
        payment.tap_cancel_pin()

        fxa = tester_app.tap_buy_product(self.test_data['product'])
        self.assertTrue(fxa.is_not_you_logout_link_visible)
        self.assertEqual('You are signed in as: %s' % acct.email, 'You are signed in as: %s' % fxa.email_text)

        fxa.tap_not_you()
        fxa.wait_for_password_field_visible()
