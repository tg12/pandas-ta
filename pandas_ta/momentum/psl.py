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
from numpy import sign as npSign
from ..utils import get_drift, get_offset, verify_series


def psl(close,
        open_=None,
        length=None,
        scalar=None,
        drift=None,
        offset=None,
        **kwargs):
    """Indicator: Psychological Line (PSL)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 12
    scalar = float(scalar) if scalar and scalar > 0 else 100
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    if open_ is not None:
        open_ = verify_series(open_)
        diff = npSign(close - open_)
    else:
        diff = npSign(close.diff(drift))

    diff.fillna(0, inplace=True)
    diff[diff <= 0] = 0  # Zero negative values

    psl = scalar * diff.rolling(length).sum()
    psl /= length

    # Offset
    if offset != 0:
        psl = psl.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        psl.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        psl.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    _props = f"_{length}"
    psl.name = f"PSL{_props}"
    psl.category = "momentum"

    return psl


psl.__doc__ = """Psychological Line (PSL)

The Psychological Line is an oscillator-type indicator that compares the
number of the rising periods to the total number of periods. In other
words, it is the percentage of bars that close above the previous
bar over a given period.

Sources:
    https://www.quantshare.com/item-851-psychological-line

Calculation:
    Default Inputs:
        length=12, scalar=100, drift=1

    IF NOT open:
        DIFF = SIGN(close - close[drift])
    ELSE:
        DIFF = SIGN(close - open)

    DIFF.fillna(0)
    DIFF[DIFF <= 0] = 0

    PSL = scalar * SUM(DIFF, length) / length

Args:
    close (pd.Series): Series of 'close's
    open_ (pd.Series, optional): Series of 'open's
    length (int): It's period.  Default: 12
    scalar (float): How much to magnify.  Default: 100
    drift (int): The difference period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
