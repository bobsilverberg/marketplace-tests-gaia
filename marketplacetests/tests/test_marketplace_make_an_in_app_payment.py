# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from fxapom.fxapom import FxATestAccount
from marionette import Wait

from marketplacetests.in_app_payments.in_app import InAppPayment
from marketplacetests.payment.app import Payment
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase


class TestMakeInAppPayment(MarketplaceGaiaTestCase):

    test_data = {
        'app_name': 'Testing In-App-Payments',
        'app_title': 'In-App-Payments',
        'server': 'marketplace-dev.allizom.org',
        'pin': '1234',
        'product': 'test 0.99 USD'}

    def test_make_an_in_app_payment(self):

        self.install_in_app_payments_test_app(self.test_data['app_name'])

        acct = FxATestAccount(base_url=self.base_url).create_account()

        # Verify that the app icon is visible on one of the homescreen pages
        self.assertTrue(
            self.homescreen.is_app_installed(self.test_data['app_name']),
            'App %s not found on homescreen' % self.test_data['app_name'])

        # Click icon and wait for h1 element displayed
        self.homescreen.installed_app(self.test_data['app_name']).tap_icon()
        Wait(self.marionette).until(lambda m: m.title == self.test_data['app_title'])

        tester_app = InAppPayment(self.marionette, self.test_data['server'])
        fxa = tester_app.tap_buy_product(self.test_data['product'])
        fxa.login(acct.email, acct.password)

        payment = Payment(self.marionette)
        payment.create_pin(self.test_data['pin'])

        self.assertEqual('Confirm Payment', payment.confirm_payment_header_text)
        self.assertEqual(self.test_data['product'], payment.in_app_product_name)

        payment.tap_in_app_buy_button()
        # self.apps.switch_to_displayed_app()
        tester_app.wait_for_bought_products_displayed()
        self.assertEqual(self.test_data['product'], tester_app.bought_product_text)
