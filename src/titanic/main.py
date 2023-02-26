import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, learning_curve
from sklearn.metrics import classification_report, roc_curve, auc, precision_recall_curve
from xgboost import XGBClassifier

train_input = pd.read_csv("../input/titanic/train.csv")
test_input = pd.read_csv("../input/titanic/test.csv")

train_x = train_input.drop(['Survived', 'PassengerId', 'Name', 'Ticket'], axis=1)
train_y = train_input['Survived']
test_x = test_input.drop(['PassengerId', 'Name', 'Ticket'], axis=1)

# Cabin の欠損地が大きいので Cabin を予測する

# Cabin 以外のカラムをラベル付け
unlabled_colmuns = ['Sex', 'Embarked']
x_all = pd.concat([train_x, test_x], axis=0)
for col in unlabled_colmuns:
    le = LabelEncoder()
    le.fit(x_all[col].fillna('NA'))
    train_x[col] = le.transform(train_x[col].fillna('NA'))
    test_x[col] = le.transform(test_x[col].fillna('NA'))
    x_all[col] = le.transform(x_all[col].fillna('NA'))

# train の cabin を予測するためのデータを用意
train_x_for_cabin = x_all[~x_all['Cabin'].isna()].drop(['Cabin'], axis=1)
train_y_for_cabin = x_all[~x_all['Cabin'].isna()]['Cabin']
test_x_for_cabin = x_all[x_all['Cabin'].isna()].drop(['Cabin'], axis=1)

# train_x_for_cabin の Cabin をラベル付け
le = LabelEncoder()
le.fit(train_y_for_cabin)
train_y_for_cabin = le.transform(train_y_for_cabin)

model = XGBClassifier(n_estimators=20, random_state=71)
model.fit(train_x_for_cabin, train_y_for_cabin)

# test_x_for_cabin の Cabin を予測
test_y_for_cabin = model.predict(test_x_for_cabin)

# train_y_for_cabin, test_y_for_cabin から train_x, test_x を生成
x_all.loc[~x_all['Cabin'].isna(), ['Cabin']] = train_y_for_cabin.astype(int)
x_all.loc[x_all['Cabin'].isna(), ['Cabin']] = test_y_for_cabin.astype(int)
x_all['Cabin'] = x_all['Cabin'].astype(int)
train_x = x_all[0:train_x.shape[0]].copy()
test_x = x_all[train_x.shape[0]:(train_x.shape[0]+test_x.shape[0])].copy()

# 予測
model = XGBClassifier(n_estimators=20, random_state=71)
model.fit(train_x, train_y)
pred = model.predict_proba(test_x)[:, 1]
test_y = np.where(pred > 0.5, 1, 0)

submission = pd.DataFrame({'PassengerId': test_input['PassengerId'], 'Survived': test_y})
submission.to_csv('../output/titanic/submission.csv', index=False)

# 普通に精度が悪いので要勉強