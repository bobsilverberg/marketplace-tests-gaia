# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import expected, By, Wait
from gaiatest.apps.base import Base


class InAppPayment(Base):

    # Products
    _bought_product_locator = (By.CSS_SELECTOR, '#bought .item > h4')
    _buy_product_button_locator = (By.XPATH, "//h4[text()='%s']/following-sibling::button")
    _server_select_locator = (By.ID, 'server')

    def __init__(self, marionette, server):
        Base.__init__(self, marionette)
        self.apps.switch_to_displayed_app()
        self.set_server('API: %s' % server)

    @property
    def bought_product_text(self):
        return self.marionette.find_element(*self._bought_product_locator).text

    def set_server(self, server):
        element = self.marionette.find_element(*self._server_select_locator)
        element.tap()
        self.select(server)
        self.apps.switch_to_displayed_app()

    def tap_buy_product(self, text):
        element = Wait(self.marionette).until(
            expected.element_present(self._buy_product_button_locator[0], self._buy_product_button_locator[1] % text))
        Wait(self.marionette).until(expected.element_displayed(element))
        element.tap()
        from marketplacetests.firefox_accounts.app import FirefoxAccounts
        return FirefoxAccounts(self.marionette)

    def wait_for_bought_products_displayed(self):
        self.wait_for_element_displayed(*self._bought_product_locator)
