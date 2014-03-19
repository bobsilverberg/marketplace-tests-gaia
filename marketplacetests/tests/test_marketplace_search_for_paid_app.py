# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestSearchMarketplacePaidApp(MarketplaceGaiaTestCase):

    def test_search_paid_app(self):
        marketplace = Marketplace(self.marionette, 'Marketplace Dev')
        marketplace.launch()

        results = marketplace.search(':paid')

        self.assertGreater(len(results.search_results), 0, 'No results found.')

        for result in results.search_results:
            print 'The text of the result element is: %s' % result.full_text
            print 'The price seems to be: %s' % result.price
            print 'The length of price is: %s' % len(result.price)
