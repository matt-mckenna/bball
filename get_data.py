# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 21:29:33 2015

@author: matt
"""

import requests
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import display
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show



#example
#http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID=201939&SeasonType=Regular+Season

#url = http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID=201939&SeasonType=Regular+Season
#url2 = http://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=PerGame&PlayerID=201939

def get_player_id(player):
    """
    Loads a pandas DataFrame, numpy array, or int with the desired player ID(s)
    from an online repository.

    The player IDs are used to identify players in the NBA stats api.

    Parameters
    ----------
    player : str
        The desired player's name in 'Last Name, First Name' format. Passing in
        a single name returns a numpy array containing all the player IDs
        associated with that name.

        Passing "SHOTS" returns a DataFrame with all the players and their IDs
        that have shot chart data.

        Passing in "ALL" returns a DataFrame with all the available player IDs
        used by the NBA stats API, along with additional information.
        The column information for this DataFrame is as follows:
            PERSON_ID: The player ID for that player
            DISPLAY_LAST_COMMA_FIRST: The player's name.
            ROSTERSTATUS: 0 means player is not on a roster, 1 means he's on a
                          roster
            FROM_YEAR: The first year the player played.
            TO_YEAR: The last year the player played.
            PLAYERCODE: A code representing the player. Unsure of its use.
    """
    if player == "SHOTS":
        return pd.read_csv("http://raw.githubusercontent.com/savvastj/nbaShotChartsData/master/players2001.csv")
    elif player == "ALL":
        return pd.read_csv("http://raw.githubusercontent.com/savvastj/nbaShotChartsData/master/player_id.csv")
    else:
        df = pd.read_csv("http://raw.githubusercontent.com/savvastj/nbaShotChartsData/master/player_id.csv")
        player_id = df[df.DISPLAY_LAST_COMMA_FIRST == player].PERSON_ID
        if len(player_id) == 1:
            return player_id.values[0]
        if len(player_id) == 0:
            raise NoPlayerError('There is no player with that name.')
        return player_id.values


#url2 = http://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=PerGame&PlayerID=201939
class carStats:
    """
    Wrapper for career stats for a single player
    """
    def __init__(self, player_id, PerMode="PerGame",league_id="00"):
                     
        self.player_id = player_id

        self.base_url = "http://stats.nba.com/stats/playercareerstats?"


        self.url_paramaters = { "LeagueID": league_id,
                                "PerMode": PerMode,
                                "PlayerID": player_id,      
                              }                      
        self.response = requests.get(self.base_url, params=self.url_paramaters)
        
    def get_dat(self):
        """Returns the shot chart data as a pandas DataFrame."""
        sta = self.response.json()['resultSets'][0]['rowSet']
        headers = self.response.json()['resultSets'][0]['headers']
        return pd.DataFrame(sta, columns=headers)

class ComPlyrInf:
    """
    Wrapper for the common player info
    """
    def __init__(self, player_id,league_id="00", season="2014-15",
                 season_type="Regular Season", team_id=0, game_id="",
                 outcome="", location="", month=0, season_segment="",
                 date_from="", date_to="", opp_team_id=0, vs_conference="",
                 vs_division="", position="", rookie_year="", game_segment="",
                 period=0, last_n_games=0, clutch_time
                 ="", ahead_behind="",
                 point_diff="", range_type="", start_period="", end_period="",
                 start_range="", end_range="", context_filter="",
                 context_measure="FGA"):
                     
        self.player_id = player_id

        self.base_url = "http://stats.nba.com/stats/commonplayerinfo?"

        # TODO: Figure out what all these parameters mean for NBA stats api
        #       Need to figure out and include CFID and CFPARAMS, they are
        #       associated w/ContextFilter somehow
        self.url_paramaters = { "LeagueID": league_id,
                                "SeasonType": season_type,
                                "PlayerID": player_id,      
                              }
                              
        self.response = requests.get(self.base_url, params=self.url_paramaters)
        
    def get_dat(self):
        """Returns the shot chart data as a pandas DataFrame."""
        sta = self.response.json()['resultSets'][0]['rowSet']
        headers = self.response.json()['resultSets'][0]['headers']
        return pd.DataFrame(sta, columns=headers)

#url http://stats.nba.com/stats/playergamelog?LeagueID=00&PlayerID=201939&Season=2015-16&SeasonType=Regular+Season
class gamelog:

    def __init__(self, player_id, league_id="00", season="2015-16", season_type="Regular Season"):
                     
        self.player_id = player_id

        self.base_url = "http://stats.nba.com/stats/playergamelog?"


        self.url_paramaters = { "LeagueID": league_id,
                                "PlayerID": player_id, 
                                "Season": season,
                                "SeasonType" : season_type
                              }                      
        self.response = requests.get(self.base_url, params=self.url_paramaters)
        
    def get_dat(self):
        """Returns the shot chart data as a pandas DataFrame."""
        sta = self.response.json()['resultSets'][0]['rowSet']
        headers = self.response.json()['resultSets'][0]['headers']
        return pd.DataFrame(sta, columns=headers)

#usl is http://stats.nba.com/stats/teaminfocommon?LeagueID=00&SeasonType=Regular+Season&TeamID=1610612738&season=2015-16
class teaminfo:
    
    def __init__(self,team_id,league_id="00", season_type="Regular Season",  season="2015-16"):
        
        self.team_id = team_id
        
        self.base_url = "http://stats.nba.com/stats/teaminfocommon?"
        
        self.url_parameters= { "LeagueID": league_id,
                               "SeasonType": season_type,
                               "Season" : season,
                               "SeasonType" : season_type,
                               "TeamID" : team_id
                             }
                               
        self.response = requests.get(self.base_url, params=self.url_parameters)
        
    def get_dat(self):
        """Returns the shot chart data as a pandas DataFrame."""
        sta = self.response.json()['resultSets'][0]['rowSet']
        headers = self.response.json()['resultSets'][0]['headers']
        return pd.DataFrame(sta, columns=headers)
                   
#http://stats.nba.com/stats/teamgamelog?LeagueID=00&Season=2015-16&SeasonType=Regular+Season&TeamID=1610612738                   
class teamGameLog: 
    def __init__(self, team_id, league_id="00",season="2015-16", season_type="Regular Season"):
        
        self.team_id = team_id
        
        self.base_url = "http://stats.nba.com/stats/teamgamelog?"
        
        self.url_parameters = { "TeamID" : team_id,
                                "SeasonType" : season_type,
                                "Season" : season,
                                "LeagueID" : league_id}
                                
        self.response = requests.get(self.base_url, params=self.url_parameters)
        
    def get_dat(self):
        """Returns the shot chart data as a pandas DataFrame."""
        sta = self.response.json()['resultSets'][0]['rowSet']
        headers = self.response.json()['resultSets'][0]['headers']
        return pd.DataFrame(sta, columns=headers)
        
"""  examples     
#celtics
tid = 1610612738
id1 = get_player_id ("Bryant, Kobe")

gl = gamelog(id1, season="2014-15").get_dat()
#gets = ComPlyrInf(id1).get_dat()
getsc = carStats(id1).get_dat()
#tgl = teamGameLog(tid, season="2014-15").get_dat()

#tinf = teaminfo(tid, season="2014-15").get_dat()

print(list(getsc.columns.values))
print(getsc)
#print(tgl.groupby('WL').count())

#print(list(gl.columns.values))
#print(gl[['MATCHUP','PTS','REB','AST']])
#print(gl.mean())
#print(getsc[[]])
#print(getsc[['PTS','SEASON_ID']])

#print(type(gets))
#print(list(gets.columns.values))
#print(getsc)
"""
