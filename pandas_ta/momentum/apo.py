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
from pandas_ta.overlap import sma
from pandas_ta.utils import get_offset, verify_series


def apo(close, fast=None, slow=None, offset=None, **kwargs):
    """Indicator: Absolute Price Oscillator (APO)"""
    # Validate Arguments
    close = verify_series(close)
    fast = int(fast) if fast and fast > 0 else 12
    slow = int(slow) if slow and slow > 0 else 26
    if slow < fast:
        fast, slow = slow, fast
    min_periods = (int(kwargs["min_periods"]) if "min_periods" in kwargs and
                   kwargs["min_periods"] is not None else fast)
    offset = get_offset(offset)

    # Calculate Result
    fastma = sma(close, length=fast)
    slowma = sma(close, length=slow)
    apo = fastma - slowma

    # Offset
    if offset != 0:
        apo = apo.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        apo.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        apo.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    apo.name = f"APO_{fast}_{slow}"
    apo.category = "momentum"

    return apo


apo.__doc__ = """Absolute Price Oscillator (APO)

The Absolute Price Oscillator is an indicator used to measure a security's
momentum.  It is simply the difference of two Exponential Moving Averages
(EMA) of two different periods.  Note: APO and MACD lines are equivalent.

Sources:
    https://www.tradingtechnologies.com/xtrader-help/x-study/technical-indicator-definitions/absolute-price-oscillator-apo/

Calculation:
    Default Inputs:
        fast=12, slow=26
    SMA = Simple Moving Average
    APO = SMA(close, fast) - SMA(close, slow)

Args:
    close (pd.Series): Series of 'close's
    fast (int): The short period.  Default: 12
    slow (int): The long period.   Default: 26
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
