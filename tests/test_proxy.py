from typing import List

import pandas as pd
import pytest
from hamcrest import assert_that, close_to

from artificial_detection.data.proxy import BERTScoreMetrics, BLEUMetrics, Calculator, METEORMetrics, TERMetrics


@pytest.fixture()
def mock_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "sources": "Il va à la bibliothèque pour lire des livres.",
                "translations": "Он едет в библиотеку, чтобы читать книги.",
                "targets": "Он ходит в библиотеку, чтобы читать книги.",
            },
            {
                "sources": "It is no use crying over spilt milk.",
                "translations": "Нет смысла плакать над пролитым молоком.",
                "targets": "Слезами горю не поможешь.",
            },
        ]
    )


@pytest.fixture()
def statistical_metrics() -> List[str]:
    return ["BLEU", "METEOR", "TER"]


@pytest.fixture()
def neural_metrics() -> List[str]:
    return ["BLEURT", "Comet"]


@pytest.fixture()
def richness_metrics() -> List[str]:
    return [
        "LexicalRichnessWords",
        "LexicalRichnessTerms",
        "LexicalRichnessTTR",
        "LexicalRichnessRTTR",
        "LexicalRichnessCTTR",
        "LexicalRichnessMTLD",
        "LexicalRichnessHerdan",
    ]


def test_bleu(mock_dataset: pd.DataFrame) -> None:
    metrics = BLEUMetrics()
    scores = metrics.compute(mock_dataset)
    gt_scores = [75.062, 6.567]
    for i, score in enumerate(scores):
        assert_that(score, close_to(gt_scores[i], 0.01))


def test_meteor(mock_dataset: pd.DataFrame) -> None:
    metrics = METEORMetrics()
    scores = metrics.compute(mock_dataset)
    gt_scores = [0.882, 0.096]
    for i, score in enumerate(scores):
        assert_that(score, close_to(gt_scores[i], 0.01))


def test_ter(mock_dataset: pd.DataFrame) -> None:
    metrics = TERMetrics()
    scores = metrics.compute(mock_dataset)
    gt_scores = [14.286, 150.0]
    for i, score in enumerate(scores):
        assert_that(score, close_to(gt_scores[i], 0.01))


def test_bleurt(mock_dataset: pd.DataFrame) -> None:
    pass


def test_bert_score(mock_dataset: pd.DataFrame) -> None:
    metrics = BERTScoreMetrics(model_path="/home/masaidov/.cache/huggingface/metrics/bert_score")
    scores = metrics.compute(mock_dataset)


def test_calculator_statistical_metrics(mock_dataset: pd.DataFrame, statistical_metrics: List[str]) -> None:
    model_specific_dict = {metric_name: {} for metric_name in statistical_metrics}
    calculator = Calculator(df_or_path=mock_dataset, model_specific_dict=model_specific_dict)
    scores_df = calculator.compute(metrics_names=statistical_metrics)
    gt_scores = [40.815, 0.489, 82.143]
    for i, metrics_name in enumerate(statistical_metrics):
        assert_that(scores_df[metrics_name].mean(), close_to(gt_scores[i], 0.01))


def test_calculator_lexical_richness_metrics(mock_dataset: pd.DataFrame, richness_metrics: List[str]) -> None:
    model_specific_dict = {metric_name: {} for metric_name in richness_metrics}
    calculator = Calculator(df_or_path=mock_dataset, model_specific_dict=model_specific_dict)
    scores_df = calculator.compute(metrics_names=richness_metrics)
