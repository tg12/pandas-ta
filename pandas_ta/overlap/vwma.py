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
from .sma import sma
from ..utils import get_offset, verify_series


def vwma(close, volume, length=None, offset=None, **kwargs):
    """Indicator: Volume Weighted Moving Average (VWMA)"""
    # Validate Arguments
    close = verify_series(close)
    volume = verify_series(volume)
    length = int(length) if length and length > 0 else 10
    offset = get_offset(offset)

    # Calculate Result
    pv = close * volume
    vwma = sma(close=pv, length=length) / sma(close=volume, length=length)

    # Offset
    if offset != 0:
        vwma = vwma.shift(offset)

    # Name & Category
    vwma.name = f"VWMA_{length}"
    vwma.category = "overlap"

    return vwma


vwma.__doc__ = """Volume Weighted Moving Average (VWMA)

Volume Weighted Moving Average.

Sources:
    https://www.motivewave.com/studies/volume_weighted_moving_average.htm

Calculation:
    Default Inputs:
        length=10
    SMA = Simple Moving Average
    pv = close * volume
    VWMA = SMA(pv, length) / SMA(volume, length)

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
