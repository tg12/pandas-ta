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
from numpy import sqrt as npsqrt
from .variance import variance
from ..utils import get_offset, verify_series


def stdev(close, length=None, ddof=1, offset=None, **kwargs):
    """Indicator: Standard Deviation"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 30
    ddof = int(ddof) if ddof >= 0 and ddof < length else 1
    offset = get_offset(offset)

    # Calculate Result
    stdev = variance(close=close, length=length, ddof=ddof).apply(npsqrt)

    # Offset
    if offset != 0:
        stdev = stdev.shift(offset)

    # Name & Category
    stdev.name = f"STDEV_{length}"
    stdev.category = "statistics"

    return stdev


stdev.__doc__ = """Rolling Standard Deviation

Sources:

Calculation:
    Default Inputs:
        length=30
    VAR = Variance
    STDEV = variance(close, length).apply(np.sqrt)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 30
    ddof (int): Delta Degrees of Freedom.
                The divisor used in calculations is N - ddof,
                where N represents the number of elements. Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
