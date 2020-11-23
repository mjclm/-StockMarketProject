from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier


def my_model(columns_to_scale):
    preprocessor = ColumnTransformer(
        transformers=[('num', StandardScaler(), columns_to_scale)],
        remainder='passthrough')

    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', RandomForestClassifier(class_weight='balanced', random_state=0))])

    return clf
