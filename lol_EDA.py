import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

final_df = pd.read_csv('c:/data/final_df.csv') 

#data shape
print("Data Size : {}".format(final_df.shape))
final_df.columns
final_df.head(5)


#승패 통계치
final_df[final_df['win']==1].describe()[['towerKills','inhibitorKills','baronKills','dragonKills','riftHeraldKills']]
final_df[final_df['win']==0].describe()[['towerKills','inhibitorKills','baronKills','dragonKills','riftHeraldKills']]

feature=['win','firstBlood','firstTower','firstInhibitor','firstBaron','firstDragon']
final_df.columns
win_pct = []
lose_pct = [1,1,1,1,1,1]

for i in feature:
    win_pct.append(final_df[final_df[i]==1].count()['win']/final_df.count()['win'])
    
plt.figure(figsize=(15,10))

plt.bar(feature,lose_pct, color='pink', edgecolor='black', width=0.5)
plt.bar(feature,win_pct, color='skyblue', edgecolor='black', width=0.5)

#average game time

print("Average game time : {:.2f} minutes".format(final_df['gameDuration'].mean()/60))
sns.distplot(final_df['gameDuration']/60, hist=True)
plt.xlabel('game time (min)',size=20)
plt.ylabel('Number of Games',size=20)

#win corr

final_df['win']
final_df['win'] = pd.get_dummies(final_df['win'],drop_first = True)

final_df.columns
feature = ['win','towerKills','inhibitorKills','baronKills','dragonKills','gameDuration']
plt.figure(figsize=(12,12))
sns.set(font_scale = 1)
sns.heatmap(final_df[feature].corr(), annot=True)

plt.figure(figsize=(2,7))
sns.heatmap(final_df[feature].corr().to_frame(), annot=True, cbar=False)

