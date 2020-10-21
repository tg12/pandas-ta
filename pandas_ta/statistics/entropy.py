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
from numpy import log as npLog
from ..utils import get_offset, verify_series


def entropy(close, length=None, base=None, offset=None, **kwargs):
    """Indicator: Entropy (ENTP)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    base = float(base) if base and base > 0 else 2.0
    offset = get_offset(offset)

    # Calculate Result
    p = close / close.rolling(length).sum()
    entropy = (-p * npLog(p) / npLog(base)).rolling(length).sum()

    # Offset
    if offset != 0:
        entropy = entropy.shift(offset)

    # Name & Category
    entropy.name = f"ENTP_{length}"
    entropy.category = "statistics"

    return entropy


entropy.__doc__ = """Entropy (ENTP)

Introduced by Claude Shannon in 1948, entropy measures the unpredictability
of the data, or equivalently, of its average information. A die has higher
entropy (p=1/6) versus a coin (p=1/2).

Sources:
    https://en.wikipedia.org/wiki/Entropy_(information_theory)

Calculation:
    Default Inputs:
        length=10, base=2

    P = close / SUM(close, length)
    E = SUM(-P * npLog(P) / npLog(base), length)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    base (float): Logarithmic Base.  Default: 2
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
