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



from .config import sample_data
from .context import pandas_ta

from unittest import TestCase
from pandas import Series


class TestPerformace(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.close = cls.data["close"]
        cls.islong = (cls.close > pandas_ta.sma(cls.close,
                                                length=8)).astype(int)

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.close
        del cls.islong

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_log_return(self):
        result = pandas_ta.log_return(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "LOGRET_1")

    def test_cum_log_return(self):
        result = pandas_ta.log_return(self.close, cumulative=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CUMLOGRET_1")

    def test_percent_return(self):
        result = pandas_ta.percent_return(self.close, cumulative=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "PCTRET_1")

    def test_cum_percent_return(self):
        result = pandas_ta.percent_return(self.close, cumulative=True)
        self.assertEqual(result.name, "CUMPCTRET_1")

    def test_log_trend_return(self):
        result = pandas_ta.trend_return(self.close,
                                        self.islong,
                                        log=True,
                                        cumulative=False)
        self.assertEqual(result.name, "LTR")

    def test_cum_log_trend_return(self):
        result = pandas_ta.trend_return(self.close,
                                        self.islong,
                                        log=True,
                                        cumulative=True)
        self.assertEqual(result.name, "CLTR")

    def test_variable_cum_log_trend_return(self):
        result = pandas_ta.trend_return(self.close,
                                        self.islong,
                                        log=True,
                                        cumulative=True,
                                        variable=True)
        self.assertEqual(result.name, "CLTR")

    def test_pct_trend_return(self):
        result = pandas_ta.trend_return(self.close,
                                        self.islong,
                                        log=False,
                                        cumulative=False)
        self.assertEqual(result.name, "PTR")

    def test_cum_pct_trend_return(self):
        result = pandas_ta.trend_return(self.close,
                                        self.islong,
                                        log=False,
                                        cumulative=True)
        self.assertEqual(result.name, "CPTR")

    def test_variable_pct_log_trend_return(self):
        result = pandas_ta.trend_return(self.close,
                                        self.islong,
                                        log=False,
                                        cumulative=True,
                                        variable=True)
        self.assertEqual(result.name, "CPTR")
