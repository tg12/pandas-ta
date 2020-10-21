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
from numpy import NaN as npNaN
from pandas import DataFrame, Series
from .ema import ema
from .hma import hma
from .sma import sma
from pandas_ta.utils import get_offset, verify_series


def hilo(
    high,
    low,
    close,
    high_length=None,
    low_length=None,
    mamode=None,
    offset=None,
    **kwargs,
):
    """Indicator: Gann HiLo (HiLo)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    high_length = int(high_length) if high_length and high_length > 0 else 13
    low_length = int(low_length) if low_length and low_length > 0 else 21
    mamode = mamode.lower() if mamode else "sma"
    offset = get_offset(offset)

    # Calculate Result
    m = close.size
    hilo = Series(npNaN, index=close.index)
    long = Series(npNaN, index=close.index)
    short = Series(npNaN, index=close.index)

    if mamode == "ema":
        high_ma = ema(high, high_length)
        low_ma = ema(low, low_length)
    if mamode == "hma":
        high_ma = hma(high, high_length)
        low_ma = hma(low, low_length)
    else:  # "sma"
        high_ma = sma(high, high_length)
        low_ma = sma(low, low_length)

    for i in range(1, m):
        if close.iloc[i] > high_ma.iloc[i - 1]:
            hilo.iloc[i] = long.iloc[i] = low_ma.iloc[i]
        elif close.iloc[i] < low_ma.iloc[i - 1]:

            hilo.iloc[i] = short.iloc[i] = high_ma.iloc[i]
        else:
            hilo.iloc[i] = hilo.iloc[i - 1]
            long.iloc[i] = short.iloc[i] = hilo.iloc[i - 1]

    # Offset
    if offset != 0:
        hilo = hilo.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        hilo.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        hilo.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    _props = f"_{high_length}_{low_length}"
    df = DataFrame(
        {
            f"HILO{_props}": hilo,
            f"HILOl{_props}": long,
            f"HILOs{_props}": short
        },
        index=close.index,
    )

    df.name = f"HILO{_props}"
    df.category = "overlap"

    return df


hilo.__doc__ = """Gann HiLo Activator(HiLo)

The Gann High Low Activator Indicator was created by Robert Krausz in a 1998
issue of Stocks & Commodities Magazine. It is a moving average based trend
indicator consisting of two different simple moving averages.

The indicator tracks both curves (of the highs and the lows). The close of the
bar defines which of the two gets plotted.

Increasing high_length and decreasing low_length better for short trades,
vice versa for long positions.

Sources:
    https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=447&Name=Gann_HiLo_Activator
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/simple-moving-average-sma/
    https://www.tradingview.com/script/XNQSLIYb-Gann-High-Low/

Calculation:
    Default Inputs:
        high_length=13, low_length=21, mamode="sma"
    EMA = Exponential Moving Average
    HMA = Hull Moving Average
    SMA = Simple Moving Average # Default

    if "ema":
        high_ma = EMA(high, high_length)
        low_ma = EMA(low, low_length)
    elif "hma":
        high_ma = HMA(high, high_length)
        low_ma = HMA(low, low_length)
    else: # "sma"
        high_ma = SMA(high, high_length)
        low_ma = SMA(low, low_length)

    # Similar to Supertrend MA selection
    hilo = Series(npNaN, index=close.index)
    for i in range(1, m):
        if close.iloc[i] > high_ma.iloc[i - 1]:
            hilo.iloc[i] = low_ma.iloc[i]
        elif close.iloc[i] < low_ma.iloc[i - 1]:
            hilo.iloc[i] = high_ma.iloc[i]
        else:
            hilo.iloc[i] = hilo.iloc[i - 1]

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    high_length (int): It's period. Default: 13
    low_length (int): It's period. Default: 21
    mamode (str): Options: 'sma' or 'ema'.  Default: 'sma'
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    adjust (bool): Default: True
    presma (bool, optional): If True, uses SMA for initial value.
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: HILO (line), HILOl (long), HILOs (short) columns.
"""
