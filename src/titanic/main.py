import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import category_encoders as ce
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

unlabled_colmuns = ['Sex', 'Cabin', 'Embarked']

x_all = pd.concat([train_x, test_x], axis=0)
for col in unlabled_colmuns:
    le = LabelEncoder()
    le.fit(x_all[col].fillna('NA'))
    train_x[col] = le.transform(train_x[col].fillna('NA'))
    test_x[col] = le.transform(test_x[col].fillna('NA'))

model = XGBClassifier(n_estimators=20, random_state=71)
model.fit(train_x, train_y)

pred = model.predict_proba(test_x)[:, 1]
test_y = np.where(pred > 0.5, 1, 0)
submission = pd.DataFrame({'PassengerId': test_input['PassengerId'], 'Survived': test_y})
submission.to_csv('../output/titanic/submission.csv', index=False)