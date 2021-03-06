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
from pandas_ta.overlap import ema, sma
from pandas_ta.statistics import stdev
from pandas_ta.utils import (
    get_drift,
    get_offset,
    non_zero_range,
    unsigned_differences,
    verify_series,
)


def rvi(
    close,
    high=None,
    low=None,
    length=None,
    scalar=None,
    refined=None,
    thirds=None,
    mamode=None,
    drift=None,
    offset=None,
    **kwargs,
):
    """Indicator: Relative Volatility Index (RVI)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    scalar = float(scalar) if scalar and scalar > 0 else 100
    refined = False if refined is None else refined
    thirds = False if thirds is None else thirds
    mamode = mamode.lower() if mamode else "ema"
    drift = get_drift(drift)
    offset = get_offset(offset)

    if refined or thirds:
        high = verify_series(high)
        low = verify_series(low)

    # Calculate Result
    def rvi_(source, length, scalar, mamode, drift):
        """RVI"""
        std = stdev(source, length)
        pos, neg = unsigned_differences(source, amount=drift)

        pos_std = pos * std
        neg_std = neg * std

        if mamode == "sma":
            pos_avg = sma(pos_std, length)
            neg_avg = sma(neg_std, length)
        else:  # "ema"
            pos_avg = ema(pos_std, length)
            neg_avg = ema(neg_std, length)

        result = scalar * pos_avg
        result /= pos_avg + neg_avg
        return result

    _mode = ""
    if refined:
        high_rvi = rvi_(high, length, scalar, mamode, drift)
        low_rvi = rvi_(low, length, scalar, mamode, drift)
        rvi = 0.5 * (high_rvi + low_rvi)
        _mode = "r"
    elif thirds:
        high_rvi = rvi_(high, length, scalar, mamode, drift)
        low_rvi = rvi_(low, length, scalar, mamode, drift)
        close_rvi = rvi_(close, length, scalar, mamode, drift)
        rvi = (high_rvi + low_rvi + close_rvi) / 3.0
        _mode = "t"
    else:
        rvi = rvi_(close, length, scalar, mamode, drift)

    # Offset
    if offset != 0:
        rvi = rvi.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        rvi.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        rvi.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    rvi.name = f"RVI{_mode}_{length}"
    rvi.category = "volatility"

    return rvi


rvi.__doc__ = """Relative Volatility Index (RVI)

The Relative Volatility Index (RVI) was created in 1993 and
revised in 1995. Instead of adding up price changes like RSI
based on price direction, the RVI adds up standard deviations
based on price direction.

Sources:
    https://www.tradingview.com/wiki/Keltner_Channels_(KC)

Calculation:
    Default Inputs:
        length=14, scalar=100, refined=None, thirds=None
    EMA = Exponential Moving Average
    STDEV = Standard Deviation

    UP = STDEV(src, length) IF src.diff() > 0 ELSE 0
    DOWN = STDEV(src, length) IF src.diff() <= 0 ELSE 0

    UPSUM = EMA(UP, length)
    DOWNSUM = EMA(DOWN, length

    RVI = scalar * (UPSUM / (UPSUM + DOWNSUM))

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): The short period. Default: 14
    scalar (float): A positive float to scale the bands.   Default: 100
    mamode (str): Options: 'sma' or 'ema'. Default: 'sma'
    refined (bool): Use 'refined' calculation which is the average of
        RVI(high) and RVI(low) instead of RVI(close). Default: False
    thirds (bool): Average of high, low and close. Default: False
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: lower, basis, upper columns.
"""
