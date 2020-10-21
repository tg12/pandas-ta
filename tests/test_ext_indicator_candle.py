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


class TestCandleExtension(TestCase):

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

    def test_cdl_doji_ext(self):
        self.data.ta.cdl_doji(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "CDL_DOJI_10_0.1")

    def test_cdl_inside_ext(self):
        self.data.ta.cdl_inside(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "CDL_INSIDE")

    def test_ha_ext(self):
        self.data.ta.ha(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-4:]),
                         ["HA_open", "HA_high", "HA_low", "HA_close"])
