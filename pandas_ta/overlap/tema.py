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
from .ema import ema
from ..utils import get_offset, verify_series


def tema(close, length=None, offset=None, **kwargs):
    """Indicator: Triple Exponential Moving Average (TEMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = (int(kwargs["min_periods"]) if "min_periods" in kwargs and
                   kwargs["min_periods"] is not None else length)
    offset = get_offset(offset)

    # Calculate Result
    ema1 = ema(close=close, length=length, **kwargs)
    ema2 = ema(close=ema1, length=length, **kwargs)
    ema3 = ema(close=ema2, length=length, **kwargs)
    tema = 3 * (ema1 - ema2) + ema3

    # Offset
    if offset != 0:
        tema = tema.shift(offset)

    # Name & Category
    tema.name = f"TEMA_{length}"
    tema.category = "overlap"

    return tema


tema.__doc__ = """Triple Exponential Moving Average (TEMA)

A less laggy Exponential Moving Average.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/triple-exponential-moving-average-tema/

Calculation:
    Default Inputs:
        length=10
    EMA = Exponential Moving Average
    ema1 = EMA(close, length)
    ema2 = EMA(ema1, length)
    ema3 = EMA(ema2, length)
    TEMA = 3 * (ema1 - ema2) + ema3

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    adjust (bool): Default: True
    presma (bool, optional): If True, uses SMA for initial value.
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
