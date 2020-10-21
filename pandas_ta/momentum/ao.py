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
from ..utils import get_offset, verify_series


def ao(high, low, fast=None, slow=None, offset=None, **kwargs):
    """Indicator: Awesome Oscillator (AO)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    fast = int(fast) if fast and fast > 0 else 5
    slow = int(slow) if slow and slow > 0 else 34
    if slow < fast:
        fast, slow = slow, fast
    min_periods = (int(kwargs["min_periods"]) if "min_periods" in kwargs and
                   kwargs["min_periods"] is not None else fast)
    offset = get_offset(offset)

    # Calculate Result
    median_price = 0.5 * (high + low)
    fast_sma = median_price.rolling(fast, min_periods=min_periods).mean()
    slow_sma = median_price.rolling(slow, min_periods=min_periods).mean()
    ao = fast_sma - slow_sma

    # Offset
    if offset != 0:
        ao = ao.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        ao.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ao.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    ao.name = f"AO_{fast}_{slow}"
    ao.category = "momentum"

    return ao


ao.__doc__ = """Awesome Oscillator (AO)

The Awesome Oscillator is an indicator used to measure a security's momentum.
AO is generally used to affirm trends or to anticipate possible reversals.

Sources:
    https://www.tradingview.com/wiki/Awesome_Oscillator_(AO)
    https://www.ifcm.co.uk/ntx-indicators/awesome-oscillator

Calculation:
    Default Inputs:
        fast=5, slow=34
    SMA = Simple Moving Average
    median = (high + low) / 2
    AO = SMA(median, fast) - SMA(median, slow)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    fast (int): The short period.  Default: 5
    slow (int): The long period.   Default: 34
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
