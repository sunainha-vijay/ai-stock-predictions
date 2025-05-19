import os
import pandas as pd
import yfinance as yf
from fredapi import Fred
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Hardcoded FRED API key — replace with your actual key
FRED_API_KEY = '9170ea382526b8770fe5073a73a83d3f'

def get_macro_data(indicator: str, source: str, interval: str = '1d', period: str = '5y') -> pd.DataFrame:
    """
    Fetch macroeconomic data from supported sources.

    Parameters:
        indicator (str): Ticker or identifier of the macroeconomic indicator.
        source (str): Data source ('fred' or 'yfinance').
        interval (str): Data interval (only used for yfinance).
        period (str): Time period (only used for yfinance).

    Returns:
        pd.DataFrame: DataFrame containing date-indexed macroeconomic data.
    """
    if source == 'fred':
        if not FRED_API_KEY:
            logger.error("FRED API key is missing. Cannot proceed with data download.")
            raise ValueError("Missing FRED API key.")

        logger.info(f"Fetching FRED macro data for {indicator}")
        try:
            fred = Fred(api_key=FRED_API_KEY)
            data = fred.get_series(indicator)
            df = pd.DataFrame(data, columns=[indicator])
            df.index.name = 'Date'
            df.reset_index(inplace=True)
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            return df
        except Exception as e:
            logger.error(f"Error fetching data from FRED: {e}")
            raise

    elif source == 'yfinance':
        logger.info(f"Fetching yFinance macro data for {indicator}")
        try:
            data = yf.download(indicator, interval=interval, period=period, progress=False)
            if data.empty:
                logger.warning(f"No data found for {indicator} on yFinance.")
                raise ValueError(f"No data found for {indicator}")
            return data
        except Exception as e:
            logger.error(f"Error fetching data from yFinance: {e}")
            raise

    else:
        logger.error(f"Unsupported data source: {source}")
        raise ValueError(f"Unsupported data source: {source}")
