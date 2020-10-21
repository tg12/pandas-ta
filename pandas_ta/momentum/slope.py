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
from math import atan, pi
from pandas_ta.utils import get_offset, verify_series


def slope(
    close,
    length=None,
    as_angle=None,
    to_degrees=None,
    vertical=None,
    offset=None,
    **kwargs,
):
    """Indicator: Slope"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 1
    as_angle = True if isinstance(as_angle, bool) else False
    to_degrees = True if isinstance(to_degrees, bool) else False
    offset = get_offset(offset)

    # Calculate Result
    slope = close.diff(length) / length
    if as_angle:
        slope = slope.apply(atan)
        if to_degrees:
            slope *= 180 / pi

    # Offset
    if offset != 0:
        slope = slope.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        slope.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        slope.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    slope.name = (f"SLOPE_{length}" if not as_angle else
                  f"ANGLE{'d' if to_degrees else 'r'}_{length}")
    slope.category = "momentum"

    return slope


slope.__doc__ = """Slope

Returns the slope of a series of length n.  Can convert the slope to angle. Default: slope.

Sources: Algebra I

Calculation:
    Default Inputs:
        length=1
    slope = close.diff(length) / length

    if as_angle:
        slope = slope.apply(atan)
        if to_degrees:
            slope *= 180 / PI

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    as_angle (value, optional): Converts slope to an angle. Default: False
    to_degrees (value, optional): Converts slope angle to degrees. Default: False
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
