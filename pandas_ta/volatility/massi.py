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
from ..overlap.ema import ema
from ..utils import get_offset, non_zero_range, verify_series


def massi(high, low, fast=None, slow=None, offset=None, **kwargs):
    """Indicator: Mass Index (MASSI)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    high_low_range = non_zero_range(high, low)
    fast = int(fast) if fast and fast > 0 else 9
    slow = int(slow) if slow and slow > 0 else 25
    if slow < fast:
        fast, slow = slow, fast
    min_periods = (int(kwargs["min_periods"]) if "min_periods" in kwargs and
                   kwargs["min_periods"] is not None else fast)
    offset = get_offset(offset)

    # Calculate Result
    hl_ema1 = ema(close=high_low_range, length=fast, **kwargs)
    hl_ema2 = ema(close=hl_ema1, length=fast, **kwargs)

    hl_ratio = hl_ema1 / hl_ema2
    massi = hl_ratio.rolling(slow, min_periods=slow).sum()

    # Offset
    if offset != 0:
        massi = massi.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        massi.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        massi.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    massi.name = f"MASSI_{fast}_{slow}"
    massi.category = "volatility"

    return massi


massi.__doc__ = """Mass Index (MASSI)

The Mass Index is a non-directional volatility indicator that utilitizes the
High-Low Range to identify trend reversals based on range expansions.

Sources:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:mass_index
    mi = sum(ema(high - low, 9) / ema(ema(high - low, 9), 9), length)

Calculation:
    Default Inputs:
        fast: 9, slow: 25
    EMA = Exponential Moving Average
    hl = high - low
    hl_ema1 = EMA(hl, fast)
    hl_ema2 = EMA(hl_ema1, fast)
    hl_ratio = hl_ema1 / hl_ema2
    MASSI = SUM(hl_ratio, slow)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    fast (int): The short period.  Default: 9
    slow (int): The long period.   Default: 25
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
