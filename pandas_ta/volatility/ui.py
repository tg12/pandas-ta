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
from numpy import sqrt as npsqrt
from pandas_ta.overlap import sma
from ..utils import get_offset, non_zero_range, verify_series


def ui(close, length=None, scalar=None, offset=None, **kwargs):
    """Indicator: Ulcer Index (UI)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    scalar = float(scalar) if scalar and scalar > 0 else 100
    offset = get_offset(offset)

    # Calculate Result
    highest_close = close.rolling(length).max()
    downside = scalar * (close - highest_close)
    downside /= highest_close
    d2 = downside * downside

    everget = kwargs.pop("everget", False)
    if everget:
        # Everget uses SMA instead of SUM for calculation
        ui = (sma(d2, length) / length).apply(npsqrt)
    else:
        ui = (d2.rolling(length).sum() / length).apply(npsqrt)

    # Offset
    if offset != 0:
        ui = ui.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        ui.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ui.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    ui.name = f"UI{'' if not everget else 'e'}_{length}"
    ui.category = "volatility"

    return ui


ui.__doc__ = """Ulcer Index (UI)

The Ulcer Index by Peter Martin measures the downside volatility with the use of
the Quadratic Mean, which has the effect of emphasising large drawdowns.

Sources:
    https://library.tradingtechnologies.com/trade/chrt-ti-ulcer-index.html
    https://en.wikipedia.org/wiki/Ulcer_index
    http://www.tangotools.com/ui/ui.htm

Calculation:
    Default Inputs:
        length=14, scalar=100
    HC = Highest Close
    SMA = Simple Moving Average

    HCN = HC(close, length)
    DOWNSIDE = scalar * (close - HCN) / HCN
    if kwargs["everget"]:
        UI = SQRT(SMA(DOWNSIDE^2, length) / length)
    else:
        UI = SQRT(SUM(DOWNSIDE^2, length) / length)

Args:
    high (pd.Series): Series of 'high's
    close (pd.Series): Series of 'close's
    length (int): The short period.  Default: 14
    scalar (float): A positive float to scale the bands. Default: 100
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method
    everget (value, optional): TradingView's Evergets SMA instead of SUM
        calculation. Default: False

Returns:
    pd.Series: New feature
"""
