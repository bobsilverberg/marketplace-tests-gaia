# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from fxapom.fxapom import FxATestAccount
from marionette import Wait

from marketplacetests.in_app_payments.in_app import InAppPaymentTester
from marketplacetests.payment.app import InAppPayment
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase


class TestMakeInAppPayment(MarketplaceGaiaTestCase):

    test_data = {
        'app_name': 'Testing In-App-Payments',
        'app_title': 'In-App-Payments',
        'pin': '1234',
        'product': 'test 0.99 USD'}

    def test_make_an_in_app_payment(self):

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
        payment.create_pin(self.test_data['pin'])

        self.assertEqual('Confirm Payment', payment.confirm_payment_header_text)
        self.assertEqual(self.test_data['product'], payment.in_app_product_name)

        payment.tap_buy_button()
        # self.apps.switch_to_displayed_app()
        tester_app.wait_for_bought_products_displayed()
        self.assertEqual(self.test_data['product'], tester_app.bought_product_text)
