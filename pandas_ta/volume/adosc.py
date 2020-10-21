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



# -*- coding: utf-8 -*-
from .ad import ad
from ..overlap.ema import ema
from ..utils import get_offset, verify_series


def adosc(high,
          low,
          close,
          volume,
          open_=None,
          fast=None,
          slow=None,
          offset=None,
          **kwargs):
    """Indicator: Accumulation/Distribution Oscillator"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    volume = verify_series(volume)
    fast = int(fast) if fast and fast > 0 else 3
    slow = int(slow) if slow and slow > 0 else 10
    offset = get_offset(offset)

    # Calculate Result
    ad_ = ad(high=high, low=low, close=close, volume=volume, open_=open_)
    fast_ad = ema(close=ad_, length=fast, **kwargs)
    slow_ad = ema(close=ad_, length=slow, **kwargs)
    adosc = fast_ad - slow_ad

    # Offset
    if offset != 0:
        adosc = adosc.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        adosc.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        adosc.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    adosc.name = f"ADOSC_{fast}_{slow}"
    adosc.category = "volume"

    return adosc


adosc.__doc__ = """Accumulation/Distribution Oscillator or Chaikin Oscillator

Accumulation/Distribution Oscillator indicator utilizes
Accumulation/Distribution and treats it similarily to MACD
or APO.

Sources:
    https://www.investopedia.com/articles/active-trading/031914/understanding-chaikin-oscillator.asp

Calculation:
    Default Inputs:
        fast=12, slow=26
    AD = Accum/Dist
    ad = AD(high, low, close, open)
    fast_ad = EMA(ad, fast)
    slow_ad = EMA(ad, slow)
    ADOSC = fast_ad - slow_ad

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    open (pd.Series): Series of 'open's
    volume (pd.Series): Series of 'volume's
    fast (int): The short period.  Default: 12
    slow (int): The long period.   Default: 26
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
