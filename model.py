import joblib
from sklearn import metrics
from exceptions import InvalidMeticException
from typing import Dict, Any
import random
import pandas as pd


METRICS_MAPPING = {
    'accuracy': metrics.accuracy_score,
    'balanced_accuracy': metrics.balanced_accuracy_score,
    'average_precision': metrics.average_precision_score,
    'brier_score_loss': metrics.brier_score_loss,
    'f1': metrics.f1_score,
    'f1_micro': metrics.f1_score,
    'f1_macro': metrics.f1_score,
    'f1_weighted': metrics.f1_score,
    'f1_samples': metrics.f1_score,
    'neg_log_loss': metrics.log_loss,
    'precision': metrics.precision_score,
    'recall': metrics.recall_score,
    'roc_auc': metrics.roc_auc_score,
    'adjusted_mutual_info_score': metrics.adjusted_mutual_info_score,
    'adjusted_rand_score': metrics.adjusted_rand_score,
    'completeness_score': metrics.completeness_score,
    'fowlkes_mallows_score': metrics.fowlkes_mallows_score,
    'homogeneity_score': metrics.homogeneity_score,
    'mutual_info_score': metrics.mutual_info_score,
    'normalized_mutual_info_score': metrics.normalized_mutual_info_score,
    'v_measure_score': metrics.v_measure_score,
    'explained_variance': metrics.explained_variance_score,
    'neg_mean_absolute_error': metrics.mean_absolute_error,
    'neg_mean_squared_error': metrics.mean_squared_error,
    'neg_mean_squared_log_error': metrics.mean_squared_log_error,
    'neg_median_absolute_error': metrics.median_absolute_error,
    'r2': metrics.r2_score
}


class TrainedModel(object):

    def __init__(self, model: Any, metadata: Dict) -> None:
        self.model = model
        self.metadata = metadata

    @staticmethod
    def load(path: str) -> Any:
        return joblib.load(path)

    def save(self, path: str) -> None:
        joblib.dump(self, path)

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        return self.model.predict(data)

    def evaluate(self, data: pd.DataFrame, expected_output: pd.DataFrame, metric: str='accuracy') -> float:  # noqa
        return random.randint(0, 100)

        # Can also use the actual models (generated using generate_models.py)
        # Uncomment the above line to run the actual models
        if metric not in METRICS_MAPPING:
            raise InvalidMeticException
        actual_output = self.predict(data)
        eval_function = METRICS_MAPPING[metric]
        return eval_function(expected_output, actual_output)
