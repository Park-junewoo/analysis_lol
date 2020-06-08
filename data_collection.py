import requests
import pandas as pd
import time
import matplotlib.pyplot as plt

api_key = 'RGAPI-3ba9a230-ac05-4d08-a06a-8365c217320d'


challenger = 'https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=' + api_key
g_master = 'https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key='+ api_key
master = 'https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key='+ api_key

c_r = requests.get(challenger)
gm_r = requests.get(g_master)
m_r = requests.get(master)

c_df = pd.DataFrame(c_r.json())
gm_df = pd.DataFrame(gm_r.json())
m_df = pd.DataFrame(m_r.json())
league_df.columns
league_df= pd.concat([c_df,gm_df,m_df])

league_df.reset_index(inplace=True,drop=True)
league_entries_df = pd.DataFrame(dict(league_df['entries'])).T #dict구조로 되어 있는 entries컬럼 풀어주기
league_df = pd.concat([league_df, league_entries_df], axis=1) #열끼리 결합
league_df.columns
league_df = league_df.drop(['queue', 'name', 'leagueId', 'entries', 'rank'], axis=1)
#league_df.to_csv('c:/data/챌린저데이터.csv',index=False,encoding = 'cp949')#중간저장

league_df.info()


league_df['summonerId']


account_id = []
for i in range(len(league_df)):
    try:
        sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
        r = requests.get(sohwan)
        time.sleep(2)
        while r.status_code == 429:
            sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
            r = requests.get(sohwan)
            print(i)
            
        account_id.append(r.json()['accountId'])
        print(i)
    except:
        pass
    
account_df=pd.DataFrame(account_id)

#account_df.to_csv('c:/data/challenger_account_id.csv',index=False,encoding = 'cp949')#중간저장
account_df=pd.read_csv('c:/data/challenger_account_id.csv')
account_id = account_df['0'].tolist()



match_info_df = pd.DataFrame()
for i in range(len(account_id)):
    try:
        match0 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account_id[i]  +'?api_key=' + api_key
        r = requests.get(match0)
        r.json()
        time.sleep(1.7)
        while r.status_code == 429:
            time.sleep(5)
            match0 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account_id[i] + '&api_key=' + api_key
            r = requests.get(match0)
            print('wait')
        match_info_df = pd.concat([match_info_df, pd.DataFrame(r.json()['matches'])])
        print(i)
    
    except:
        print("error")
        
len(match_info_df['gameId'].unique())
game_id = match_info_df.drop_duplicates(['gameId'])
match_info_df.columns
#game_id.to_csv('c:/data/challenger_game_id.csv',index=False,encoding = 'cp949')#중간저장

game_id = pd.read_csv('c:/data/challenger_game_id.csv') #중복 제거한 게임id


#game_id로 match 정보 가져오기

match_fin = pd.DataFrame()
a=0
for i in game_id['gameId']:
    match = "https://kr.api.riotgames.com/lol/match/v4/matches/{}?api_key=".format(i) + api_key
    r1 = requests.get(match)
    data = r1.json()
    mat = pd.DataFrame(list(r1.json().values()), index=list(r1.json().keys())).T
    match_fin = pd.concat([match_fin,mat])
    time.sleep(2)
    a+=1
    print(a)
    
#match_fin.to_csv('c:/data/challenger_match_fin.csv',index=False,encoding = 'cp949')#약 13000건 중간저장
match_fin = pd.read_csv('c:/data/challenger_match_fin.csv',encoding = 'cp949')# match 정보

match_fin.columns
match_fin.iloc[:1,:8]
list(match_fin['teams'])
match_fin['gameDuration']



#잘못 들어간 데이터 삭제

a=0
idx_lst=[]
import re
for i in match_fin['gameCreation']:
    if re.findall('nan',str(i)):
        print(i,a)
        idx_lst.append(a)
    a+=1

for i in idx_lst:
    match_fin.drop(i,0,inplace=True)

for i in idx_lst:
    print(match_fin.iloc[i:i+1])

match_fin.reset_index(drop=True,inplace=True)

#리스트로된 컬럼 풀어주기
import ast
df = pd.DataFrame(match_fin['teams'])
team_df1 = pd.DataFrame()
a=0
for i in df['teams']:
    b=ast.literal_eval(i)
    b[0].pop('bans')
    print(b[0])
    team_1=pd.DataFrame(b[0].values(),b[0].keys()).T
    team_df1=pd.concat([team_df1,team_1])


team_df1.reset_index(drop=True,inplace=True)

final_df = pd.concat([team_df1,match_fin['gameDuration']],axis=1)
final_df.columns
#final_df.to_csv('c:/data/final_df.csv',index=False,encoding = 'cp949')#최종 macth data 저장
final_df = pd.read_csv('c:/data/final_df.csv') #게임정보
final_df.columns