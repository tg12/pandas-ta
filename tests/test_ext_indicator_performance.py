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
from pandas import DataFrame


class TestPerformaceExtension(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.islong = cls.data["close"] > pandas_ta.sma(cls.data["close"],
                                                       length=50)

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.islong

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_log_return_ext(self):
        self.data.ta.log_return(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "LOGRET_1")

    def test_cum_log_return_ext(self):
        self.data.ta.log_return(append=True, cumulative=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "CUMLOGRET_1")

    def test_percent_return_ext(self):
        self.data.ta.percent_return(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "PCTRET_1")

    def test_cum_percent_return_ext(self):
        self.data.ta.percent_return(append=True, cumulative=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "CUMPCTRET_1")

    def test_log_trend_return_ext(self):
        self.data.ta.trend_return(trend=self.islong,
                                  log=True,
                                  cumulative=False,
                                  append=True)
        self.assertIsInstance(self.data, DataFrame)

    def test_cum_log_trend_return_ext(self):
        self.data.ta.trend_return(trend=self.islong,
                                  log=True,
                                  cumulative=True,
                                  append=True)
        self.assertIsInstance(self.data, DataFrame)

    def test_pct_trend_return_ext(self):
        self.data.ta.trend_return(trend=self.islong,
                                  log=False,
                                  cumulative=False,
                                  append=True)
        self.assertIsInstance(self.data, DataFrame)

    def test_cum_pct_trend_return_ext(self):
        self.data.ta.trend_return(trend=self.islong,
                                  log=False,
                                  cumulative=True,
                                  append=True)
        self.assertIsInstance(self.data, DataFrame)
