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


def ad(high, low, close, volume, open_=None, offset=None, **kwargs):
    """Indicator: Accumulation/Distribution (AD)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    volume = verify_series(volume)
    high_low_range = non_zero_range(high, low)
    offset = get_offset(offset)

    # Calculate Result
    if open_ is not None:
        open_ = verify_series(open_)
        ad = non_zero_range(close, open_)  # AD with Open
    else:
        ad = 2 * close - (high + low)  # AD with High, Low, Close

    ad *= volume / high_low_range
    ad = ad.cumsum()

    # Offset
    if offset != 0:
        ad = ad.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        ad.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ad.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    ad.name = "AD" if open_ is None else "ADo"
    ad.category = "volume"

    return ad


ad.__doc__ = """Accumulation/Distribution (AD)

Accumulation/Distribution indicator utilizes the relative position
of the close to it's High-Low range with volume.  Then it is cumulated.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/accumulationdistribution-ad/

Calculation:
    CUM = Cumulative Sum
    if 'open':
        AD = close - open
    else:
        AD = 2 * close - high - low

    hl_range = high - low
    AD = AD * volume / hl_range
    AD = CUM(AD)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    open (pd.Series): Series of 'open's
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
