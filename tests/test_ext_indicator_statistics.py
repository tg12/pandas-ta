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


class TestStatisticsExtension(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = sample_data

    @classmethod
    def tearDownClass(cls):
        del cls.data

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_entropy_ext(self):
        self.data.ta.entropy(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "ENTP_10")

    def test_kurtosis_ext(self):
        self.data.ta.kurtosis(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "KURT_30")

    def test_mad_ext(self):
        self.data.ta.mad(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "MAD_30")

    def test_median_ext(self):
        self.data.ta.median(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "MEDIAN_30")

    def test_quantile_ext(self):
        self.data.ta.quantile(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "QTL_30_0.5")

    def test_skew_ext(self):
        self.data.ta.skew(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "SKEW_30")

    def test_stdev_ext(self):
        self.data.ta.stdev(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "STDEV_30")

    def test_variance_ext(self):
        self.data.ta.variance(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "VAR_30")
