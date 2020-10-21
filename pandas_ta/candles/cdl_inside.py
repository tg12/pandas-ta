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
from pandas import DataFrame, set_option
from pandas_ta.utils import candle_color, get_drift, get_offset
from pandas_ta.utils import non_zero_range, real_body, verify_series


def cdl_inside(open_, high, low, close, asbool=False, offset=None, **kwargs):
    """Candle Type: Inside Bar"""
    # Validate arguments
    open_ = verify_series(open_)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)

    # Calculate Result
    inside = (high.diff() < 0) & (low.diff() > 0)

    if not asbool:
        inside *= candle_color(open_, close)

    # Offset
    if offset != 0:
        inside = inside.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        inside.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        inside.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    inside.name = f"CDL_INSIDE"
    inside.category = "candles"

    return inside


cdl_inside.__doc__ = """Candle Type: Inside Bar

An Inside Bar is a bar that is engulfed by the prior highs and lows of it's
previous bar. In other words, the current bar is smaller than it's previous bar.
Set asbool=True if you want to know if it is an Inside Bar. Note by default
asbool=False so this returns a 0 if it is not an Inside Bar, 1 if it is an
Inside Bar and close > open, and -1 if it is an Inside Bar but close < open.

Sources:
    https://www.tradingview.com/script/IyIGN1WO-Inside-Bar/

Calculation:
    Default Inputs:
        asbool=False
    inside = (high.diff() < 0) & (low.diff() > 0)

    if not asbool:
        inside *= candle_color(open_, close)

Args:
    open_ (pd.Series): Series of 'open's
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    asbool (bool): Returns the boolean result. Default: False
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature
"""
