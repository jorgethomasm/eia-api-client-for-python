import datetime
import os
import sys
import polars as pl
import plotly.express as px
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from eia_client import EIAClient

def test_client_backfill_hourly():

    api_key = os.getenv("EIA_API_KEY")
    
   
    client = EIAClient(api_key)

    # API path for DAILY data
    api_path = "electricity/rto/daily-region-sub-ba-data/data/"

    # Parameters
    freq = "daily"

    # Subfilter categories
    facets = {"parent": "CISO", 
              "subba": "SDGE"}
    dt_start = datetime.date(2015, 1, 1)
    dt_end = datetime.date(2025, 1, 31)

    df = client.get_eia_data(api_path=api_path, frequency=freq, facets=facets, start=dt_start, end=dt_end, offset=2000) 
    
    print(f"{df.height} observations returned")
    print(df)
    
    # Create a simple line plot
    df_tz_Arizona =  df.filter(
        (pl.col("timezone") == "Arizona")
    )
    
    fig = px.line(df_tz_Arizona, x='period', y='value', title='EIA Data Visualisation')
    fig.show()
    
    return print(df_tz_Arizona)


if __name__ == "__main__":
    test_client_backfill_hourly()
