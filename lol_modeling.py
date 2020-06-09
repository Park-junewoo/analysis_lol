#학습
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn import metrics 

x_train , x_test, y_train,y_test = train_test_split(x,y,test_size= 0.3)

xgb=XGBClassifier(n_estimators=500)   
xgb.fit(x_train,y_train)
y_pred = xgb.predict(x_test)
metrics.accuracy_score(y_test,y_pred)

#교차검증
skf = StratifiedKFold(n_splits=5,shuffle=True,random_state = 0)
xgb=XGBClassifier(n_estimators=500)
scores = cross_val_score(xgb,data_scaled,y,cv=skf)
scores.mean()




#로지스틱 회귀분석
logreg = LogisticRegression()
logreg.fit(x_train,y_train)
y_pred = logreg.predict(x_test)
accuracy_score(y_pred, y_test)

#랜덤포레스트
rf = RandomForestClassifier(n_estimators=500)
rf.fit(x_train, y_train)
y_pred = rf.predict(x_test)
metrics.accuracy_score(y_test,y_pred)

#그라디언트부스팅
gbc = GradientBoostingClassifier()
gbc.fit(x_train,y_train)
y_pred = gbc.predict(x_test)
accuracy_score(y_test,y_pred)



#그라디언트부스팅 하이퍼파라미터 조정
from sklearn.model_selection import GridSearchCV
gb_param_gird={
'n_estimators' : [500,1000,1500],
'max_depth' : [3,5,7],
'min_samples_leaf' : [3,5],
'min_samples_split' : [2,3,5],
'learning_rate':[0.05,0.1,0.2]
}

gbc_grid = GridSearchCV(gbc,param_grid=gb_param_gird,scoring = "accuracy",n_jobs=-1,verbose=1)
gbc_grid.fit(x_train,y_train)

gb_best_e = gbc_grid.best_estimator_
y_pred = gb_best_e.predict(x_test)
metrics.accuracy_score(y_test,y_pred)