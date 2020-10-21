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


def obv(close, volume, offset=None, **kwargs):
    """Indicator: On Balance Volume (OBV)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    offset = get_offset(offset)

    # Calculate Result
    signed_volume = signed_series(close, initial=1) * volume
    obv = signed_volume.cumsum()

    # Offset
    if offset != 0:
        obv = obv.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        obv.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        obv.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    obv.name = f"OBV"
    obv.category = "volume"

    return obv


obv.__doc__ = """On Balance Volume (OBV)

On Balance Volume is a cumulative indicator to measure buying and selling
pressure.

Sources:
    https://www.tradingview.com/wiki/On_Balance_Volume_(OBV)
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/on-balance-volume-obv/
    https://www.motivewave.com/studies/on_balance_volume.htm

Calculation:
    signed_volume = signed_series(close, initial=1) * volume
    obv = signed_volume.cumsum()

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
