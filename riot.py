from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv
import pandas as pd
import yaml
import os

load_dotenv()

# global variables
api_key = os.getenv('RIOT_API_KEY')

watcher = LolWatcher(api_key)


with open('summoners.yaml') as f:
    roster = yaml.load(f, Loader=yaml.FullLoader)


# get player ID from discord name 
def get_summoner_aliases(discord_id):
	'''
	return all known aliases for discord user
	'''
	if roster.get(discord_id):
		return roster.get(discord_id).get('aliases')

	else:
		print('User not in summoner roster')
		return 


def get_puuid(summoner_name):
	'''
	get puuid from summoner name, return puuid of most recent account

	'''
	puuid = watcher.summoner.by_name(region='na1', summoner_name=summoner_name).get('puuid') 

	return puuid


# get last match from player ID
def get_last_match_df(puuid):
	'''
	get last match summary from puuid
	'''
	my_matches = watcher.match.matchlist_by_puuid(region='americas', puuid=puuid)
	last_match = my_matches[0]
	match_detail = watcher.match.by_id(region='americas', match_id=my_matches[0])
	game_end_timestamp = match_detail.get('info').get('gameEndTimestamp')
	match_participants = match_detail.get('info').get('participants')

	participants = []
	for row in match_participants:
		if puuid == row['puuid']:
			participants_row = {}
			participants_row['champion'] = row['championName']
			participants_row['kills'] = row['kills']
			participants_row['deaths'] = row['deaths']
			participants_row['summonerName'] = row['summonerName']
			participants_row['win'] = row['win']
			participants_row['gameEndTimestamp'] = game_end_timestamp
			participants_row['puuid'] = row['puuid']
			participants_row['puuid_self'] = row['puuid']
			participants_row['wards_placed'] = row['wardsPlaced']
			participants_row['position'] = row['individualPosition']
			participants_row['assists'] = row['assists']
	
			participants.append(participants_row)

	df = pd.DataFrame(participants)

	return df


def get_last_game_summary(discord_id):

	aliases = get_summoner_aliases(discord_id)

	if aliases: 

		dfs = [] 

		for alias in aliases:
			puuid = get_puuid(alias)
			dfs.append(get_last_match_df(puuid))

		df = pd.concat(dfs)

		most_recent_game = df['gameEndTimestamp'].max()
		df = df[df['gameEndTimestamp'] == most_recent_game]

		out = {
			'kills': df['kills'].values[0],
			'deaths': df['deaths'].values[0],
			'assists': df['assists'].values[0],
			'champion': df['champion'].values[0],
			'win': df['win'].values[0],
			'wards': df['wards_placed'].values[0] 

		}

		return out

	else: 
		return None


def get_most_recent_game_puuid(discord_id):

	aliases = get_summoner_aliases(discord_id)

	if aliases: 

		dfs = [] 

		for alias in aliases:
			puuid = get_puuid(alias)
			dfs.append(get_last_match_df(puuid))

		df = pd.concat(dfs)

		most_recent_game = df['gameEndTimestamp'].max()
		df = df[df['gameEndTimestamp'] == most_recent_game]	
		puuid = df.iloc[0]['puuid']

		return puuid

	else:
		return None


# get last match from player ID
def get_matches(puuid, n=1):
	'''
	get last match summary from puuid
	'''

	my_matches = watcher.match.matchlist_by_puuid(region='americas', puuid=puuid)
	last_n_match_ids = my_matches[0:n]

	return last_n_match_ids


def last_n_match_details_df(puuid, n):

	match_results = []

	last_n_match_ids = get_matches(puuid, n)

	for match_id in last_n_match_ids:
		match_detail = watcher.match.by_id(region='americas', match_id=match_id)
		game_end_timestamp = match_detail.get('info').get('gameEndTimestamp')
		match_participants = match_detail.get('info').get('participants')
		match_results.append(pd.DataFrame(match_participants))

	return pd.concat(match_results)
	

def tablefy(data, cols):

	d = pd.DataFrame(data)
	d_limited = d[cols]

	return d_limited.to_markdown(tablefmt='grid', showindex=False)





