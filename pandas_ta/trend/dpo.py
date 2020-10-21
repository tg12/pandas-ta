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
from pandas_ta.overlap import sma
from pandas_ta.utils import get_offset, verify_series


def dpo(close, length=None, centered=True, offset=None, **kwargs):
    """Indicator: Detrend Price Oscillator (DPO)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 20
    offset = get_offset(offset)

    # Calculate Result
    t = int(0.5 * length) + 1
    ma = sma(close, length)

    dpo = close - ma.shift(t)
    if centered:
        dpo = (close.shift(t) - ma).shift(-t)

    # Offset
    if offset != 0:
        dpo = dpo.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        dpo.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        dpo.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    dpo.name = f"DPO_{length}"
    dpo.category = "trend"

    return dpo


dpo.__doc__ = """Detrend Price Oscillator (DPO)

Is an indicator designed to remove trend from price and make it easier to
identify cycles.

Sources:
    https://www.tradingview.com/scripts/detrendedpriceoscillator/
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dpo
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:detrended_price_osci

Calculation:
    Default Inputs:
        length=20, centered=True
    SMA = Simple Moving Average
    t = int(0.5 * length) + 1

    DPO = close.shift(t) - SMA(close, length)
    if centered:
        DPO = DPO.shift(-t)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    centered (bool): Shift the dpo back by int(0.5 * length) + 1.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
