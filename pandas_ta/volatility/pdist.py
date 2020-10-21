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
from ..utils import get_drift, get_offset, non_zero_range, verify_series


def pdist(open_, high, low, close, drift=None, offset=None, **kwargs):
    """Indicator: Price Distance (PDIST)"""
    # Validate Arguments
    open_ = verify_series(open_)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    pdist = 2 * non_zero_range(high, low)
    pdist += non_zero_range(open_, close.shift(drift)).abs()
    pdist -= non_zero_range(close, open_).abs()

    # Offset
    if offset != 0:
        pdist = pdist.shift(offset)

    # Name & Category
    pdist.name = "PDIST"
    pdist.category = "volatility"

    return pdist


pdist.__doc__ = """Price Distance (PDIST)

Measures the "distance" covered by price movements.

Sources:
    https://www.prorealcode.com/prorealtime-indicators/pricedistance/

Calculation:
    Default Inputs:
        drift=1

    PDIST = 2(high - low) - ABS(close - open) + ABS(open - close[drift])

Args:
    open_ (pd.Series): Series of 'opens's
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
