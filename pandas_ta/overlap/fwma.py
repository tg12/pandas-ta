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
from ..utils import fibonacci, get_offset, verify_series, weights


def fwma(close, length=None, asc=None, offset=None, **kwargs):
    """Indicator: Fibonacci's Weighted Moving Average (FWMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = (int(kwargs["min_periods"]) if "min_periods" in kwargs and
                   kwargs["min_periods"] is not None else length)
    asc = asc if asc else True
    offset = get_offset(offset)

    # Calculate Result
    fibs = fibonacci(n=length, weighted=True)
    fwma = close.rolling(length, min_periods=length).apply(weights(fibs),
                                                           raw=True)

    # Offset
    if offset != 0:
        fwma = fwma.shift(offset)

    # Name & Category
    fwma.name = f"FWMA_{length}"
    fwma.category = "overlap"

    return fwma


fwma.__doc__ = """Fibonacci's Weighted Moving Average (FWMA)

Fibonacci's Weighted Moving Average is similar to a Weighted Moving Average
(WMA) where the weights are based on the Fibonacci Sequence.

Source: Kevin Johnson

Calculation:
    Default Inputs:
        length=10,

    def weights(w):
        def _compute(x):
            return np.dot(w * x)
        return _compute

    fibs = utils.fibonacci(length - 1)
    FWMA = close.rolling(length)_.apply(weights(fibs), raw=True)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    asc (bool): Recent values weigh more.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
