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
from .roc import roc
from ..overlap.rma import rma
from ..overlap.wma import wma
from ..utils import get_offset, verify_series


def coppock(close, length=None, fast=None, slow=None, offset=None, **kwargs):
    """Indicator: Coppock Curve (COPC)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    fast = int(fast) if fast and fast > 0 else 11
    slow = int(slow) if slow and slow > 0 else 14
    min_periods = (int(kwargs["min_periods"]) if "min_periods" in kwargs and
                   kwargs["min_periods"] is not None else length)
    offset = get_offset(offset)

    # Calculate Result
    total_roc = roc(close, fast) + roc(close, slow)
    coppock = wma(total_roc, length)

    # Offset
    if offset != 0:
        coppock = coppock.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        coppock.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        coppock.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    coppock.name = f"COPC_{fast}_{slow}_{length}"
    coppock.category = "momentum"

    return coppock


coppock.__doc__ = """Coppock Curve (COPC)

Coppock Curve (originally called the "Trendex Model") is a momentum indicator
is designed for use on a monthly time scale.  Although designed for monthly
use, a daily calculation over the same period can be made, converting the
periods to 294-day and 231-day rate of changes, and a 210-day weighted
moving average.

Sources:
    https://en.wikipedia.org/wiki/Coppock_curve

Calculation:
    Default Inputs:
        length=10, fast=11, slow=14
    SMA = Simple Moving Average
    MAD = Mean Absolute Deviation
    tp = typical_price = hlc3 = (high + low + close) / 3
    mean_tp = SMA(tp, length)
    mad_tp = MAD(tp, length)
    CCI = (tp - mean_tp) / (c * mad_tp)

Args:
    close (pd.Series): Series of 'close's
    length (int): WMA period.  Default: 10
    fast (int): Fast ROC period.  Default: 11
    slow (int): Slow ROC period.  Default: 14
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
