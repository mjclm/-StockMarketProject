from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier

from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV


def my_model(columns_to_scale):
    preprocessor = ColumnTransformer(
        transformers=[('num', StandardScaler(), columns_to_scale)],
        remainder='passthrough')

    rf = RandomForestClassifier(random_state=1, class_weight='balanced')
    lr = LogisticRegression(max_iter=500,  random_state=1, class_weight='balanced')
    pipe_lr = Pipeline([
        ('scale', StandardScaler()),
        ('reduce_dims', PCA(n_components=10)),
        ('clf', lr)
    ])

    vc = VotingClassifier(estimators=[('rf', rf), ('clf2', pipe_lr)], voting='hard')

    pipe = Pipeline(steps=[('preprocessor', preprocessor), ('vc', vc)])

    params = {
        'vc__rf__n_estimators': [10, 20, 40, 100],
        'vc__rf__max_depth': [5, 15, 25, 50],
        'vc__rf__min_samples_split': [.1, .05, .02, .01],
        'vc__clf2__clf__C': [1., .5, .1, .01]
    }

    search = RandomizedSearchCV(pipe, params, n_iter=20, random_state=1)

    return search
