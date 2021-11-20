import pandas as pd
import datetime

PRODUCT_SOURCE = 'data/products.csv'
BRAND_SOURCE = 'data/products.csv'
USER_SOURCE = 'data/user/{}.csv'

DATA_TIME_FMT = "%Y-%m-%d %H:%M:%S.%f"


def strip_date_time(date_time_str):
    return datetime.datetime.strptime(date_time_str, DATA_TIME_FMT)


def sustainability_score_to_label(score):
    return "Bad" if score < 0.35 else "Okay" if score < 0.48 else "Good"


def co2_footprint(user_id, tail_days=5):
    """
    Return the carbon equivalent usage aggregated over each day for the user specified by user_id.

    @rtype:   DataFrame: {
                Cols: [DaysBack, CO2_Eqiv]
              }
    """
    product_sustainability_scores = pd.read_csv(PRODUCT_SOURCE, index_col='Id', header=0, usecols=['Id', 'CO2_Eqiv'])
    co2_overview = pd.read_csv(USER_SOURCE.format(user_id), header=0)

    # merge frames
    timestamp_now = datetime.datetime.now()
    co2_overview[['CO2_Eqiv', 'DaysBack']] = co2_overview.apply(
        lambda row: pd.Series([
            product_sustainability_scores.loc[row['Id']],
            timestamp_now.day - strip_date_time(row['datetime']).day
        ]),
        axis=1
    )

    # filer data temporally
    co2_overview = co2_overview.loc[co2_overview['DaysBack'] < tail_days]

    # group and sum
    co2_overview = co2_overview.groupby("DaysBack")["CO2_Eqiv"].sum()

    return co2_overview


def product_sustainability_breakdown(user_id, tail_days=5):
    """
    Return the breakdown eof purchases of user given by user_id.

    @rtype:   pandas.Series: {
                Cols: [Sustainably_Label, Count]
              }
              Type: Good/Okay/Bad
    """
    product_sustainability_scores = pd.read_csv(PRODUCT_SOURCE, index_col='Id', header=0, usecols=['Id', 'Sustainably_Score'])
    sustainability_breakdown = pd.read_csv(USER_SOURCE.format(user_id), header=0)

    # merge frames
    timestamp_now = datetime.datetime.now()
    sustainability_breakdown[['Sustainably_Score', 'Sustainably_Label', 'DaysBack']] = sustainability_breakdown.apply(
        lambda row: pd.Series([
            product_sustainability_scores.loc[row['Id']],
            sustainability_score_to_label(float(product_sustainability_scores.loc[row['Id']])),
            timestamp_now.day - strip_date_time(row['datetime']).day
        ]),
        axis=1
    )

    # filer data temporally
    sustainability_breakdown = sustainability_breakdown.loc[sustainability_breakdown['DaysBack'] < tail_days]

    # group and sum
    sustainability_breakdown = sustainability_breakdown.groupby("Sustainably_Label").size()

    return sustainability_breakdown
