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
from pandas_ta.overlap import ema, sma
from pandas_ta.utils import get_drift, get_offset, verify_series


def efi(close,
        volume,
        length=None,
        drift=None,
        mamode=None,
        offset=None,
        **kwargs):
    """Indicator: Elder's Force Index (EFI)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    length = int(length) if length and length > 0 else 13
    drift = get_drift(drift)
    mamode = mamode.lower() if mamode else None
    offset = get_offset(offset)

    # Calculate Result
    pv_diff = close.diff(drift) * volume

    if mamode == "sma":
        efi = sma(pv_diff, length)
    else:
        efi = ema(pv_diff, length)

    # Offset
    if offset != 0:
        efi = efi.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        efi.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        efi.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    efi.name = f"EFI_{length}"
    efi.category = "volume"

    return efi


efi.__doc__ = """Elder's Force Index (EFI)

Elder's Force Index measures the power behind a price movement using price
and volume as well as potential reversals and price corrections.

Sources:
    https://www.tradingview.com/wiki/Elder%27s_Force_Index_(EFI)
    https://www.motivewave.com/studies/elders_force_index.htm

Calculation:
    Default Inputs:
        length=20, drift=1, mamode=None
    EMA = Exponential Moving Average
    SMA = Simple Moving Average

    pv_diff = close.diff(drift) * volume
    if mamode == 'sma':
        EFI = SMA(pv_diff, length)
    else:
        EFI = EMA(pv_diff, length)

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    length (int): The short period.  Default: 13
    drift (int): The diff period.   Default: 1
    mamode (str): Two options: None or "sma".  Default: None
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
