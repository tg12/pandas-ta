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
from pandas import DataFrame
from pandas_ta.overlap import ema
from pandas_ta.utils import get_offset, verify_series


def eri(high, low, close, length=None, offset=None, **kwargs):
    """Indicator: Elder Ray Index (ERI)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 13
    offset = get_offset(offset)

    # Calculate Result
    ema_ = ema(close, length)
    bull = high - ema_
    bear = low - ema_

    # Offset
    if offset != 0:
        bull = bull.shift(offset)
        bear = bear.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        bull.fillna(kwargs["fillna"], inplace=True)
        bear.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        bull.fillna(method=kwargs["fill_method"], inplace=True)
        bear.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    bull.name = f"BULLP_{length}"
    bear.name = f"BEARP_{length}"
    bull.category = bear.category = "momentum"

    # Prepare DataFrame to return
    data = {bull.name: bull, bear.name: bear}
    df = DataFrame(data)
    df.name = f"ERI_{length}"
    df.category = bull.category

    return df


eri.__doc__ = """Elder Ray Index (ERI)

Elder's Bulls Ray Index contains his Bull and Bear Powers. Which are useful ways
to look at the price and see the strength behind the market. Bull Power
measures the capability of buyers in the market, to lift prices above an average
consensus of value.

Bears Power measures the capability of sellers, to drag prices below an average
consensus of value. Using them in tandem with a measure of trend allows you to
identify favourable entry points. We hope you've found this to be a useful
discussion of the Bulls and Bears Power indicators.

Sources:
    https://admiralmarkets.com/education/articles/forex-indicators/bears-and-bulls-power-indicator

Calculation:
    Default Inputs:
        length=13
    EMA = Exponential Moving Average

    BULLPOWER = high - EMA(close, length)
    BEARPOWER = low - EMA(close, length)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 14
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: bull power and bear power columns.
"""
