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
from ..utils import get_offset, signed_series, verify_series


def pvol(close, volume, offset=None, **kwargs):
    """Indicator: Price-Volume (PVOL)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    offset = get_offset(offset)
    signed = kwargs.pop("signed", False)

    # Calculate Result
    if signed:
        pvol = signed_series(close, 1) * close * volume
    else:
        pvol = close * volume

    # Offset
    if offset != 0:
        pvol = pvol.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        pvol.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        pvol.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    pvol.name = f"PVOL"
    pvol.category = "volume"

    return pvol


pvol.__doc__ = """Price-Volume (PVOL)

Returns a series of the product of price and volume.

Calculation:
    if signed:
        pvol = signed_series(close, 1) * close * volume
    else:
        pvol = close * volume

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    signed (bool): Keeps the sign of the difference in 'close's.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
