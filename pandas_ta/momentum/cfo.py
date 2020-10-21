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
from pandas_ta.overlap import linreg
from pandas_ta.utils import get_drift, get_offset, verify_series


def cfo(close, length=None, scalar=None, drift=None, offset=None, **kwargs):
    """Indicator: Chande Forcast Oscillator (CFO)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 9
    scalar = float(scalar) if scalar else 100
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Finding linear regression of Series
    cfo = scalar * (close - linreg(close, length=length, tsf=True))
    cfo /= close

    # Offset
    if offset != 0:
        cfo = cfo.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        cfo.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        cfo.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    cfo.name = f"CFO_{length}"
    cfo.category = "momentum"

    return cfo


cfo.__doc__ = """Chande Forcast Oscillator (CFO)

The Forecast Oscillator calculates the percentage difference between the actual
price and the Time Series Forecast (the endpoint of a linear regression line).

Sources:
    https://www.fmlabs.com/reference/default.htm?url=ForecastOscillator.htm

Calculation:
    Default Inputs:
        length=9, drift=1, scalar=100
    LINREG = Linear Regression

    CFO = scalar * (close - LINERREG(length, tdf=True)) / close

Args:
    close (pd.Series): Series of 'close's
    length (int): The period. Default: 9
    scalar (float): How much to magnify. Default: 100
    drift (int): The short period. Default: 1
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
