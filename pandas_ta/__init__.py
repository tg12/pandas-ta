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



name = "pandas_ta"
"""
.. moduleauthor:: Kevin Johnson
"""
from pkg_resources import get_distribution, DistributionNotFound
import os.path

try:
    _dist = get_distribution("pandas_ta")
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, "pandas_ta")):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = "Please install this project with setup.py"
else:
    __version__ = _dist.version

from importlib.util import find_spec

Imports = {
    "scipy": find_spec("scipy") is not None,
    "sklearn": find_spec("sklearn") is not None,
    "statsmodels": find_spec("statsmodels") is not None,
    "mplfinance": find_spec("mplfinance") is not None,
    "alphaVantage-api ": find_spec("alphaVantageAPI") is not None,
    "yfinance": find_spec("yfinance") is not None,
    "talib": find_spec("talib") is not None,
}

# Not ideal and not dynamic but it works.
# Will find a dynamic solution later.
Category = {
    # Candles
    "candles": ["cdl_doji", "cdl_inside", "ha"],
    # Momentum
    "momentum": [
        "ao",
        "apo",
        "bias",
        "bop",
        "brar",
        "cci",
        "cfo",
        "cg",
        "cmo",
        "coppock",
        "er",
        "eri",
        "fisher",
        "inertia",
        "kdj",
        "kst",
        "macd",
        "mom",
        "pgo",
        "ppo",
        "psl",
        "pvo",
        "roc",
        "rsi",
        "rvgi",
        "slope",
        "smi",
        "squeeze",
        "stoch",
        "stochrsi",
        "trix",
        "tsi",
        "uo",
        "willr",
    ],
    # Overlap
    "overlap": [
        "dema",
        "ema",
        "fwma",
        "hilo",
        "hl2",
        "hlc3",
        "hma",
        "ichimoku",
        "kama",
        "linreg",
        "midpoint",
        "midprice",
        "ohlc4",
        "pwma",
        "rma",
        "sinwma",
        "sma",
        "supertrend",
        "swma",
        "t3",
        "tema",
        "trima",
        "vwap",
        "vwma",
        "wcp",
        "wma",
        "zlma",
    ],
    # Performance
    "performance": ["log_return", "percent_return", "trend_return"],
    # Statistics
    "statistics": [
        "entropy",
        "kurtosis",
        "mad",
        "median",
        "quantile",
        "skew",
        "stdev",
        "variance",
        "zscore",
    ],
    # Trend
    "trend": [
        "adx",
        "amat",
        "aroon",
        "chop",
        "cksp",
        "decay",
        "decreasing",
        "dpo",
        "increasing",
        "long_run",
        "psar",
        "qstick",
        "short_run",
        "ttm_trend",
        "vortex",
    ],
    # Volatility
    "volatility": [
        "aberration",
        "accbands",
        "atr",
        "bbands",
        "donchian",
        "kc",
        "massi",
        "natr",
        "pdist",
        "rvi",
        "true_range",
        "ui",
    ],
    # Volume, "vp" or "Volume Profile" is unique
    "volume": [
        "ad",
        "adosc",
        "aobv",
        "cmf",
        "efi",
        "eom",
        "mfi",
        "nvi",
        "obv",
        "pvi",
        "pvol",
        "pvt",
    ],
}

# https://www.worldtimezone.com/markets24.php
EXCHANGE_TZ = {
    "NZSX": 12,
    "ASX": 11,
    "TSE": 9,
    "HKE": 8,
    "SSE": 8,
    "SGX": 8,
    "NSE": 5.5,
    "DIFX": 4,
    "RTS": 3,
    "JSE": 2,
    "FWB": 1,
    "LSE": 1,
    "BMF": -2,
    "NYSE": -4,
    "TSX": -4,
}

RATE = {
    "TRADING_DAYS_PER_YEAR": 252,  # Keep even
    "TRADING_HOURS_PER_DAY": 6.5,
    "MINUTES_PER_HOUR": 60,
}

from pandas_ta.core import *
