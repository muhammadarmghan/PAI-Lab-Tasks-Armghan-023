
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# ============================
# Load Data
# ============================
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# ============================
# Data Preparation
# ============================
def build_features(df):
    temp = df.copy()

    def parse_cabin(value):
        if pd.isna(value):
            return pd.Series([np.nan, np.nan, np.nan])
        parts = str(value).split('/')
        if len(parts) == 3:
            return pd.Series(parts)
        return pd.Series([np.nan, np.nan, np.nan])

    temp[['Deck', 'CabinNo', 'Side']] = temp['Cabin'].apply(parse_cabin)
    temp.drop(['Name', 'Cabin'], axis=1, inplace=True)
    return temp

train_proc = build_features(train_data)
test_proc = build_features(test_data)

# ============================
# Features / Target
# ============================
X = train_proc.drop(['PassengerId', 'Transported'], axis=1)
y = train_proc['Transported'].astype(int)

X_test = test_proc.drop(['PassengerId'], axis=1)
pid = test_proc['PassengerId']

X['CabinNo'] = pd.to_numeric(X['CabinNo'])
X_test['CabinNo'] = pd.to_numeric(X_test['CabinNo'])

num_features = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck', 'CabinNo']
cat_features = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP', 'Deck', 'Side']

# ============================
# Pipelines
# ============================
num_pipe = Pipeline([
    ('impute', SimpleImputer(strategy='median')),
    ('scale', StandardScaler())
])

cat_pipe = Pipeline([
    ('impute', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

processor = ColumnTransformer([
    ('num', num_pipe, num_features),
    ('cat', cat_pipe, cat_features)
])

classifier = RandomForestClassifier(
    n_estimators=120,
    min_samples_leaf=2,
    random_state=21
)

model = Pipeline([
    ('processor', processor),
    ('rf', classifier)
])

# ============================
# Train & Predict
# ============================
print("Training model...")
model.fit(X, y)

print("Predicting test data...")
pred = model.predict(X_test).astype(bool)

output = pd.DataFrame({
    'PassengerId': pid,
    'Transported': pred
})

output.to_csv('submission.csv', index=False)
print("submission.csv saved.")
