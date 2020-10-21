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
from datetime import datetime
from time import perf_counter

from pandas_ta import EXCHANGE_TZ


def final_time(stime):
    time_diff = perf_counter() - stime
    return f"{time_diff * 1000:2.4f} ms ({time_diff:2.4f} s)"


def get_time(exchange: str = "NYSE", to_string: bool = False) -> (None, str):
    tz = EXCHANGE_TZ["NYSE"]  # Default is NYSE (Eastern Time Zone)
    if isinstance(exchange, str):
        exchange = exchange.upper()
        tz = EXCHANGE_TZ[exchange]

    day_of_year = datetime.utcnow().timetuple().tm_yday
    today = datetime.utcnow()
    s = f"Today: {today}, "
    s += f"Day {day_of_year}/365 ({100 * round(day_of_year/365, 2)}%), "
    s += f"{exchange} Time: {(today.timetuple().tm_hour + tz) % 12}:{today.timetuple().tm_min}:{today.timetuple().tm_sec}"
    return s if to_string else print(s)
