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
from pandas_ta.utils import get_offset, high_low_range, is_percent
from pandas_ta.utils import non_zero_range, real_body, verify_series


def cdl_doji(
    open_,
    high,
    low,
    close,
    length=None,
    factor=None,
    scalar=None,
    asint=True,
    offset=None,
    **kwargs,
):
    """Candle Type: Doji"""
    # Validate Arguments
    open_ = verify_series(open_)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    factor = float(factor) if is_percent(factor) else 10
    scalar = float(scalar) if scalar else 100
    offset = get_offset(offset)
    naive = kwargs.pop("naive", False)

    # Calculate Result
    body = real_body(open_, close).abs()
    hl_range = high_low_range(high, low).abs()
    hl_range_avg = sma(hl_range, length)
    doji = body < 0.01 * factor * hl_range_avg

    if naive:
        doji.iloc[:length] = body < 0.01 * factor * hl_range
    if asint:
        doji = scalar * doji.astype(int)

    # Offset
    if offset != 0:
        doji = doji.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        doji.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        doji.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    doji.name = f"CDL_DOJI_{length}_{0.01 * factor}"
    doji.category = "candles"

    return doji


cdl_doji.__doc__ = """Candle Type: Doji

A candle body is Doji, when it's shorter than 10% of the
average of the 10 previous candles' high-low range.

Sources:
    TA-Lib: 96.56% Correlation

Calculation:
    Default values:
        length=10, percent=10 (0.1), scalar=100
    ABS = Absolute Value
    SMA = Simple Moving Average

    BODY = ABS(close - open)
    HL_RANGE = ABS(high - low)

    DOJI = scalar IF BODY < 0.01 * percent * SMA(HL_RANGE, length) ELSE 0

Args:
    open_ (pd.Series): Series of 'open's
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): The period. Default: 10
    factor (float): Doji value. Default: 100
    scalar (float): How much to magnify. Default: 100
    asint (bool): Keep results numerical instead of boolean. Default: True

Kwargs:
    naive (bool, optional): If True, prefills potential Doji less than
        the length if less than a percentage of it's high-low range. Default: False
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: CDL_DOJI column.
"""
