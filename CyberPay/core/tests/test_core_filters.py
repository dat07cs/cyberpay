from django.test import TestCase

from CyberPay.core.templatetags.core_filters import currency_filter


class TestCoreFilters(TestCase):
    def test_currency_filter(self):
        result = currency_filter(1234567890.5, 0)
        self.assertEqual('$1,234,567,891', result)
        result = currency_filter(1234567890.555, 2)
        self.assertEqual('$1,234,567,890.56', result)
        result = currency_filter(-1234567890.5, 0)
        self.assertEqual('($1,234,567,891)', result)
        result = currency_filter(-1234567890.555, 2)
        self.assertEqual('($1,234,567,890.56)', result)
