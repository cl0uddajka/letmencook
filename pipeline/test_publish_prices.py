import unittest
from datetime import date
from publish_prices import build


class PublishTests(unittest.TestCase):
    def row(self, market='A', **changes):
        return dict(approved=True, source_type='market_retail', region='Hà Nội', market=market,
                    ingredient='Cà chua', variant='thường', unit='kg', reviewed_by='test',
                    source_url='https://example.com/survey', surveyed_on='2026-09-26',
                    price_min_vnd=20000, price_max_vnd=20000, **changes)

    def result(self, rows):
        return build({'observations': rows}, date(2026, 9, 26))[0]['regions']['Hà Nội']

    def test_two_markets(self):
        self.assertEqual(self.result([self.row(), self.row('B')])['Cà chua']['price_vnd'], 20000)

    def test_duplicates_not_independent(self):
        self.assertEqual(self.result([self.row(), self.row()]), {})

    def test_stale_unknown_unreviewed_or_wrong_source(self):
        for changes in ({'surveyed_on': None}, {'surveyed_on': '2026-09-16'}, {'approved': False}, {'source_type': 'online_retail'}, {'price_min_vnd': float('nan')}, {'unit': 'bó'}):
            rows = [{**self.row(), **changes}, {**self.row('B'), **changes}]
            self.assertEqual(self.result(rows), {})

    def test_regions_not_mixed(self):
        self.assertEqual(self.result([self.row(), {**self.row('B'), 'region': 'TP.HCM'}]), {})


if __name__ == '__main__': unittest.main()
