#컬럼 타입확인
final_df.dtypes

#결측치 확인
final_df.isnull().sum()

#불필요한 컬럼 삭제
final_df.columns
final_df.drop(['teamId'],axis=1,inplace=True)

#모든 컬럼의 내용이 0 이므로 삭제
final_df[final_df['vilemawKills']==0]
final_df.drop(['vilemawKills'],axis=1,inplace=True)

final_df[final_df['dominionVictoryScore']==0] 
final_df.drop(['dominionVictoryScore'],axis=1,inplace=True)

#이상치 idx 추출
outlier = []
import numpy as np
final_df.columns
for i in range(6):
    plt.rcParams['figure.figsize'] = [13, 10]
    plt.subplot(2,3,i+1)
    data = final_df[final_df.iloc[:,7:].columns[i]]
    plt.boxplot(data)
    plt.title("{}".format(final_df.iloc[:,7:].columns[i]))
    q1 = np.percentile(data,25)
    q3 = np.percentile(data,75)
    iqr = q3-q1
    lf = q1 - 1.5 * iqr
    uf = q3 + 1.5 * iqr
    data[data<uf].max()
    data[data>lf].min()
    for i in data[data>uf].index:
        outlier.append(i)
    # upperfense 이상치
    for i in data[data<lf].index:
        outlier.append(i)
    # lowerfense 이상치

len(outlier)
outlier = set(outlier)            
outlier = list(outlier)
len(outlier)
#제거
for i in outlier:
    final_df.drop(i,0,inplace=True)

final_df.reset_index(drop=True,inplace=True)

#이상치 확인

for i in range(6):
    plt.rcParams['figure.figsize'] = [13, 10]
    plt.subplot(2,3,i+1)
    data = final_df[final_df.iloc[:,7:].columns[i]]
    plt.boxplot(data)
    plt.title("{}".format(final_df.iloc[:,7:].columns[i])) 

                    
#object 타입 dummies로 수치화 해주기
final_df.columns
final_df.dtypes
final_obj_df = final_df.select_dtypes(exclude=['float64','int64'])


for i in final_obj_df.columns:
    final_obj_df[i]=final_obj_df[i].astype('object')
    
final_obj_df.dtypes  
   
final_obj_df = pd.get_dummies(final_obj_df,drop_first = True)

final_df.select_dtypes(include=['float64','int64'])
import numpy as np
final_df_last = pd.concat([final_obj_df,final_df.select_dtypes(include=['float64','int64'])],axis=1)
final_df_last.columns





#-----------------------------------------------------------------------------------#

#ban 추출

import ast
df = pd.DataFrame(match_fin['teams'])
team_df1 = pd.DataFrame()

a=0
idx_lst=[]
import re
for i in df['teams']:
    if re.findall('nan',str(i)):
        print(i,a)
        idx_lst.append(a)
    a+=1
for i in idx_lst:
    df.drop(i,0,inplace=True)

a=0
for i in df['teams']:
    b=ast.literal_eval(i)
    #b[0].pop('bans')
    print(b[0])
    team_1=pd.DataFrame(b[0].values(),b[0].keys()).T
    team_df1=pd.concat([team_df1,team_1])



    
df = team_df1['bans']
df.reset_index(drop=True,inplace=True)
bans_df = pd.DataFrame()
for i in df:
    print(i)
    ban = pd.DataFrame(i)
    bans_df=pd.concat([bans_df,ban])
    
ban_count = bans_df['pickTurn'].groupby(bans_df['championId']).count()

#캐릭터 정보
import requests
import pandas as pd
a  = 'http://ddragon.leagueoflegends.com/cdn/10.8.1/data/ko_KR/champion.json'
r = requests.get(a)
df = pd.DataFrame(r.json()['data'])
df = df.T
champ_key = pd.DataFrame(df['key']).reset_index()
champ_key['key']=champ_key['key'].astype('int64')
ban_count_fin = pd.DataFrame(ban_count).reset_index()

final_ban_df = pd.merge(champ_key,ban_count_fin,left_on='key',right_on='championId',how='left')
final_ban_df = final_ban_df.sort_values(by='pickTurn',ascending=False)
final_ban_df.head(10)
final_ban_df.tail(10)