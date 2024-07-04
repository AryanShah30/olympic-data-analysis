import streamlit as st
import helper
import preprocessor
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

df = preprocessor.preprocess(df, region_df)

st.set_page_config(page_title="Olympics Analysis", page_icon="🏅", layout="wide")
st.sidebar.header("From Athens to Rio")
st.sidebar.image("images.png")

with st.sidebar:
    user_menu = option_menu(
        None,
        [
            "Table of Contents",
            "Executive Summary",
            "Medal Census",
            "Athlete Demographics",
            "Temporal Analysis",
            "Geographical Analysis",
            "Performance Analysis",
            "Medal Analysis",
            "Location Analysis",
            "Connect"
        ],
        icons=[
            "list",
            "file-text",
            "bar-chart",
            "people",
            "clock",
            "geo-alt",
            "speedometer",
            "trophy",
            "map",
            "person-lines-fill"
        ],
        default_index=0,
    )

sport_list = df["Sport"].unique().tolist()
sport_list.sort()
sport_list.insert(0, "Overall")

country_list = df["region"].dropna().unique().tolist()
country_list.sort()
country_list.insert(0, "Overall")

years = df["Year"].unique().tolist()
years.sort()
years.insert(0, "All")

# TABLE OF CONTENTS
if user_menu == "Table of Contents":
    st.header("Summer Olympics Analysis")
    st.markdown("---")
    
    st.subheader("📜 Overview")
    st.write(
        '''
        Explore the world of Olympic Analysis, delving into over a century of athletic excellence from the inaugural games in 1896 to the modern spectacles of 2016. This comprehensive analysis covers key facets including the Executive Summary, Medal Census, Athlete Demographics, Temporal and Geographical Insights, Performance Analysis, Medal Dynamics, and Location Impact.

        Navigate through our interactive sidebar to uncover trends such as shifts in Olympic participation by gender, the emergence of dominant sporting dynasties, and the cultural impacts of host cities. Discover the achievements of nations through their medal tallies and explore the unforgettable performances that define Olympic history.

        Whether you're a sports enthusiast, data analyst, or researcher, these tools offer an insightful journey through Olympic history—a tribute to excellence, resilience, and the spirit of competition.
        '''
    )

    st.markdown("---")
    st.subheader("📄 Executive Summary")
    st.write("- Top Statistics")
    st.write("- Nations' Medal Distribution")
    st.write("- Most Decorated Athletes of the Olympics")
    st.write("- Percentage of Missing Values in the Dataset")
    st.markdown("---")

    st.subheader("🏅 Medal Census")
    st.write("- Medal Tally")
    st.markdown("---")

    st.subheader("🏌️‍♂️ Athlete Demographics")
    st.write("- Gender Trends in Olympic Participation")
    st.write("- Medal-Winning Age Groups in Olympics")
    st.write("- Age Variance Across Olympic Disciplines")
    st.write("- Age Distribution Across Olympic Editions")
    st.write("- Youngest Olympians")
    st.write("- Oldest Olympians")
    st.write("- Olympic Metrics: Height-Weight Insights")
    st.markdown("---")

    st.subheader("⏳ Temporal Analysis")
    st.write("- Evolution of Olympic Participation")
    st.write("- Olympic Diversity: Nations Over Time")
    st.write("- Olympic Event Growth Over Time")
    st.write("- A Historical Timeline of Olympic Sports")
    st.write("- Medal Distribution through Olympic Editions")
    st.markdown("---")

    st.subheader("🌍 Geographical Analysis")
    st.write("- Country Medal Tally over the years")
    st.write("- Country excels in the following sports")
    st.write("- Top 10 Athletes of Country")
    st.markdown("---")

    st.subheader("🏃 Performance Analysis")
    st.write("- Olympic Icons: The Most Decorated Athletes")
    st.write("- Medal-Producing Olympic Sports")
    st.write("- Medal Timeline of Olympic Sports")
    st.markdown("---")

    st.subheader("🥇 Medal Analysis")
    st.write("- Dynamics in Medalists and Non-Medalists")
    st.write("- Leading Olympic Sports in Medals")
    st.write("- Leading Olympic Events in Medals")
    st.write("- Olympic Medal Leaders")
    st.write("- Nations at the Top of the Podium")
    st.write("- Nations' Medal Distribution")
    st.write("- Nations Still Chasing Medals")
    st.markdown("---")

    st.subheader("🗺️ Location Analysis")
    st.write("- Olympic Host Cities")
    st.write("- Cities that have Hosted Multiple Games")
    st.markdown("---")
    st.markdown("""
    <div style='color: gray; font-size: 15px;'>
        Last updated on 07/06/2024.
    </div>
    """, unsafe_allow_html=True)

# EXECUTIVE SUMMARY
if user_menu == "Executive Summary":

    # TOP STATISTICS
    st.title("Top Statistics")
    editions = df["Year"].unique().shape[0]
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    events = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    nations = df["region"].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    st.text("")
    st.text("")
    st.text("")
    st.text("")

    # NATIONS' MEDAL DISTRIBUTION
    st.subheader("Nations' Medal Distribution")

    selected_medal_type = st.selectbox(
        "Select a medal type", ("All Medals", "Gold", "Silver", "Bronze")
    )

    medal_tally = helper.nations_medal_distribution(df, selected_medal_type)

    if selected_medal_type == "All Medals":
        fig = px.pie(medal_tally, names="region", values="Total")
    else:
        medal_tally = (
            medal_tally.sort_values(selected_medal_type, ascending=False)
            .reset_index(drop=True)
            .head(10)
        )
        medal_tally = medal_tally.head(10)
        fig = px.pie(medal_tally, names="region", values=selected_medal_type)
    st.plotly_chart(fig)

    # MOST DECORATED ATHLETES OF THE OLYMPICS
    st.subheader(f"Most Decorated Athletes of the Olympics")
    selected_sport = st.selectbox("Select a sport", sport_list, key="summary_sport")
    selected_country = st.selectbox(
        "Select a country", country_list, key="summary_country"
    )

    x = helper.most_successful_ath_summary(
        df,
        selected_sport,
        selected_country,
    )
    st.table(x)

    # PERCENTAGE OF MISSING VALUES IN THE DATASET
    st.subheader("Percentage of Missing Values in the Dataset")
    missing_percentage_sorted = helper.missing_values(df)
    fig = px.bar(
        missing_percentage_sorted,
        x=missing_percentage_sorted.index,
        y=missing_percentage_sorted.values,
    )
    fig.update_layout(xaxis_title="Data", yaxis_title="Percentage")
    st.plotly_chart(fig)

# MEDAL CENSUS
if user_menu == "Medal Census":

    # MEDAL TALLY
    st.title("Medal Census")

    years, country = helper.country_year_list(df)

    selected_year = st.selectbox("Select Year", years, key="medal_year")
    selected_country = st.selectbox("Select Country", country, key="medal_country")

    if selected_year == "Overall" and selected_country == "Overall":
        st.subheader("Overall Medal Tally")
    elif selected_year != "Overall" and selected_country == "Overall":
        st.subheader("Medal Tally in " + str(selected_year))
    elif selected_year == "Overall" and selected_country != "Overall":
        st.subheader(selected_country + " Overall Performance")
    else:
        st.subheader(selected_country + " Performance in " + str(selected_year))

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    st.table(medal_tally)

# ATHLETE DEMOGRAPHICS
if user_menu == "Athlete Demographics":
    st.title("Athlete Demographics")

    # GENDER TRENDS IN OLYMPIC PARTICIPATION
    st.subheader("Gender Trends in Olympic Participation")
    final = helper.men_v_women(df)
    fig = px.line(
        final,
        x="Year",
        y=["Male", "Female"],
        labels={"variable": "Sex", "value": "Number"},
        markers=True,
    )
    fig.update_layout(yaxis_title="Number of athletes")
    st.plotly_chart(fig)

    # MEDAL - WINNING AGE GROUPS IN OLYMPICS
    st.subheader("Medal-Winning Age Groups in Olympics")
    athlete_df = df.drop_duplicates(subset=["Name", "region", "Year"])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()
    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ["Overall Age", "Gold Medallist", "Silver Medallist", "Bronze Medallist"],
        show_hist=False,
        show_rug=False,
    )
    fig.update_layout(xaxis_title="Age")
    st.plotly_chart(fig)

    # AGE VARIANCE ACROSS OLYMPIC DISCIPLINES
    st.subheader("Age Variance Across Olympic Disciplines")
    selected_medal = st.selectbox("Select medal type", ("Gold", "Silver", "Bronze"))
    x, name = helper.dist_age_sports(athlete_df, selected_medal)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(xaxis_title="Age")
    st.plotly_chart(fig)

    # AGE DISTRIBUTION ACROSS OLYMPIC EDITIONS
    st.subheader("Age Distribution Across Olympic Editions")
    final = helper.age_across_editions(df)
    fig = px.line(
        final,
        x="Year",
        y=["Male", "Female"],
        labels={"value": "Age", "variable": "Sex"},
        markers=True,
    )
    fig.update_layout(xaxis_title="Year", yaxis_title="Age")
    st.plotly_chart(fig)

    # YOUNGEST OLYMPIANS
    st.subheader("Youngest Olympians")

    selected_gender = st.selectbox(
        "Select a gender", ("All", "Male", "Female"), key="youngest_gender_select"
    )
    selected_sport = st.selectbox(
        "Select a sport", sport_list, key="youngest_sport_select"
    )
    age_df = helper.youngest_olympians(df, selected_gender, selected_sport)
    st.table(age_df)

    # OLDEST OLYMPIANS
    st.subheader("Oldest Olympians")

    selected_gender1 = st.selectbox(
        "Select a gender", ("All", "Male", "Female"), key="older_gender_select"
    )
    selected_sport1 = st.selectbox(
        "Select a sport", sport_list, key="oldest_sport_select"
    )
    age_df = helper.oldest_olympians(df, selected_gender1, selected_sport1)
    st.table(age_df)

    # OLYMPIC METRICS: HEIGHT - WEIGHT INSIGHTS
    st.subheader(f"Olympic Metrics: Height-Weight Insights")

    selected_sport1 = st.selectbox("Select a sport", sport_list, key="sport1")
    temp_df = helper.weight_v_height(df, selected_sport1)
    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(13, 7))
    ax = sns.scatterplot(x="Weight", y="Height", data=temp_df, hue="Medal", style="Sex")
    st.pyplot(fig)

# TEMPORAL ANALYSIS
if user_menu == "Temporal Analysis":
    st.title("Temporal Analysis")

    # EVOLUTION OF OLYMPIC PARTICIPATION
    st.subheader("Evolution of Olympic Participation")
    athletes_over_time = helper.athletes_over_time(df)
    fig = px.line(athletes_over_time, x="Edition", y="Athletes", markers=True)
    fig.update_layout(xaxis_title="Year")
    st.plotly_chart(fig)

    # OLYMPIC DIVERSITY: NATIONS OVER TIME
    st.subheader("Olympic Diversity: Nations Over Time")
    nations_over_time = helper.nations_over_time(df)
    fig = px.line(nations_over_time, x="Edition", y="No. of Countries", markers=True)
    fig.update_layout(xaxis_title="Year")
    st.plotly_chart(fig)

    # OLYMPIC EVENT GROWTH OVER TIME
    st.subheader("Olympic Event Growth Over Time")
    events_over_time = helper.events_over_time(df)
    fig = px.line(events_over_time, x="Edition", y="Events", markers=True)
    fig.update_layout(xaxis_title="Year")
    fig.update_layout(yaxis_title="No. of Editions")
    st.plotly_chart(fig)

    # A HISTORICAL TIMELINE OF OLYMPIC SPORTS
    st.subheader("A Historical Timeline of Olympic Sports")
    fig, ax = plt.subplots(figsize=(20, 25))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    ax = sns.heatmap(
        x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count")
        .fillna(0)
        .astype(int),
        annot=True,
    )
    st.pyplot(fig)

    # MEDAL DISTRIBUTION THROUGH OLYMPIC EDITIONS
    st.subheader("Medal Distribution through Olympic Editions")
    final = helper.medal_distribution_over_editions(df)
    fig = px.bar(
        final,
        x="Year",
        y=["Gold", "Silver", "Bronze"],
        labels={"value": "No. of Medals", "variable": "Medal Type"},
        barmode="group",
    )
    st.plotly_chart(fig)

# GEOGRAPHICAL ANALYSIS
if user_menu == "Geographical Analysis":

    # COUNTRY MEDAL TALLY OVER THE YEARS
    country_list3 = df["region"].dropna().unique().tolist()
    country_list3.sort()
    selected_country = st.selectbox("Select Country", country_list3, key="geo_country")

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal", markers=True)
    fig.update_layout(yaxis_title="Medals")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    # COUNTRY EXCELS IN THE FOLLOWING SPORTS
    st.title(f"{selected_country} excels in the following sports")
    fig, ax = plt.subplots(figsize=(20, 25))
    x = helper.sportwise_country_performance(df, selected_country)
    if x.empty:
        st.write(f"No data available for {selected_country}")
    else:
        ax = sns.heatmap(
            x.pivot_table(
                index="Sport", columns="Year", values="Event", aggfunc="count"
            )
            .fillna(0)
            .astype(int),
            annot=True,
        )
        st.pyplot(fig)

    # TOP 10 ATHLETES OF COUNTRY
    st.title(f"Top 10 Athletes of {selected_country}")
    selected_sport = st.selectbox("Select a sport", sport_list, key="top10_sport")
    selected_edition = st.selectbox("Select an edition", years, key="top10_edition")
    selected_gender = st.selectbox(
        "Select a gender", ("All", "Male", "Female"), key="top10_gender"
    )
    x = helper.most_successful_countrywise(
        df, selected_country, selected_sport, selected_gender, selected_edition
    )
    st.table(x)

# PERFORMANCE ANALYSIS
if user_menu == "Performance Analysis":
    st.title("Performance Analysis")

    # OLYMPIC ICONS: THE MOST DECORATED ATHLETES
    st.subheader(f"Olympic Icons: The Most Decorated Athletes")

    selected_sport = st.selectbox(
        "Select a sport", sport_list, key="most_decorated_ath_sport"
    )
    selected_country = st.selectbox(
        "Select a country", country_list, key="most_decorated_ath_country"
    )
    selected_edition = st.selectbox(
        "Select an edition", years, key="most_decorated_ath_edition"
    )
    selected_gender = st.selectbox(
        "Select a gender", ("All", "Male", "Female"), key="most_decorated_ath_gender"
    )
    medal_type = st.selectbox(
        "Select medal type",
        ("All Medals", "Gold", "Silver", "Bronze"),
        key="most_decorated_ath_medal_type",
    )

    x = helper.most_successful(
        df,
        selected_sport,
        selected_gender,
        selected_country,
        medal_type,
        selected_edition,
    )
    st.table(x)

    # MEDAL - PRODUCING OLYMPIC SPORTS
    st.subheader("Medal-Producing Olympic Sports")

    selected_edition = st.selectbox("Select an edition", years, key="edition_selectbox")
    if selected_edition != "All":
        df = df[df["Year"] == selected_edition]
    sport_distributions = df.groupby("Sport")["Medal"].count().reset_index()
    fig = px.bar(sport_distributions, x="Medal", y="Sport")
    fig.update_layout(xaxis_title="Medals")
    fig.update_layout(
        autosize=False,
        width=1000,
        height=1000,
    )
    st.plotly_chart(fig)

    # MEDAL TIMELINE OF OLYMPIC SPORTS
    st.subheader("Medal Timeline of Olympic Sports")
    fig, ax = plt.subplots(figsize=(20, 25))
    x = df
    ax = sns.heatmap(
        x.pivot_table(index="Sport", columns="Year", values="Medal", aggfunc="count")
        .fillna(0)
        .astype(int),
        annot=True,
        fmt="d",
    )
    st.pyplot(fig)

# MEDAL ANALYSIS
if user_menu == "Medal Analysis":
    st.title("Medal Analysis")

    # DYNAMICS IN MEDALISTS AND NON - MEDALISTS
    st.subheader("Dynamics in Medalists and Non-Medalists")
    selected_dynamic = st.selectbox(
        "Select a dynamic", ("Age", "Height", "Weight"), key="dyanmics"
    )
    final = helper.age_distribution(df, selected_dynamic)
    if selected_dynamic == "Age":
        fig = px.bar(
            final,
            x="Year",
            y=["Age_non_medallists", "Age_medallists"],
            barmode="group",
            labels={"value": "Mean Value", "variable": "Statistic"},
        )
        fig.update_traces(name="Medalist", selector=dict(name="Age_medallists"))
        fig.update_traces(name="Non Medalist", selector=dict(name="Age_non_medallists"))

    elif selected_dynamic == "Height":
        fig = px.bar(
            final,
            x="Year",
            y=["Height_non_medallists", "Height_medallists"],
            barmode="group",
            labels={"value": "Mean Value", "variable": "Statistic"},
        )
        fig.update_traces(name="Medalist", selector=dict(name="Height_medallists"))
        fig.update_traces(
            name="Non Medalist", selector=dict(name="Height_non_medallists")
        )

    elif selected_dynamic == "Weight":
        fig = px.bar(
            final,
            x="Year",
            y=["Weight_non_medallists", "Weight_medallists"],
            barmode="group",
            labels={"value": "Mean Value", "variable": "Statistic"},
        )
        fig.update_traces(name="Medalist", selector=dict(name="Weight_medallists"))
        fig.update_traces(
            name="Non Medalist", selector=dict(name="Weight_non_medallists")
        )

    st.plotly_chart(fig)

    # LEADING OLYMPIC SPORTS IN MEDALS
    st.subheader("Leading Olympic Sports in Medals")
    temp = helper.leading_medals(df, "Sport")
    st.table(temp)

    # LEADING OLYMPIC EVENTS IN MEDALS
    st.subheader("Leading Olympic Events in Medals")
    temp = helper.leading_medals(df, "Event")
    st.table(temp)

    # OLYMPIC MEDAL LEADERS
    st.subheader("Olympic Medal Leaders")
    temp = helper.olympic_medal_leaders(df)
    st.table(temp)

    # NATIONS AT THE TOP OF THE PODIUM
    st.subheader("Nations at the Top of the Podium")
    multiple_wins = helper.nations_at_top(df)
    fig = px.bar(multiple_wins, x="Country", y="Number of wins")
    st.plotly_chart(fig)

    # NATIONS' MEDAL DISTRIBUTION
    st.subheader("Nations' Medal Distribution")
    selected_medal_type = st.selectbox(
        "Select a medal type",
        ("All Medals", "Gold", "Silver", "Bronze"),
        key="nation_medal_dis",
    )

    medal_tally = helper.nations_medal_distribution(df, selected_medal_type)

    if selected_medal_type == "All Medals":
        fig = px.pie(medal_tally, names="region", values="Total")
    else:
        medal_tally = (
            medal_tally.sort_values(selected_medal_type, ascending=False)
            .reset_index(drop=True)
            .head(10)
        )
        medal_tally = medal_tally.head(10)
        fig = px.pie(medal_tally, names="region", values=selected_medal_type)
    st.plotly_chart(fig)

    # NATIONS STILL CHASING MEDALS
    st.subheader("Nations Still Chasing Medals")
    temp = helper.nations_still_chasing(df)
    st.table(temp)

# LOCATION ANALYSIS
if user_menu == "Location Analysis":
    st.title("Location Analysis")

    # OLYMPIC HOST CITIES
    st.subheader("Olympic Host Cities")
    city_df = helper.olympic_host_cities(df)
    fig = px.scatter(city_df, x="Athletes", y="Host Cities", text="Year")
    fig.update_traces(textposition="top center")
    fig.update_layout(
        autosize=False,
        width=800,
        height=800,
    )
    st.plotly_chart(fig)
    st.table(city_df)

    # CITIES THAT HAVE HOSTED MULTIPLE GAMES
    st.subheader("Cities that have Hosted Multiple Games")
    multiple_host_cities = helper.multiple_hostings(df)
    fig = px.bar(multiple_host_cities, x="City", y="No. of times")
    fig.update_traces(width=0.5)
    st.plotly_chart(fig)


if user_menu == "Connect":
    import streamlit as st

    st.title("Connect with Me")
    st.markdown("""
        Feel free to reach out to me via email or connect with me on LinkedIn and GitHub! 💬
    """)
    st.write("")

    st.subheader("Contact Information 📩")
    st.write("**Name:** Aryan Shah")
    st.write("**Email:** aryanshah1957@gmail.com")
    st.write("")

    st.subheader("Social Media 🌍")
    st.write("[LinkedIn](https://www.linkedin.com/in/aryanashah/) 🔗")
    st.write("[GitHub](https://github.com/AryanShah30) 🔗")
