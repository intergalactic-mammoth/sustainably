import pandas as pd
import datetime

PRODUCT_SOURCE = 'data/products.csv'
BRAND_SOURCE = 'data/products.csv'
USER_SOURCE = 'data/user/{}.csv'

DATA_TIME_FMT = "%Y-%m-%d %H:%M:%S.%f"


def strip_date_time(date_time_str):
    return datetime.datetime.strptime(date_time_str, DATA_TIME_FMT)


def co2_footprint(user_id, tail_days=5):
    """
    Return the carbon equivalent usage aggregated over each day for the user specified by user_id.

    @rtype:   DataFrame: {
                Cols: [DaysBack, CO2_Eqiv]
              }
    """
    product_sustainability_scores = pd.read_csv(PRODUCT_SOURCE, index_col='Id', header=0, usecols=['Id', 'CO2_Eqiv'])
    user_overview = pd.read_csv(USER_SOURCE.format(user_id), header=0)

    # merge frames
    timestamp_now = datetime.datetime.now()
    user_overview[['CO2_Eqiv', 'DaysBack']] = user_overview.apply(
        lambda row: pd.Series([product_sustainability_scores.loc[row['Id']], timestamp_now.day - strip_date_time(row['datetime']).day]),
        axis=1
    )

    # filer data
    user_overview = user_overview.loc[user_overview['DaysBack'] < tail_days]

    # group and sum
    user_overview = user_overview.groupby("DaysBack")["CO2_Eqiv"].sum()

    return user_overview
