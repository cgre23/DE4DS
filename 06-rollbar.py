import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelBinarizer, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn_pandas import DataFrameMapper
from sklearn.pipeline import make_pipeline

# new imports
import rollbar  # pip install rollbar
from dotenv import load_dotenv, find_dotenv  # pip install python-dotenv

# find the dotenv file if it lives beside this script
load_dotenv(find_dotenv())

# load the key-value secret
ROLLBAR = os.getenv("ROLLBAR")
rollbar.init(ROLLBAR, 'production')

df = pd.read_csv('/home/christiangrech/Documents/GitHub/DE4DS/data/football.csv')
df = df.sort_values(['name', 'week']).reset_index(drop=True)
df['yards_2'] = df.groupby('name')['yards'].shift(2)
df['yards_1'] = df.groupby('name')['yards'].shift(1)
df = df.dropna(subset=["yards_1", "yards_2"])

target = 'yards'
y = df[target]
X = df[['position', 'yards_1', 'yards_2']]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.10,
    random_state=42,
    shuffle=False
)

mapper = DataFrameMapper([
    (['position'], [SimpleImputer(strategy="most_frequent"), LabelBinarizer()]),
    (['yards_1'], [SimpleImputer(), StandardScaler()]),
    (['yards_2'], [SimpleImputer(), StandardScaler()]),
    ], df_out=True)

model = LinearRegression()

pipe = make_pipeline(mapper, model)
pipe.fit(X_train, y_train)
score = round(pipe.score(X_train, y_train), 2)

# sound the alarm if below
threshold = 0.80
if score < threshold:
    rollbar.report_message(
        f"score ({score}) is below acceptable threshold ({threshold})"
    )

with open("/home/christiangrech/Documents/GitHub/DE4DS/pickles/pipe.pkl", "wb") as f:
    pickle.dump(pipe, f)
