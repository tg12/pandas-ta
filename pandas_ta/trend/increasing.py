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
from pandas_ta.utils import get_offset, verify_series


def increasing(close, length=None, asint=True, offset=None, **kwargs):
    """Indicator: Increasing"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    increasing = close.diff(length) > 0
    if asint:
        increasing = increasing.astype(int)

    # Offset
    if offset != 0:
        increasing = increasing.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        increasing.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        increasing.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    increasing.name = f"INC_{length}"
    increasing.category = "trend"

    return increasing


increasing.__doc__ = """Increasing

Returns True or False if the series is increasing over a periods.  By default,
it returns True and False as 1 and 0 respectively with kwarg 'asint'.

Sources:

Calculation:
    increasing = close.diff(length) > 0
    if asint:
        increasing = increasing.astype(int)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    asint (bool): Returns as binary.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
