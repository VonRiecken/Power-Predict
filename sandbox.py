from power_predict.params import *
from power_predict.logic.registry import *
from power_predict.interface.main import *
from power_predict.logic.data import *
from power_predict.logic.preprocessor import *
from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

# df = load_local_df()
# df = targets_and_features(df)
# X = df.drop(columns=['Hydro', 'Solar', 'Wind', 'total_sol_wind_hyd'])
# y = df['total_sol_wind_hyd']
# X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)
# model = load_target_model('Total')
# X_fake = X_test.iloc[0:1,:]
# y_fake_pred = model.predict(X_fake)[0][3]

# print(y_fake_pred)#[0][3])

target = 'Total'

df = pd.DataFrame(locals, index=[0])
X_pred = df.drop(columns=[target])

# Preproccessing features
X_pred_preprocessed = preprocess_features(X_pred)
num_features = X_pred.select_dtypes(include=[np.number]).columns.tolist()

preprocessing_pipeline = ColumnTransformer(
transformers=[
    ('num', Pipeline(steps=[
        ('scaler', MinMaxScaler())
    ]), num_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), ['Country'])
])

X_process = Pipeline(steps=[('preprocessor', preprocessing_pipeline)])

X_pred_preprocessed = X_process.fit_transform(X_pred)

model = load_target_model(target)
y_pred_spec_model = model.predict(X_pred_preprocessed)[0][3]

print(y_pred_spec_model)
