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
from ..utils import get_offset, non_zero_range, verify_series


def bop(open_, high, low, close, scalar=None, offset=None, **kwargs):
    """Indicator: Balance of Power (BOP)"""
    # Validate Arguments
    open_ = verify_series(open_)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    scalar = float(scalar) if scalar else 1
    high_low_range = non_zero_range(high, low)
    close_open_range = non_zero_range(close, open_)
    offset = get_offset(offset)

    # Calculate Result
    bop = scalar * close_open_range / high_low_range

    # Offset
    if offset != 0:
        bop = bop.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        bop.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        bop.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    bop.name = f"BOP"
    bop.category = "momentum"

    return bop


bop.__doc__ = """Balance of Power (BOP)

Balance of Power measure the market strength of buyers against sellers.

Sources:
    http://www.worden.com/TeleChartHelp/Content/Indicators/Balance_of_Power.htm

Calculation:
    BOP = scalar * (close - open) / (high - low)

Args:
    open (pd.Series): Series of 'open's
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    scalar (float): How much to magnify. Default: 1
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
