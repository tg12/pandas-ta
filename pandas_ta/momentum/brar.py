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
from pandas import DataFrame
from ..utils import get_drift, get_offset, non_zero_range, verify_series


def brar(open_,
         high,
         low,
         close,
         length=None,
         scalar=None,
         drift=None,
         offset=None,
         **kwargs):
    """Indicator: BRAR (BRAR)"""
    # Validate Arguments
    open_ = verify_series(open_)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 26
    scalar = float(scalar) if scalar else 100
    high_open_range = non_zero_range(high, open_)
    open_low_range = non_zero_range(open_, low)
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    hcy = non_zero_range(high, close.shift(drift))
    cyl = non_zero_range(close.shift(drift), low)

    hcy[hcy < 0] = 0  # Zero negative values
    cyl[cyl < 0] = 0  # ""

    ar = scalar * high_open_range.rolling(length).sum()
    ar /= open_low_range.rolling(length).sum()

    br = scalar * hcy.rolling(length).sum()
    br /= cyl.rolling(length).sum()

    # Offset
    if offset != 0:
        ar = ar.shift(offset)
        br = ar.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        ar.fillna(kwargs["fillna"], inplace=True)
        br.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ar.fillna(method=kwargs["fill_method"], inplace=True)
        br.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    _props = f"_{length}"
    ar.name = f"AR{_props}"
    br.name = f"BR{_props}"
    ar.category = br.category = "momentum"

    # Prepare DataFrame to return
    brardf = DataFrame({ar.name: ar, br.name: br})
    brardf.name = f"BRAR{_props}"
    brardf.category = "momentum"

    return brardf


brar.__doc__ = """BRAR (BRAR)

BR and AR

Sources:
    No internet resources on definitive definition.
    Request by Github user homily, issue #46

Calculation:
    Default Inputs:
        length=26, scalar=100
    SUM = Sum

    HO_Diff = high - open
    OL_Diff = open - low
    HCY = high - close[-1]
    CYL = close[-1] - low
    HCY[HCY < 0] = 0
    CYL[CYL < 0] = 0
    AR = scalar * SUM(HO, length) / SUM(OL, length)
    BR = scalar * SUM(HCY, length) / SUM(CYL, length)

Args:
    open_ (pd.Series): Series of 'open's
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): The period.  Default: 26
    scalar (float): How much to magnify.  Default: 100
    drift (int): The difference period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: ar, br columns.
"""
