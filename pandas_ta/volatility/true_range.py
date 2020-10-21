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
from ..utils import get_drift, get_offset, non_zero_range, verify_series


def true_range(high, low, close, drift=None, offset=None, **kwargs):
    """Indicator: True Range"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    high_low_range = non_zero_range(high, low)
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    prev_close = close.shift(drift)
    ranges = [high_low_range, high - prev_close, prev_close - low]
    true_range = DataFrame(ranges).T
    true_range = true_range.abs().max(axis=1)

    # Offset
    if offset != 0:
        true_range = true_range.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        true_range.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        true_range.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    true_range.name = f"TRUERANGE_{drift}"
    true_range.category = "volatility"

    return true_range


true_range.__doc__ = """True Range

An method to expand a classical range (high minus low) to include
possible gap scenarios.

Sources:
    https://www.macroption.com/true-range/

Calculation:
    Default Inputs:
        drift=1
    ABS = Absolute Value
    prev_close = close.shift(drift)
    TRUE_RANGE = ABS([high - low, high - prev_close, low - prev_close])

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    drift (int): The shift period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature
"""
