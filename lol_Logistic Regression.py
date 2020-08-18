import pandas as pd
import numpy as np
final_df = pd.read_csv('c:/data/loldata/final_df.csv',encoding = 'cp949')# match 정보

tf_mapping = {True:1,False:0}
bool_column = final_df.select_dtypes('bool').columns.tolist()

for i in bool_column:
    final_df[i] = final_df[i].map(tf_mapping)
    
wl_mapping = {'Win':'Win','Fail':'Lose'}
final_df['win'] = final_df['win'].map(wl_mapping)

final_df['game_time'] = final_df['gameDuration']/60

final_df['win_encoding'] = final_df['win'].map({'Win':1,'Lose':0})



reg_df = final_df.drop(columns=['teamId','vilemawKills','dominionVictoryScore','win','game_time'])
reg_df = reg_df.dropna()

reg_df['win_encoding'] = reg_df['win_encoding'].astype('int64')

final_df.select_dtypes(['int64','float64']).corr()[['win_encoding']]

import statsmodels.api as sm
logit = sm.Logit(reg_df[['win_encoding']],reg_df[reg_df.columns.tolist()[:-2]]) #로지스틱 회귀분석 시행
result = logit.fit()
result.summary2()
result.pvalues
for i in range(len(result.params)):
    print('{} 1증가 할 때 마다 승리할 확률이 {} 배 증가'.format(result.params.keys()[i],np.exp(result.params.values[i])))

multiple_model = pd.DataFrame()
multiple_model['variance'] = result.params.keys().tolist()
multiple_model['coefficient'] = result.params.values.tolist()
solution = np.round(np.exp(result.params.values).tolist(),3)
s = [] 
for i in solution:
    s.append(str(i)+"배 증가")
multiple_model['solution'] = s
multiple_model['p_value'] = result.pvalues.tolist()


reg_df2 = reg_df[reg_df.columns.tolist()[:-2] + ['win_encoding']]
explain_var = reg_df2.columns.tolist()[:-1]

coef_ls = []
pvalue_ls = []
exp_ls = []
var_ls = []
simple_model = pd.DataFrame()
for i in explain_var:
    logit = sm.Logit(reg_df2[['win_encoding']],reg_df[[i]]) #로지스틱 회귀분석 시행
    result = logit.fit()
    
    coef_ls.append(result.params.values[0])
    pvalue_ls.append(result.pvalues.values[0])
    exp_ls.append(str(round(np.exp(result.params.values[0]),3)) + '배 증가')
    var_ls.append(i)

simple_model['variance'] = var_ls
simple_model['coefficient'] = coef_ls
simple_model['solution'] = exp_ls
simple_model['p_value'] = pvalue_ls