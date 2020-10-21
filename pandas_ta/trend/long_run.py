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
from .decreasing import decreasing
from .increasing import increasing
from pandas_ta.utils import get_offset, verify_series


def long_run(fast, slow, length=None, offset=None, **kwargs):
    """Indicator: Long Run"""
    # Validate Arguments
    fast = verify_series(fast)
    slow = verify_series(slow)
    length = int(length) if length and length > 0 else 2
    offset = get_offset(offset)

    # Calculate Result
    pb = increasing(fast, length) & decreasing(
        slow, length)  # potential bottom or bottom
    bi = increasing(fast, length) & increasing(
        slow, length)  # fast and slow are increasing
    long_run = pb | bi

    # Offset
    if offset != 0:
        long_run = long_run.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        long_run.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        long_run.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    long_run.name = f"LR_{length}"
    long_run.category = "trend"

    return long_run
