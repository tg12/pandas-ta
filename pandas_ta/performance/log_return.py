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
from numpy import log as nplog
from pandas_ta.utils import get_offset, verify_series


def log_return(close, length=None, cumulative=False, offset=None, **kwargs):
    """Indicator: Log Return"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    log_return = nplog(close).diff(periods=length)

    if cumulative:
        log_return = log_return.cumsum()

    # Offset
    if offset != 0:
        log_return = log_return.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        log_return.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        log_return.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    log_return.name = f"{'CUM' if cumulative else ''}LOGRET_{length}"
    log_return.category = "performance"

    return log_return


log_return.__doc__ = """Log Return

Calculates the logarithmic return of a Series.
See also: help(df.ta.log_return) for additional **kwargs a valid 'df'.

Sources:
    https://stackoverflow.com/questions/31287552/logarithmic-returns-in-pandas-dataframe

Calculation:
    Default Inputs:
        length=1, cumulative=False
    LOGRET = log( close.diff(periods=length) )
    CUMLOGRET = LOGRET.cumsum() if cumulative

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 20
    cumulative (bool): If True, returns the cumulative returns.  Default: False
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
