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
# from numpy import sqrt as npsqrt
from pandas import DataFrame
from .atr import atr
from ..overlap.hlc3 import hlc3
from ..overlap.sma import sma
from ..utils import get_offset, non_zero_range, verify_series


def aberration(high,
               low,
               close,
               length=None,
               atr_length=None,
               offset=None,
               **kwargs):
    """Indicator: Aberration (ABER)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 5
    atr_length = int(atr_length) if atr_length and atr_length > 0 else 15
    offset = get_offset(offset)

    # Calculate Result
    atr_ = atr(high=high, low=low, close=close, length=atr_length)
    jg = hlc3(high=high, low=low, close=close)

    zg = sma(jg, length)
    sg = zg + atr_
    xg = zg - atr_

    # Offset
    if offset != 0:
        zg = zg.shift(offset)
        sg = sg.shift(offset)
        xg = xg.shift(offset)
        atr_ = atr_.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        zg.fillna(kwargs["fillna"], inplace=True)
        sg.fillna(kwargs["fillna"], inplace=True)
        xg.fillna(kwargs["fillna"], inplace=True)
        atr_.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        zg.fillna(method=kwargs["fill_method"], inplace=True)
        sg.fillna(method=kwargs["fill_method"], inplace=True)
        xg.fillna(method=kwargs["fill_method"], inplace=True)
        atr_.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    _props = f"_{length}_{atr_length}"
    zg.name = f"ABER_ZG{_props}"
    sg.name = f"ABER_SG{_props}"
    xg.name = f"ABER_XG{_props}"
    atr_.name = f"ABER_ATR{_props}"
    zg.category = sg.category = "volatility"
    xg.category = atr_.category = zg.category

    # Prepare DataFrame to return
    data = {zg.name: zg, sg.name: sg, xg.name: xg, atr_.name: atr_}
    aberdf = DataFrame(data)
    aberdf.name = f"ABER{_props}"
    aberdf.category = zg.category

    return aberdf


aberration.__doc__ = """Aberration

A volatility indicator similar to Keltner Channels.

Sources:
    Few internet resources on definitive definition.
    Request by Github user homily, issue #46

Calculation:
    Default Inputs:
        length=5, atr_length=15
    ATR = Average True Range
    SMA = Simple Moving Average

    ATR = ATR(length=atr_length)
    JG = TP = HLC3(high, low, close)
    ZG = SMA(JG, length)
    SG = ZG + ATR
    XG = ZG - ATR

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): The short period.  Default: 5
    atr_length (int): The short period.  Default: 15
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: zg, sg, xg, atr columns.
"""
