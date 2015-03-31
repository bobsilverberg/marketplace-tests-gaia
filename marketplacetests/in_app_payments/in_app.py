# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion
from marionette import expected, By, Wait

from marketplacetests.firefox_accounts.app import FirefoxAccounts


class InAppPayment(Base):

    # Products
    _available_products_locator = (By.ID, 'items')
    _available_product_locator = (By.CSS_SELECTOR, '#items li')
    _bought_product_locator = (By.CSS_SELECTOR, '#bought .item > h4')
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

    def tap_buy_product(self, name):
        for product in self.available_products:
            if product.name == name:
                product.tap_buy_button()
                return FirefoxAccounts(self.marionette)
        raise Exception('Unable to find and tap on product %s.'
                        % name)

    def wait_for_bought_products_displayed(self):
        self.wait_for_element_displayed(*self._bought_product_locator)

    @property
    def available_products(self):
        element = Wait(self.marionette).until(
            expected.element_present(*self._available_products_locator))
        Wait(self.marionette).until(expected.element_displayed(element))
        products = self.marionette.find_elements(*self._available_product_locator)
        return [Product(self.marionette, product) for product in products]


class Product(PageRegion):

    _buy_button_locator = (By.CSS_SELECTOR, 'button')
    _name_locator = (By.CSS_SELECTOR, 'h4')

    @property
    def name(self):
        return self.root_element.find_element(*self._name_locator).text

    def tap_buy_button(self):
        self.root_element.find_element(*self._buy_button_locator).tap()
