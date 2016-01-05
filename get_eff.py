
import sys
import csv
import numpy as np

execfile('get_data.py')



def wcsv (f, obj):
	with open(f, 'wb') as fp:
		a = csv.writer(fp, delimiter=',')
		a.writerows(obj)


def get_eff(name):

    id = get_player_id(name)
    gl = gamelog(id, season="ALL").get_dat()
    gl['MS'] = gl['FGA'] - gl['FGM']
    gl['eff'] = gl['PTS']+gl['REB']+gl['AST']+gl['STL']+gl['BLK']-gl['TOV']-gl['MS']
    gl['inx'] = gl.index
    gl = gl.loc[gl['eff'].notnull()]
    
    return(gl.sort_values(by='inx', ascending=False))

#[['inx', 'eff']])


kobe_eff=get_eff("Bryant, Kobe")
mj_eff = get_eff ("Jordan, Michael")
pip_eff = get_eff("Pippen, Scottie")
mal = get_eff('Malone, Karl')
stock = get_eff('Stockton, John')

kobe_eff.to_csv('../data/kobe.csv')
mj_eff.to_csv('../data/mj.csv')
pip_eff.to_csv('../data/pip.csv')
mal.to_csv('../data/mal.csv')
stock.to_csv('../data/stock.csv')



