import numpy as np
import streamlit as st


# NATIONS' MEDAL DISTRIBUTION
def nations_medal_distribution(df, selected_medal_type):
    if selected_medal_type != "All Medals":
        df_filtered = df[df["Medal"] == selected_medal_type]
    else:
        df_filtered = df

    medal_tally = df_filtered.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )
    medal_tally = (
        medal_tally.groupby("region").sum()[["Gold", "Silver", "Bronze"]].reset_index()
    )
    medal_tally["Total"] = (
            medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]
    )
    medal_tally = medal_tally.sort_values("Total", ascending=False)
    medal_tally = medal_tally.head(10)

    return medal_tally


# MOST DECORATED ATHLETES OF THE OLYMPICS
def most_successful_ath_summary(
        df,
        selected_sport,
        selected_country,
):
    temp_df = df.dropna(subset=["Medal"])

    if selected_sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == selected_sport]

    if selected_country != "Overall":
        temp_df = temp_df[temp_df["region"] == selected_country]
    result = (
        temp_df["Name"]
        .value_counts()
        .reset_index()
        .head(15)
        .merge(df, left_on="Name", right_on="Name", how="left")[
            ['Name', 'count', 'Sport', 'region']
        ]
        .drop_duplicates("Name")
    )
    result.rename(
        columns={"count": "Medals", "region": "Country"}, inplace=True
    )
    result = result.reset_index(drop=True)
    result.index += 1

    gold_df = temp_df[temp_df["Medal"] == "Gold"]
    gold_count_df = gold_df.groupby("Name").size().reset_index(name="Gold")
    gold_count_df = gold_count_df.sort_values(by="Gold", ascending=False)
    result["Gold"] = result["Name"].apply(
        lambda x: gold_count_df[gold_count_df["Name"] == x]["Gold"].values[0]
        if x in gold_count_df["Name"].values
        else 0
    )

    silver_df = temp_df[temp_df["Medal"] == "Silver"]
    silver_count_df = silver_df.groupby("Name").size().reset_index(name="Silver")
    silver_count_df = silver_count_df.sort_values(by="Silver", ascending=False)
    result["Silver"] = result["Name"].apply(
        lambda x: silver_count_df[silver_count_df["Name"] == x]["Silver"].values[0]
        if x in silver_count_df["Name"].values
        else 0
    )

    bronze_df = temp_df[temp_df["Medal"] == "Bronze"]
    bronze_count_df = bronze_df.groupby("Name").size().reset_index(name="Bronze")
    bronze_count_df = bronze_count_df.sort_values(by="Bronze", ascending=False)
    result["Bronze"] = result["Name"].apply(
        lambda x: bronze_count_df[bronze_count_df["Name"] == x]["Bronze"].values[0]
        if x in bronze_count_df["Name"].values
        else 0
    )

    return result


# PERCENTAGE OF MISSING VALUES IN THE DATASET
def missing_values(df):
    temp = df.drop(columns=["Gold", "Silver", "Bronze"])
    x = temp.isnull().sum()
    missing_percentage = 100 * (x / len(df))
    missing_percentage_sorted = missing_percentage.sort_values(ascending=False)
    return missing_percentage_sorted


# MEDAL TALLY
def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )
    flag = 0
    if year == "Overall" and country == "Overall":
        temp_df = medal_df
    if year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]
    if year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(year)]
    if year != "Overall" and country != "Overall":
        temp_df = medal_df[
            (medal_df["Year"] == int(year)) & (medal_df["region"] == country)
            ]

    if flag == 1:
        x = (
            temp_df.groupby("Year")
            .sum()[["Gold", "Silver", "Bronze"]]
            .sort_values("Year")
            .reset_index()
        )
        x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]
        x["Year"] = x["Year"].apply(lambda x: "{:.0f}".format(x))
    else:
        x = (
            temp_df.groupby("region")
            .sum()[["Gold", "Silver", "Bronze"]]
            .sort_values("Gold", ascending=False)
            .reset_index()
        )
        x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]

    x["Gold"] = x["Gold"].astype(int)
    x["Silver"] = x["Silver"].astype(int)
    x["Bronze"] = x["Bronze"].astype(int)
    x["total"] = x["total"].astype(int)

    x.rename(columns={"region": "Country", "total": "Total"}, inplace=True)
    x.index += 1
    return x


# MEDAL TALLY
def country_year_list(df):
    years = df["Year"].unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    country = np.unique(df["region"].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")

    return years, country


# GENDER TRENDS IN OLYMPIC PARTICIPATION
def men_v_women(df):
    athlete_df = df.drop_duplicates(subset=["Name", "region", "Year"])
    men = (
        athlete_df[athlete_df["Sex"] == "M"]
        .groupby("Year")
        .count()["Name"]
        .reset_index()
    )
    women = (
        athlete_df[athlete_df["Sex"] == "F"]
        .groupby("Year")
        .count()["Name"]
        .reset_index()
    )
    final = men.merge(women, on="Year", how="left")
    final.rename(columns={"Name_x": "Male", "Name_y": "Female"}, inplace=True)
    final.fillna(0, inplace=True)

    return final


# AGE VARIANCE ACROSS OLYMPIC DISCIPLINES
def dist_age_sports(df, medal):
    athlete_df = df.drop_duplicates(subset=["Name", "region", "Year"])
    famous_sports = [
        "Basketball",
        "Judo",
        "Football",
        "Tug-Of-War",
        "Athletics",
        "Swimming",
        "Badminton",
        "Sailing",
        "Gymnastics",
        "Art Competitions",
        "Handball",
        "Weightlifting",
        "Wrestling",
        "Water Polo",
        "Hockey",
        "Rowing",
        "Fencing",
        "Shooting",
        "Boxing",
        "Taekwondo",
        "Cycling",
        "Diving",
        "Canoeing",
        "Tennis",
        "Golf",
        "Softball",
        "Archery",
        "Volleyball",
        "Synchronized Swimming",
        "Table Tennis",
        "Baseball",
        "Rhythmic Gymnastics",
        "Rugby Sevens",
        "Beach Volleyball",
        "Triathlon",
        "Rugby",
        "Polo",
        "Ice Hockey",
    ]
    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        ages = temp_df[temp_df["Medal"] == medal]["Age"].dropna().tolist()
        if ages:
            x.append(ages)
            name.append(sport)
    return x, name


# AGE DISTRIBUTION ACROSS OLYMPIC EDITIONS
def age_across_editions(df):
    females_df = df[df["Sex"] == "F"]
    females_avg_age = females_df.groupby("Year")["Age"].mean().reset_index()
    females_avg_age.rename(columns={"Age": "Female"}, inplace=True)

    males_df = df[df["Sex"] == "M"]
    males_avg_age = males_df.groupby("Year")["Age"].mean().reset_index()
    males_avg_age.rename(columns={"Age": "Male"}, inplace=True)
    final = females_avg_age.merge(males_avg_age, on="Year", how="left").fillna(0)
    return final


# YOUNGEST OLYMPIANS
def youngest_olympians(df, selected_gender, selected_sport):
    if selected_gender != "All":
        if selected_gender == "Male":
            df = df[df["Sex"] == "M"]
        if selected_gender == "Female":
            df = df[df["Sex"] == "F"]
    if selected_sport != "Overall":
        df = df[df["Sport"] == selected_sport]
    temp = df.dropna(subset=["Age"])
    temp1 = temp[temp["Sport"] != "Art Competitions"].drop_duplicates(
        subset=["Name", "region", "Age"]
    )
    age_df = temp1.sort_values("Age", ascending=True).reset_index(drop=True)
    age_df = age_df[["Name", "Sex", "Age", "region", "Sport"]]
    age_df.rename(columns={"region": "Country"}, inplace=True)
    age_df.index += 1
    age_df["Age"] = age_df["Age"].astype(int)
    age_df = age_df.head(10)
    return age_df


# OLDEST OLYMPIANS
def oldest_olympians(df, selected_gender1, selected_sport1):
    if selected_gender1 != "All":
        if selected_gender1 == "Male":
            df = df[df["Sex"] == "M"]
        if selected_gender1 == "Female":
            df = df[df["Sex"] == "F"]
    if selected_sport1 != "Overall":
        df = df[df["Sport"] == selected_sport1]
    temp = df.dropna(subset=["Age"])
    temp1 = temp[temp["Sport"] != "Art Competitions"].drop_duplicates(
        subset=["Name", "region", "Age"]
    )
    age_df = temp1.sort_values("Age", ascending=False).reset_index(drop=True)
    age_df = age_df[["Name", "Sex", "Age", "region", "Sport"]]
    age_df.rename(columns={"region": "Country"}, inplace=True)
    age_df.index += 1
    age_df["Age"] = age_df["Age"].astype(int)
    age_df = age_df.head(10)
    return age_df


# OLYMPIC METRICS: HEIGHT - WEIGHT INSIGHTS
def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=["Name", "region", "Year"])
    athlete_df["Medal"].fillna("No Medal", inplace=True)
    if sport != "Overall":
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        return temp_df
    else:
        return athlete_df


# EVOLUTION OF OLYMPIC PARTICIPATION
def athletes_over_time(df):
    x = (
        df.drop_duplicates(["Year", "Name"])["Year"]
        .value_counts()
        .reset_index().
        sort_values('Year')
    )
    x.rename(columns={"Year": "Edition", "count": "Athletes"}, inplace=True)

    return x


# OLYMPIC DIVERSITY: NATIONS OVER TIME
def nations_over_time(df):
    x = (
        df.drop_duplicates(["Year", "region"])["Year"]
        .value_counts()
        .reset_index()
        .sort_values("Year")
    )
    x.rename(columns={"Year": "Edition", "count": "No. of Countries"}, inplace=True)

    return x


# OLYMPIC EVENT GROWTH OVER TIME
def events_over_time(df):
    x = (
        df.drop_duplicates(["Year", "Event"])["Year"]
        .value_counts()
        .reset_index()
        .sort_values("Year")
    )
    x.rename(columns={"Year": "Edition", "count": "Events"}, inplace=True)

    return x


# MEDAL DISTRIBUTION THROUGH OLYMPIC EDITIONS
def medal_distribution_over_editions(df):
    gold_medal_distr = (
        df[df["Medal"] == "Gold"].groupby("Year")["Medal"].count().reset_index()
    )
    gold_medal_distr.rename(columns={"Medal": "Gold"}, inplace=True)

    silver_medal_distr = (
        df[df["Medal"] == "Silver"].groupby("Year")["Medal"].count().reset_index()
    )
    silver_medal_distr.rename(columns={"Medal": "Silver"}, inplace=True)

    bronze_medal_distr = (
        df[df["Medal"] == "Bronze"].groupby("Year")["Medal"].count().reset_index()
    )
    bronze_medal_distr.rename(columns={"Medal": "Bronze"}, inplace=True)

    final = gold_medal_distr.merge(silver_medal_distr, on="Year", how="left").merge(
        bronze_medal_distr, on="Year", how="left"
    )
    final.fillna(0, inplace=True)

    return final


# COUNTRY MEDAL TALLY OVER THE YEARS
def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"],
        inplace=True,
    )

    new_df = temp_df[temp_df["region"] == country]
    final_df = new_df.groupby("Year").count()["Medal"].reset_index()

    return final_df


# COUNTRY EXCELS IN THE FOLLOWING SPORTS
def sportwise_country_performance(df, country):
    x = df.dropna(subset=["Medal"])
    x = x.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )
    x = x[x["region"] == country]

    return x


# TOP 10 ATHLETES OF COUNTRY
def most_successful_countrywise(
        df, country, selected_sport, selected_gender, selected_edition
):
    temp_df = df.dropna(subset=["Medal"])

    if selected_edition != "All":
        temp_df = temp_df[temp_df["Year"] == selected_edition]

    if selected_sport == "Overall":
        if selected_gender == "All":
            temp_df = temp_df[temp_df["region"] == country]

        if selected_gender == "Male":
            temp_df = temp_df[(temp_df["region"] == country) & (temp_df["Sex"] == "M")]

        if selected_gender == "Female":
            temp_df = temp_df[(temp_df["region"] == country) & (temp_df["Sex"] == "F")]

    else:
        if selected_gender == "Male":
            temp_df = temp_df[(temp_df["region"] == country) & (temp_df["Sex"] == "M")]

        if selected_gender == "Female":
            temp_df = temp_df[(temp_df["region"] == country) & (temp_df["Sex"] == "F")]

        temp_df = temp_df[
            (temp_df["region"] == country) & (temp_df["Sport"] == selected_sport)
            ]

    counts = temp_df.groupby(["Name", "Sex"]).size().reset_index(name="Medal_Count")

    merged_df = counts.merge(df, on=["Name", "Sex"], how="left")

    top_10 = merged_df.sort_values(by="Medal_Count", ascending=False)

    result = (
        top_10[["Name", "Sex", "Sport", "Medal_Count"]].drop_duplicates("Name").head(10)
    )
    result = result.rename(columns={"Medal_Count": "Total Medals"}).reset_index(
        drop=True
    )
    result.index += 1

    gold_df = temp_df[temp_df["Medal"] == "Gold"]
    gold_count_df = gold_df.groupby("Name").size().reset_index(name="Gold")
    gold_count_df = gold_count_df.sort_values(by="Gold", ascending=False)
    result["Gold"] = result["Name"].apply(
        lambda x: gold_count_df[gold_count_df["Name"] == x]["Gold"].values[0]
        if x in gold_count_df["Name"].values
        else 0
    )

    silver_df = temp_df[temp_df["Medal"] == "Silver"]
    silver_count_df = silver_df.groupby("Name").size().reset_index(name="Silver")
    silver_count_df = silver_count_df.sort_values(by="Silver", ascending=False)
    result["Silver"] = result["Name"].apply(
        lambda x: silver_count_df[silver_count_df["Name"] == x]["Silver"].values[0]
        if x in silver_count_df["Name"].values
        else 0
    )

    bronze_df = temp_df[temp_df["Medal"] == "Bronze"]
    bronze_count_df = bronze_df.groupby("Name").size().reset_index(name="Bronze")
    bronze_count_df = bronze_count_df.sort_values(by="Bronze", ascending=False)
    result["Bronze"] = result["Name"].apply(
        lambda x: bronze_count_df[bronze_count_df["Name"] == x]["Bronze"].values[0]
        if x in bronze_count_df["Name"].values
        else 0
    )

    return result


# OLYMPIC ICONS: THE MOST DECORATED ATHLETES
def most_successful(
        df, sport, selected_gender, selected_country, medal_type, selected_edition
):
    temp_df = df.dropna(subset=["Medal"])

    if selected_edition != "All":
        temp_df = temp_df[temp_df["Year"] == selected_edition]

    if selected_country != "Overall":
        temp_df = temp_df[temp_df["region"] == selected_country]

    if selected_gender != "All":
        if selected_gender == "Male":
            temp_df = temp_df[temp_df["Sex"] == "M"]
        if selected_gender == "Female":
            temp_df = temp_df[temp_df["Sex"] == "F"]

    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]

    if medal_type != "All":
        if medal_type == "Gold":
            temp_df = temp_df[temp_df["Medal"] == "Gold"]
        if medal_type == "Silver":
            temp_df = temp_df[temp_df["Medal"] == "Silver"]
        if medal_type == "Bronze":
            temp_df = temp_df[temp_df["Medal"] == "Bronze"]

    result = (
        temp_df["Name"]
        .value_counts()
        .reset_index()
        .head(15)
        .merge(df, left_on="Name", right_on="Name", how="left")[
            ['Name', 'count', 'Sport', 'region']
        ]
        .drop_duplicates("Name")
    )
    result.rename(
        columns={'count': 'Medals', 'region': 'Country'}, inplace=True
    )
    result = result.reset_index(drop=True)
    result.index += 1

    gold_df = temp_df[temp_df["Medal"] == "Gold"]
    gold_count_df = gold_df.groupby("Name").size().reset_index(name="Gold")
    gold_count_df = gold_count_df.sort_values(by="Gold", ascending=False)
    result["Gold"] = result["Name"].apply(
        lambda x: gold_count_df[gold_count_df["Name"] == x]["Gold"].values[0]
        if x in gold_count_df["Name"].values
        else 0
    )

    silver_df = temp_df[temp_df["Medal"] == "Silver"]
    silver_count_df = silver_df.groupby("Name").size().reset_index(name="Silver")
    silver_count_df = silver_count_df.sort_values(by="Silver", ascending=False)
    result["Silver"] = result["Name"].apply(
        lambda x: silver_count_df[silver_count_df["Name"] == x]["Silver"].values[0]
        if x in silver_count_df["Name"].values
        else 0
    )

    bronze_df = temp_df[temp_df["Medal"] == "Bronze"]
    bronze_count_df = bronze_df.groupby("Name").size().reset_index(name="Bronze")
    bronze_count_df = bronze_count_df.sort_values(by="Bronze", ascending=False)
    result["Bronze"] = result["Name"].apply(
        lambda x: bronze_count_df[bronze_count_df["Name"] == x]["Bronze"].values[0]
        if x in bronze_count_df["Name"].values
        else 0
    )

    return result


# DYNAMICS IN MEDALISTS AND NON - MEDALISTS
def age_distribution(df, selected_dynamic):
    medallists_df = df.dropna(subset=["Medal"])
    non_medallists_df = df[df["Medal"].isna()]

    if selected_dynamic == "Age":
        medallists_stats = medallists_df.groupby("Year")[["Age"]].mean().reset_index()
        non_medallists_stats = (
            non_medallists_df.groupby("Year")[["Age"]].mean().reset_index()
        )
        final = non_medallists_stats.merge(
            medallists_stats, on="Year", suffixes=("_non_medallists", "_medallists")
        )

    elif selected_dynamic == "Height":
        medallists_stats = (
            medallists_df.groupby("Year")[["Height"]].mean().reset_index()
        )
        non_medallists_stats = (
            non_medallists_df.groupby("Year")[["Height"]].mean().reset_index()
        )
        final = non_medallists_stats.merge(
            medallists_stats, on="Year", suffixes=("_non_medallists", "_medallists")
        )

    elif selected_dynamic == "Weight":
        medallists_stats = (
            medallists_df.groupby("Year")[["Weight"]].mean().reset_index()
        )
        non_medallists_stats = (
            non_medallists_df.groupby("Year")[["Weight"]].mean().reset_index()
        )
        final = non_medallists_stats.merge(
            medallists_stats, on="Year", suffixes=("_non_medallists", "_medallists")
        )

    return final


# LEADING OLYMPIC SPORTS / EVENTS IN MEDALS
def leading_medals(df, type):
    temp = (
        df.groupby(type)
        .sum()[["Gold", "Silver", "Bronze"]]
        .sort_values("Gold", ascending=False)
        .reset_index()
    )
    temp["total"] = (temp["Gold"] + temp["Silver"] + temp["Bronze"]).astype(int)
    temp = temp.reset_index(drop=True)
    temp.index += 1
    temp = temp.head(15)
    temp["Gold"] = temp["Gold"].astype(int)
    temp["Silver"] = temp["Silver"].astype(int)
    temp["Bronze"] = temp["Bronze"].astype(int)
    return temp


# OLYMPIC MEDAL LEADERS
def olympic_medal_leaders(df):
    temp = df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )
    temp = (
        temp.groupby("region")
        .sum()[["Gold", "Silver", "Bronze"]]
        .sort_values("Gold", ascending=False)
        .reset_index()
    )
    temp["total"] = temp["Gold"] + temp["Silver"] + temp["Bronze"]
    temp = temp.reset_index(drop=True)
    temp.index += 1
    temp = temp.rename(columns={"region": "Country", "total": "Total"}).head(15)
    temp["Gold"] = temp["Gold"].astype(int)
    temp["Silver"] = temp["Silver"].astype(int)
    temp["Bronze"] = temp["Bronze"].astype(int)
    temp["Total"] = temp["Total"].astype(int)
    return temp


# NATIONS AT THE TOP OF THE PODIUM
def nations_at_top(df):
    city_df = (
        df.drop_duplicates(subset=["Year", "City", "Name"])
        .groupby("Year")["City"]
        .agg(lambda x: ", ".join(x.unique()))
        .reset_index()
    )
    city_df1 = (
        df.drop_duplicates(
            subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
        )
        .groupby("Year")
        .apply(lambda x: x[x["Medal"] == "Gold"]["region"].value_counts().idxmax())
        .rename("Winners")
    )
    city_df = city_df.merge(city_df1, on="Year", how="left")
    multiple_wins = city_df["Winners"].value_counts().reset_index()
    multiple_wins.index += 1
    multiple_wins.rename(
        columns={"count": "Number of wins", "Winners": "Country"}, inplace=True
    )
    return multiple_wins


# NATIONS STILL CHASING MEDALS
def nations_still_chasing(df):
    temp = df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )
    temp = (
        temp.groupby("region")
        .sum()[["Gold", "Silver", "Bronze"]]
        .sort_values("Gold", ascending=False)
        .reset_index()
    )
    temp["total"] = temp["Gold"] + temp["Silver"] + temp["Bronze"]
    temp = temp[temp["total"] == 0]
    temp = temp.rename(columns={"region": "Country", "total": "Total"})
    temp = temp.reset_index(drop=True)
    temp.index += 1
    temp["Gold"] = temp["Gold"].astype(int)
    temp["Silver"] = temp["Silver"].astype(int)
    temp["Bronze"] = temp["Bronze"].astype(int)
    temp["Total"] = temp["Total"].astype(int)
    return temp


# OLYMPIC HOST CITIES
def olympic_host_cities(df):
    city_df = (
        df.drop_duplicates(subset=["Year", "City", "Name"])
        .groupby("Year")["City"]
        .agg(lambda x: ", ".join(x.unique()))
        .reset_index()
    )
    city_df["Athletes"] = (
        df.drop_duplicates(subset=["Year", "City", "Name"])
        .groupby("Year")["Name"]
        .agg("count")
        .values
    )
    city_df1 = (
        df.drop_duplicates(
            subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
        )
        .groupby("Year")
        .apply(lambda x: x[x["Medal"] == "Gold"]["region"].value_counts().idxmax())
        .rename("Winners")
    )

    city_df = city_df.merge(city_df1, on="Year", how="left")

    city_df.rename(columns={"City": "Host Cities", "Name": "Athletes"}, inplace=True)
    city_df.index += 1
    return city_df


# CITIES THAT HAVE HOSTED MULTIPLE GAMES
def multiple_hostings(df):
    host_df = (
        df.drop_duplicates(subset=["Year", "City", "Name"])
        .groupby("Year")["City"]
        .agg(lambda x: ", ".join(x.unique()))
        .reset_index()
    )
    multiple_host_cities = host_df["City"].value_counts()
    multiple_host_cities = multiple_host_cities[multiple_host_cities > 1].reset_index()
    multiple_host_cities.columns = ["City", "No. of times"]
    multiple_host_cities.index += 1
    return multiple_host_cities
