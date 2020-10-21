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
from ..utils import get_offset, verify_series


def rma(close, length=None, offset=None, **kwargs):
    """Indicator: wildeR's Moving Average (RMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    offset = get_offset(offset)
    alpha = (1.0 / length) if length > 0 else 0.5

    # Calculate Result
    rma = close.ewm(alpha=alpha).mean()

    # Offset
    if offset != 0:
        rma = rma.shift(offset)

    # Name & Category
    rma.name = f"RMA_{length}"
    rma.category = "overlap"

    return rma


rma.__doc__ = """wildeR's Moving Average (RMA)

The WildeR's Moving Average is simply an Exponential Moving Average (EMA)
with a modified alpha = 1 / length.

Sources:
    https://alanhull.com/hull-moving-average

Calculation:
    Default Inputs:
        length=10
    EMA = Exponential Moving Average
    alpha = 1 / length
    RMA = EMA(close, alpha=alpha)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
