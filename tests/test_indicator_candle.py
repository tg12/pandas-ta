'''THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd

# contact :- github@jamessawyer.co.uk



from .config import (
    error_analysis,
    sample_data,
    CORRELATION,
    CORRELATION_THRESHOLD,
    VERBOSE,
)
from .context import pandas_ta

from unittest import TestCase, skip
import pandas.testing as pdt
from pandas import DataFrame, Series

import talib as tal


class TestCandle(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.data.columns = cls.data.columns.str.lower()
        cls.open = cls.data["open"]
        cls.high = cls.data["high"]
        cls.low = cls.data["low"]
        cls.close = cls.data["close"]
        if "volume" in cls.data.columns:
            cls.volume = cls.data["volume"]

    @classmethod
    def tearDownClass(cls):
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        if hasattr(cls, "volume"):
            del cls.volume
        del cls.data

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ha(self):
        result = pandas_ta.ha(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "Heikin-Ashi")

    def test_cdl_doji(self):
        result = pandas_ta.cdl_doji(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CDL_DOJI_10_0.1")

        try:
            expected = tal.CDLDOJI(self.open, self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result,
                                                         expected,
                                                         col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_cdl_inside(self):
        result = pandas_ta.cdl_inside(self.open, self.high, self.low,
                                      self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CDL_INSIDE")

        result = pandas_ta.cdl_inside(self.open,
                                      self.high,
                                      self.low,
                                      self.close,
                                      asbool=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CDL_INSIDE")
