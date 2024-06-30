import pandas as pd


def preprocess(df, region_df):
    df = df[df["Season"] == "Summer"]
    df = df.merge(region_df, on="NOC", how="left")
    df.drop_duplicates(inplace=True)
    df = df[df["Year"] != 1906]
    df = pd.concat([df, pd.get_dummies(df["Medal"])], axis=1)

    return df
