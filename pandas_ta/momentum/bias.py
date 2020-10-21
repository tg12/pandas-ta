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
from ..overlap.ema import ema
from ..overlap.hma import hma
from ..overlap.sma import sma
from ..overlap.rma import rma
from ..overlap.wma import wma
from ..utils import get_offset, verify_series, zero


def bias(close, length=None, mamode=None, offset=None, **kwargs):
    """Indicator: Bias (BIAS)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 26
    mamode = mamode.lower() if mamode else None
    offset = get_offset(offset)

    # Calculate Result
    if mamode is None or mamode == "sma":
        ma = sma(close, length=length, **kwargs)
    if mamode == "ema":
        ma = ema(close, length=length, **kwargs)
    if mamode == "hma":
        ma = hma(close, length=length, **kwargs)
    if mamode == "rma":
        ma = rma(close, length=length, **kwargs)
    if mamode == "wma":
        ma = wma(close, length=length, **kwargs)

    bias = (close / ma) - 1

    # Offset
    if offset != 0:
        bias = bias.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        bias.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        bias.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    bias.name = f"BIAS_{ma.name}"
    bias.category = "momentum"

    return bias


bias.__doc__ = """Bias (BIAS)

Rate of change between the source and a moving average.

Sources:
    Few internet resources on definitive definition.
    Request by Github user homily, issue #46

Calculation:
    Default Inputs:
        length=26, MA='sma'

    BIAS = (close - MA(close, length)) / MA(close, length)
         = (close / MA(close, length)) - 1

Args:
    close (pd.Series): Series of 'close's
    length (int): The period.  Default: 26
    mamode (str): Options: 'ema', 'hma', 'rma', 'sma', 'wma'.  Default: 'sma'
    drift (int): The short period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
