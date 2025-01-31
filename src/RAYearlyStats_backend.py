# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10

@author: jorloru
"""

# Libraries for API usage

import time
import requests
import datetime, calendar

# Libraries for data manipulation

import numpy as np
import pandas as pd

# Libraries for plotting

from PIL import Image
from io import BytesIO

import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Basic functions

def get_game_ids(df_historic: pd.DataFrame) -> np.array:
    
    """
    Returns all the game IDs contained in a DataFrame containing the user's metadata.
    
    Parameters:

        df (pandas.DataFrame):
            A DataFrame containing the user's RA metadata.

    Returns:
        
        numpy.array (dtype=int):
            Array containing all the game IDs.
    """

    return df_historic["GameID"].unique()

def get_game_title(game_id: int, df_games_data: pd.DataFrame) -> str:
    
    """
    Returns all the game IDs contained in a DataFrame containing the user's metadata.
    
    Parameters:
        
        game_id (int):
            The RetroAchievements ID of the desired game.

        df_games_data (pandas.DataFrame):
           A DataFrame containing RA's metadata of some games including the desired one.

    Returns:
        
        str:
            Title of the desired game.
    """

    return df_games_data[df_games_data["ID"] == game_id]["Title"].values[0]

def get_game_console(game_id: int, df_historic: pd.DataFrame) -> str:
    
    """
    Returns all the game IDs contained in a DataFrame containing the user's metadata.
    
    Parameters:
        
        game_id (int):
            The RetroAchievements ID of the desired game.

        df (pandas.DataFrame):
            A DataFrame containing the user's RA metadata.

    Returns:
        
        str:
            System of the desired game.
    """

    return df_historic[df_historic["GameID"] == game_id]["ConsoleName"].values[0]

def get_cheevo_data(game_id: int, cheevos_data_dict: dict) -> pd.DataFrame:
    
    """
    Retrieve the achievement list for a game with all the metadata.
    
    Parameters:
        
        game_id (int):
            The RetroAchievements ID of the desired game.
            
        cheevos_data_dict (dict):
            Dictionary with the involved games' ID as keys and a Pandas
            DataFrame containing the achievements' metadata as values
            
    Returns:

        pandas.DataFrame:
            Pandas DataFrame containing the game's achievement metadata.
    """

    return cheevos_data_dict[game_id]

def check_mastered(game_id: int, df_game: pd.DataFrame, cheevos_data_dict: dict) -> bool:
    
    """
    Check if a specific game was mastered.
    
    Parameters:
        
        game_id (int):
            The RetroAchievements ID of the desired game.
            
        df_game (pandas.DataFrame):
            DataFrame containing the user's RA metadata regarding the desired game.
            
        cheevos_data_dict (dict):
            Dictionary with the involved games' ID as keys and a Pandas
            DataFrame containing the achievements' metadata as values.
            
    Returns:
        
        bool:
            True if the game was mastered.
    """

    df_cheevos = get_cheevo_data(game_id, cheevos_data_dict)

    return len(df_game) == len(df_cheevos)

def check_beaten(game_id: int, df_game: pd.DataFrame, cheevos_data_dict: dict) -> bool:
    
    """
    Check if a specific game was beaten.
    
    Parameters:
        
        game_id (int):
            The RetroAchievements ID of the desired game.
            
        df_game (pandas.DataFrame):
            DataFrame containing the user's RA metadata regarding the desired game.
            
        cheevos_data_dict (dict):
            Dictionary with the involved games' ID as keys and a Pandas
            DataFrame containing the achievements' metadata as values.
            
    Returns:
        
        bool:
            True if the game was beaten.
    """

    df_cheevos = get_cheevo_data(game_id, cheevos_data_dict)

    # If one progression achievement is missing, return False
    
    for cheevo_id in df_cheevos[df_cheevos["type"] == "progression"]["ID"]:
        if cheevo_id not in df_game["AchievementID"].values:
            return False

    # If one win condition achievement is present, return True

    for cheevo_id in df_cheevos[df_cheevos["type"] == "win_condition"]["ID"]:
        if cheevo_id in df_game["AchievementID"].values:
            return True

    return False

def get_most_point_game(df_historic: pd.DataFrame) -> tuple:
    
    """
    Get the game with the most points and its point total from a historic.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history
            
    Returns:
        
        tuple:
            GameID and point total of the game with most points.
    """

    points_by_game_sorted = df_historic.groupby('GameID')['Points'].sum().sort_values(ascending=False)

    return points_by_game_sorted.index[0], points_by_game_sorted.values[0]

def get_most_retropoint_game(df_historic: pd.DataFrame) -> tuple:
    
    """
    Get the game with the most RetroPoints and its RetroPoint total from a
    historic.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history
            
    Returns:
        
        tuple:
            GameID and RetroPoint total of the game with most RetroPoints.
    """

    retropoints_by_game_sorted = df_historic.groupby('GameID')['TrueRatio'].sum().sort_values(ascending=False)

    return retropoints_by_game_sorted.index[0], retropoints_by_game_sorted.values[0]

def get_most_cheevo_game(df_historic: pd.DataFrame) -> tuple:
    
    """
    Get the game with the most achievements and its achievement total from a
    historic.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history
            
    Returns:
        
        tuple:
            GameID and achievement total of the game with most achievements.
    """

    game_counts = df_historic['GameID'].value_counts()

    return game_counts.index[0], game_counts.iloc[0]

def retrieve_image(url: str) -> Image:
    
    """
    Get an image from the web.
    
    Parameters:
        
        url (str):
            URL of the picture to download.
            
    Returns:
        
        Image:
            The requested image.
    """

    response = requests.get(url)
    
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return None
    
def retrieve_image_as_fig(url: str):
    
    """
    Get an image from the web as a plottable figure.
    
    Parameters:
        
        url (str):
            URL of the picture to download.
            
    Returns:
        
        matplotlib.figure.Figure:
            The requested image as a plottable figure.
    """

    img = retrieve_image(url)
    
    fig, ax = plt.subplots(figsize=(1, 1))
    ax.axis('off')
    
    ax.imshow(img)

    plt.close(fig)
    
    return fig

def get_game_icon(df_historic: pd.DataFrame, game_id: int):
    
    """
    Get the icon of a game registered in RetroAchievements.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history.
            
        game_id (int):
            The RetroAchievements ID of the desired game.
            
    Returns:
        
        Image:
            The requested image.
    """

    url = 'https://media.retroachievements.org' + df_historic[df_historic["GameID"] == game_id]["GameIcon"].values[0]

    return retrieve_image(url)

def get_game_icon_fig(df_historic: pd.DataFrame, game_id: int):
    
    """
    Get the icon of a game registered in RetroAchievements as a plottable
    figure.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history.
            
        game_id (int):
            The RetroAchievements ID of the desired game.
            
    Returns:
        
        matplotlib.figure.Figure:
            The requested image as a plottable figure.
    """

    url = 'https://media.retroachievements.org' + df_historic[df_historic["GameID"] == game_id]["GameIcon"].values[0]

    return retrieve_image_as_fig(url)

def get_cheevo_badge_fig(df: pd.DataFrame, cheevo_id: int):
    
    """
    Get the badge of a RetroAchievements achievement as a plottable figure.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history.
            
        cheevo_id (int):
            The RetroAchievements ID of the desired achievement.
            
    Returns:
        
        matplotlib.figure.Figure:
            The requested image as a plottable figure.
    """
    
    url = 'https://media.retroachievements.org' + df[df["AchievementID"] == cheevo_id]["BadgeURL"].values[0]

    return retrieve_image_as_fig(url)

def get_user_icon_fig(username: str):
    
    """
    Get the icon of a user registered in RetroAchievements as a plottable
    figure.
    
    Parameters:
        
        username (str):
            The user's RetroAchievements username
            
    Returns:
        
        matplotlib.figure.Figure:
            The requested image as a plottable figure.
    """

    url = 'https://media.retroachievements.org/UserPic/' + username + ".png"  
    
    return retrieve_image_as_fig(url)


# Complex functions

def retrieve_historic_df(username: str, api_key: str) -> pd.DataFrame:
    
    """
    Make some requests to the RetroAchievements API and return a DataFrame
    containing the user's achievement history.
    
    Parameters:
        
        username (str):
            The user's RetroAchievements username
            
        api_key (str):
            The user's RetroAchievements API key
        
    Returns:
        
        df_historic (pandas.DataFrame):
            The user's achievement history
    """
    
    # Set base URL
    
    func_url = "https://retroachievements.org/API/API_GetAchievementsEarnedBetween.php?"
    
    # Prepare arguments for the request
    
    start_date_epoch = calendar.timegm(datetime.datetime(1970, 1, 1, 0, 0, 0).timetuple())
    end_date_epoch   = calendar.timegm(datetime.datetime(2100, 1, 1, 0, 0, 0).timetuple())

    args = ["y=" + api_key,
            "u=" + username,
            "f=" + str(start_date_epoch),
            "t=" + str(end_date_epoch)]
    
    # Request the first batch of achievements (500/request max)

    url = func_url + "&".join(args)
    response = requests.get(url).json()
    
    # Store first batch of achievements in the historic

    historic = response
    
    # Keep repeating until there are no results left

    while len(response) == 500:
        
        # Update arguments to get next batch based on start date
        
        new_start_date = response[-1]["Date"].replace("-", " ").replace(":", " ").split()
        for i in range(6):
            new_start_date[i] = int(new_start_date[i])
        
        start_date_epoch = calendar.timegm(datetime.datetime(*new_start_date).timetuple()) + 1

        args[2] = "f=" + str(start_date_epoch)
        
        # Request the next batch achievements

        url = func_url + "&".join(args)
        response = requests.get(url).json()
        
        # Store in the historic
        
        historic += response
        
        # Avoid saturating the API
        
        time.sleep(0.2)
        
    # Convert historic data to DataFrame format
    
    df_historic = pd.DataFrame(historic)
    
    # Softcore achievements gained later on hardcore are not counted.
    # To avoid misrepresenting data, we entirely drop softcore achievements

    df_historic = df_historic[df_historic["HardcoreMode"] == 1].reset_index(drop=True)
    
    # Format the dates in a more manageable way
    
    splitdate = df_historic["Date"].apply(lambda x: np.array(x.replace("-", " ").replace(":", " ").split()))
    splitdate = splitdate.apply(lambda x: [int(item) for item in x])
    
    df_historic["Year"]   = splitdate.apply(lambda x: x[0])
    df_historic["Month"]  = splitdate.apply(lambda x: x[1])
    df_historic["Day"]    = splitdate.apply(lambda x: x[2])
    df_historic["Hour"]   = splitdate.apply(lambda x: x[3])
    df_historic["Minute"] = splitdate.apply(lambda x: x[4])
    
    df_historic["Date"] = splitdate.apply(lambda x: calendar.timegm(datetime.datetime(*x).timetuple()))
    
    # Drop unused achievements data to save memory
    
    df_historic = df_historic.drop(["HardcoreMode",
                                    "GameURL"], axis=1)

    return df_historic

def retrieve_necessary_games_data(df_historic: pd.DataFrame, api_key: str) -> pd.DataFrame:
    
    """
    Make some requests to the RetroAchievements API and return the metadata
    of the games that appear in some user's achievement history.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history.
            
        api_key (str):
            A valid RetroAchievements API key.
        
    Returns:
        
        pandas.DataFrame:
            The games' metadata.
            
        dict:
            Dictionary with the involved games' ID as keys and a Pandas
            DataFrame containing the achievements' metadata as values.
    """
    
    # Set base URL
    
    func_url = "https://retroachievements.org/API/API_GetGameExtended.php?"
    
    # Get the set of all the games to retrieve from historic_df
    
    game_ids = df_historic["GameID"].unique()

    # Prepare arguments for the request

    args = ["y=" + api_key,
            "i="]
    
    # Prepare variables to store retrieved data

    game_data_list = []
    cheevos_df_dict = {}

    # Iterate over all games

    for game_id in game_ids:
        
        # Update arguments to set current game as request target

        args[1] = "i=" + str(game_id)
        
        url = func_url + "&".join(args)
        
        # Request the next game's data
        
        game_data = requests.get(url).json()
        
        # Separate achievements data
        
        cheevos_df = pd.DataFrame(game_data.pop("Achievements")).transpose().reset_index(drop=True)
        
        # Drop unused achievements data to save memory
        
        cheevos_df.drop(["NumAwarded",
                         "NumAwardedHardcore",
                         "DateModified",
                         "DateCreated",
                         "BadgeName",
                         "DisplayOrder",
                         "MemAddr"], axis=1)
        
        # Store general data and achievements data for current game
        
        game_data_list.append(game_data)
        
        cheevos_df_dict[game_id] = cheevos_df

        # Avoid saturating the API
        
        time.sleep(0.2)
        
    # Convert game data to DataFrame and drop unused columns to save memory
    
    df_game_data = pd.DataFrame(game_data_list)
    
    df_game_data.drop(["ForumTopicID",
                       "Flags",
                       "ImageTitle",
                       "ImageIngame",
                       "ImageBoxArt",
                       "Publisher",
                       "Developer",
                       "Released",
                       "ReleasedAtGranularity",
                       "IsFinal",
                       "RichPresencePatch",
                       "GuideURL",
                       "Updated",
                       "ParentGameID",
                       "NumDistinctPlayers",
                       "NumAchievements",
                       "Claims",
                       "NumDistinctPlayersCasual",
                       "NumDistinctPlayersHardcore"], axis=1)
        
    return df_game_data, cheevos_df_dict

def get_event_data(df_historic, drop=False):
    
    """
    Separate historic into one DataFrame for games and another one for events.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history.
            
        drop (bool):
            If True, event data is removed from df_historic.
        
    Returns:
        
        pandas.DataFrame:
            Sub-DataFrame of df_historic with only event data.
    """
    
    df_events = df_historic[df_historic["ConsoleName"] == "Events"]
    
    if drop:
        df_historic.drop(df_historic[df_historic["ConsoleName"] == "Events"].index, inplace=True)
        
    return df_events

def get_yearly_stats(df_historic: pd.DataFrame,
                     year: int,
                     df_games_data: pd.DataFrame,
                     cheevos_data_dict: dict):
    
    """
    Extract the RetroAchievements stats for a certain year from some user's
    achievement history.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history.
            
        year (int):
            Year to check.
            
        df_games_data (pandas.DataFrame):
            RetroAchievements metadata of the games that appear in df_historic.
            
        cheevos_data_dict (dict):
            Dictionary with the involved games' ID as keys and a Pandas
            DataFrame containing the achievements' metadata as values.
        
    Returns:
        
        stats (dict):
            Dictionary with the user's stats for the selected year.
    """

    df_year  = df_historic[df_historic["Year"] == year].reset_index(drop=True)

    game_ids = get_game_ids(df_year)

    stats = {}

    # Get basic data

    stats["Game total"]         = len(game_ids)
    stats["Achievements total"] = len(df_year)
    stats["Points total"]       = df_year["Points"].sum()
    stats["RetroPoints total"]  = df_year["TrueRatio"].sum()

    # Get most fruitful games

    stats["Max cheevos"]      = get_most_cheevo_game(df_year)
    stats["Max pointer"]      = get_most_point_game(df_year)
    stats["Max RetroPointer"] = get_most_retropoint_game(df_year)

    # Get mastery/beaten data
    
    df_until = df_historic[df_historic["Year"] <= year]
    df_prev  = df_historic[df_historic["Year"] <  year]
    
    mastered_games = []
    beaten_games   = []
    
    game_icons = {}
    
    get_icon_flag = False
    
    for game_id in game_ids:
    
        df_game_until = df_until[df_until["GameID"] == game_id]
        df_game_prev  = df_prev[ df_prev[ "GameID"] == game_id]
    
        if (check_mastered(game_id, df_game_until, cheevos_data_dict) and not check_mastered(game_id, df_game_prev, cheevos_data_dict)):
    
            mastered_games.append(game_id)
            get_icon_flag = True
    
        if (check_beaten(game_id, df_game_until, cheevos_data_dict) and not check_beaten(game_id, df_game_prev, cheevos_data_dict)):
    
            beaten_games.append(game_id)
            get_icon_flag = True
                
        if get_icon_flag:
            game_icons[game_id] = get_game_icon_fig(df_historic, game_id)
            get_icon_flag = False

    stats["Mastered games"] = mastered_games
    stats["Beaten games"]   = beaten_games
    stats["Game icons"]     = game_icons
    
    # Get hardest achievements
    
    hardest_achievements = df_year.nlargest(10, "TrueRatio").reset_index(drop=True)
    
    stats["Hardest achievements"] = [hardest_achievements.iloc[i] for i in range(len(hardest_achievements))]
    
    stats["Hardest achievements badges"] = [get_cheevo_badge_fig(df_historic, stats["Hardest achievements"][i]["AchievementID"]) for i in range(len(hardest_achievements))]

    return stats

def get_yearly_favdev_stats(df_historic: pd.DataFrame,
                            year: int) -> dict:

    """
    Extract the developer related achievement data contained in a user's
    RetroAchievements history and structure it.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history.
            
        year (int):
            Year to check.
        
    Returns:
        
        stats (dict):
            Dictionary with the user's developer related stats for the selected
            year.
    """

    df_year = df_historic[df_historic["Year"] == year]
    dev_dist = get_dev_distribution(df_year, "Achievements").sort_values(ascending=False)

    username = dev_dist.index[0]

    stats = {}

    # Basic data

    stats["Username"] = username

    stats["User icon"] = get_user_icon_fig(username)

    # Totals
    
    stats["Achievement total"] = dev_dist.iloc[0]
    stats["Point total"] = np.sum(df_year[df_year["Author"] == username]["Points"])
    stats["RetroPoint total"] = np.sum(df_year[df_year["Author"] == username]["TrueRatio"])

    stats["Achievement %"] = 100*dev_dist.iloc[0]/len(df_year)

    # Distribution

    stats["Game distribution"] = df_year[df_year["Author"] == username].groupby("GameID")["AchievementID"].nunique()

    return stats

def get_figure_daily_points_one_year(df_historic: pd.DataFrame, year: int, title: bool=False) -> go.Figure:
    
    """
    Returns a bar chart of the daily point distribution throughout a year.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history.
            
        year (int):
            Year to check.
            
        title (bool):
            Whether the graph should have a title or not.
        
    Returns:
        
        go.Figure:
            Pie chart of the console presence in the historic.
    """
    
    # Retrieve the data

    df_year = df_historic[df_historic["Year"] == year]
    
    daily_points  = np.zeros(365 + (year%4 == 0), dtype=int)
    
    index = 0
    for month in range(1,13):
        df_month = df_year[df_year["Month"] == month]
        
        for day in range(1, calendar.monthrange(year, month)[1]+1):
            df_day = df_month[df_month["Day"] == day]
            daily_points[index]  = df_day["Points"].sum()
            index += 1

    # Create customized tooltips

    dates = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31')
    hover_text = [f"<b>{date.day} {calendar.month_name[date.month].title()[:3]}: {value} Points</b>" for date, value in zip(dates, daily_points)]
    
    # Create the bar plot
    
    fig = go.Figure(data=[go.Bar(
        x=dates,
        y=daily_points,
        text=hover_text,
        hoverinfo='text',
        marker=dict(
            color='#bd9109',
            line=dict(
                color='#bd9109',
                width=1
            )
        ),
        hoverlabel=dict(
            bgcolor='white',
            bordercolor='black',
            font=dict(
                color='black',
                family='Arial',
                size=14
            )
        )
    )])
    
    # Create customized ticks and labels
    
    xticks = [pd.Timestamp(f'{year}-{month:02d}-01') for month in range(1, 13)]
    xtick_labels = [calendar.month_name[month][0].upper() for month in range(1, 13)]
    
    y_step = np.round(np.max(daily_points)//5,-len(str(np.max(daily_points)//5))+1)
    
    # If the maximum is less than 5 it breaks, this is the fix
    
    if y_step == 0:
        y_step = np.max(daily_points)
    
    yticks = list(range(0, (np.max(daily_points)//y_step+1)*y_step, y_step))

    # Customize the plot
    
    fig.update_layout(
        xaxis=dict(
            tickvals=xticks,
            ticktext=xtick_labels,
            tickangle=0
        ),
        yaxis=dict(
            tickvals=yticks,
            tickangle=0
        ),
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='#212121',
        margin=dict(t=50 if title else 10, b=40, l=50, r=10)
    )
    
    if title:
        
        fig.update_layout(
            title=f"<b>Points earned in {year} by date</b>",
            titlefont=dict(
                    color='#1d56d3',
                    size=20, 
                    family='Arial'
                )
        )
    
    fig.update_xaxes(
        mirror=True,
        ticks='',
        showline=True,
        gridcolor='#858585',
        tickfont=dict(
                color='#1d56d3',
                size=14,
                family='Arial'
            )
    )
    
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        gridcolor='#858585',
        tickfont=dict(
                color='#1d56d3',
                size=14, 
                family='Arial'
            )
    )

    return fig

def get_yearly_game_stats(df_historic: pd.DataFrame,
                          year: int,
                          game_id: int,
                          df_games_data: pd.DataFrame,
                          cheevos_data_dict: dict) -> dict:

    """
    Extract the RetroAchievements stats for a certain game and year from some
    user's achievement history.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history.
            
        year (int):
            Year to check.
            
        game_id (int):
            The RetroAchievements ID of the desired game.
            
        df_games_data (pandas.DataFrame):
            RetroAchievements metadata of the games that appear in df_historic.
            
        cheevos_data_dict (dict):
            Dictionary with the involved games' ID as keys and a Pandas
            DataFrame containing the achievements' metadata as values.
        
    Returns:
        
        stats (dict):
            Dictionary with the user's stats for the selected year.
    """

    df_game = df_historic[(df_historic["GameID"] == game_id) & (df_historic["Year"] <= year)].reset_index(drop=True)
    df_game_year = df_game[df_game["Year"] == year].reset_index(drop=True)
    df_cheevos = get_cheevo_data(game_id, cheevos_data_dict)

    stats = {}

    # Basic data

    stats["Title"] = get_game_title(game_id, df_games_data)
    
    stats["Achievement count"] = len(df_game)
    stats["Achievement total"] = len(df_cheevos)
    stats["Achievement count this year"] = len(df_game_year)

    stats["Point count"] = np.sum(df_game["Points"])
    stats["Point total"] = np.sum(df_cheevos["Points"])
    stats["Point count this year"] = np.sum(df_game_year["Points"])

    # Beaten/mastered

    stats["Beaten"] = check_beaten(game_id, df_game, cheevos_data_dict)
    stats["Beaten this year"] = not check_beaten(game_id, df_game[df_game["Year"] < year], cheevos_data_dict)

    stats["Mastered"] = check_mastered(game_id, df_game, cheevos_data_dict)
    stats["Mastered this year"] = not check_mastered(game_id, df_game[df_game["Year"] < year], cheevos_data_dict)

    # Notorious achievements

    stats["Hardest achievement"] = df_game_year.iloc[np.argmax(df_game_year["TrueRatio"])]
    stats["Latest achievement"] = df_game_year.iloc[len(df_game_year)-1]

    # Badges

    stats["Game badge"] = get_game_icon_fig(df_historic, game_id)
    
    stats["Hardest achievement badge"] = get_cheevo_badge_fig(df_historic, stats["Hardest achievement"]["AchievementID"])
    stats["Latest achievement badge"] =  get_cheevo_badge_fig(df_historic, stats["Latest achievement"]["AchievementID"])

    return stats

def get_system_distribution(df_historic: pd.DataFrame, by: str) -> pd.Series:
    
    """
    Returns a histogram of the consoles by selected count method.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history
            
        by (str):
            Categorization method (options: 'Games', 'Achievements', 'Points', 'RetroPoints').
        
    Returns:
        
        pandas.Series:
            Pandas Series containing console names as indices and selected count as values.
    """
    
    if by == "Games":
        return df_historic.groupby('ConsoleName')['GameID'].nunique()
    
    elif by == "Achievements":
        return df_historic.groupby('ConsoleName')['AchievementID'].nunique()
    
    elif by == "Points":
        return df_historic.groupby('ConsoleName')['Points'].sum()
    
    elif by == "RetroPoints":
        return df_historic.groupby('ConsoleName')['TrueRatio'].sum()
    
    else:
        raise ValueError(f"'by' argument should be one of 'Games', 'Points' or 'RetroPoints', but was '{by}'.")

def get_figure_system_distribution(df_historic: pd.DataFrame, year: str, by: str, max_shown: int= 8, title: bool= False) -> go.Figure:
    
    """
    Returns a pie chart of the console presence in the historic.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history.
            
        year (int):
            Year to check.
            
        by (str):
            Categorization method (options: 'Games', 'Achievements', 'Points', 'RetroPoints').
            
        max_shown (int):
            Maximum number of entries shown, plus one for 'Others'
            
        title (bool):
            Whether the graph should have a title or not.
        
    Returns:
        
        go.Figure:
            Pie chart of the console presence in the historic.
    """

    df_year = df_historic[df_historic["Year"] == year]
    
    system_dist = get_system_distribution(df_year, by)
    
    if len(system_dist) > max_shown:

        system_dist = system_dist.sort_values(ascending=False)

        total = system_dist.values.sum()
        system_dist = system_dist.iloc[range(max_shown)]
        system_dist["Others"] = total - system_dist.values.sum()
    
    fig = go.Figure(
        data=[
            go.Pie(
                labels=system_dist.index,
                values=system_dist.values,
                textinfo='label+value',
                textposition='outside',
                pull=[0.1, 0.1, 0.1],
                showlegend=False
            )
        ]
    )
    
    fig.update_layout(template='plotly',
                      margin=dict(t=50 if title else 10, b=40, l=50, r=10))
    
    if title:
        fig.update_layout(title=f"{by} per console in {year}")

    return fig

def get_dev_distribution(df_historic: pd.DataFrame, by: str) -> pd.Series:
    
    """
    Returns a histogram of the developers by selected count method.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history
            
        by (str):
            Categorization method (options: 'Achievements', 'Points', 'RetroPoints').
        
    Returns:
        
        pandas.Series:
            Pandas Series containing developer usernames as indices and selected count as values.
    """
    
    if by == "Achievements":
        return df_historic.groupby('Author')['AchievementID'].nunique()
    
    elif by == "Points":
        return df_historic.groupby('Author')['Points'].sum()
    
    elif by == "RetroPoints":
        return df_historic.groupby('Author')['TrueRatio'].sum()
    
    else:
        raise ValueError(f"'by' argument should be one of 'Achievements' 'Points' or 'RetroPoints', but was '{by}'.")
        
def get_figure_dev_distribution(df_historic: pd.DataFrame, year: str, by: str, max_shown: int= 8, title: bool= False) -> go.Figure:
    
    """
    Returns a pie chart of the developer presence in the historic.
    
    Parameters:
        
        df_historic (pandas.DataFrame):
            Some user's RetroAchievements achievement history.
            
        year (int):
            Year to check.
            
        by (str):
            Categorization method (options: 'Games', 'Achievements', 'Points', 'RetroPoints').
            
        max_shown (int):
            Maximum number of entries shown, plus one for 'Others'
            
        title (bool):
            Whether the graph should have a title or not.
        
    Returns:
        
        go.Figure:
            Pie chart of the developer presence in the historic.
    """

    df_year = df_historic[df_historic["Year"] == year]
    
    dev_dist = get_dev_distribution(df_year, by)

    if len(dev_dist) > max_shown:

        dev_dist = dev_dist.sort_values(ascending=False)

        total = dev_dist.values.sum()
        dev_dist = dev_dist.iloc[range(max_shown)]
        dev_dist["Others"] = total - dev_dist.values.sum()
    
    fig = go.Figure(
        data=[
            go.Pie(
                labels=dev_dist.index,
                values=dev_dist.values,
                textinfo='label+value',
                textposition='outside',
                pull=[0.1, 0.1, 0.1],
                showlegend=False
            )
        ]
    )
    
    fig.update_layout(template='plotly',
                      margin=dict(t=50 if title else 10, b=40, l=50, r=10))
    
    if title:
        fig.update_layout(title=f"{by} per developer in {year}")
    return fig

if __name__ == "__main__":
    
    username = input("Username: ")
    api_key = input("Your API key: ")
    
    df_historic = retrieve_historic_df(username=username,
                                       api_key=api_key)
    
    df_games_data, cheevos_data_dict = retrieve_necessary_games_data(df_historic=df_historic,
                                                                     api_key=api_key)
    
    year = 2023
    
    # Yearly stats
    
    stats = get_yearly_stats(df_historic=df_historic,
                             year=year,
                             df_games_data=df_games_data,
                             cheevos_data_dict=cheevos_data_dict)

    print(year, "stats")
    print("-----------------------------------------\n")
    
    print("You played", stats["Game total"], "games.\n")
    print("You got", stats["Achievements total"], "achievements.")
    print("The game you got the most achievements for is " + get_game_title(stats["Max cheevos"][0], df_games_data) + ", with " + str(stats["Max cheevos"][1]) + " achievements.\n")

    print("You got", stats["Points total"], "points.")
    print("The game that gave you the most points is " + get_game_title(stats["Max pointer"][0], df_games_data) + ", with " + str(stats["Max pointer"][1]) + " points.\n")
    
    print("You got", stats["RetroPoints total"], "RetroPoints.")
    print("The game that gave you the most RetroPoints is " + get_game_title(stats["Max RetroPointer"][0], df_games_data) + ", with " + str(stats["Max RetroPointer"][1]) + " points.\n")
        
    print("You beat", len(stats["Beaten games"]), "games:")
    for game_id in stats["Beaten games"]:
        print("\t" + get_game_title(game_id, df_games_data) + ", " + get_game_console(game_id, df_historic))
    print()
    
    print("You mastered", len(stats["Mastered games"]), "games:")
    for game_id in stats["Mastered games"]:
        print("\t" + get_game_title(game_id, df_games_data) + ", " + get_game_console(game_id, df_historic))
        
    # Daily points figure
        
    fig = get_figure_daily_points_one_year(df_historic=df_historic, year=year)
    fig.show(renderer="browser")