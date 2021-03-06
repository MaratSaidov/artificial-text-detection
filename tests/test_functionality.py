from typing import List, Union
from unittest import TestCase

import numpy as np
from hamcrest import assert_that, equal_to, greater_than, has_items
from transformers import EvalPrediction

from artificial_detection.data.factory import collect
from artificial_detection.data.generate import get_generation_dataset, translate_dataset
from artificial_detection.models.validate import compute_metrics
from artificial_detection.utils import MockDataset, translations_to_torch_dataset


def reverse_transform(s: Union[str, List[str]]) -> Union[str, List[str]]:
    if isinstance(s, str):
        return "".join(reversed(s))
    return ["".join(reversed(element)) for element in s]


class TestFunctionality(TestCase):
    dataset = None
    translations = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.dataset = MockDataset.dataset
        cls.targets = MockDataset.targets()
        cls.translations = translate_dataset(cls.dataset, reverse_transform, src_lang="ru")

    def test_translations(self):
        assert_that(len(self.translations), equal_to(2))
        assert_that(self.translations, equal_to(["ьнед йырбод", "етинивзи"]))

    def test_compute_metrics(self):
        eval_pred = EvalPrediction(
            predictions=np.array([[0], [1]]),
            label_ids=np.array([0, 1]),
        )
        results = compute_metrics(eval_pred)
        metrics_names = list(results.keys())
        metrics_values = list(results.values())

        assert_that(metrics_names, equal_to(["accuracy", "f1", "precision", "recall"]))
        for value in metrics_values:
            assert_that(type(value), equal_to(float))

    def test_translations_to_torch(self):
        dataset = translations_to_torch_dataset(
            self.targets,
            self.translations,
            device="cpu",
        )
        encodings_keys = list(dataset.encodings.keys())
        assert_that(encodings_keys, has_items(*["input_ids", "attention_mask"]))

        train_dataset, eval_dataset = dataset.split()
        assert_that(len(train_dataset.encodings["input_ids"]), equal_to(3))
        assert_that(len(eval_dataset.encodings["input_ids"]), equal_to(1))

    def test_generation_dataset(self):
        dataset_name, ext = "tatoeba", "bin"
        datasets = collect(dataset_name, save=False, ext=ext)
        dataset = datasets[0]
        sized_dataset = get_generation_dataset(dataset, dataset_name, size=10)
        assert_that(len(sized_dataset), equal_to(10))
        unsized_dataset = get_generation_dataset(dataset, dataset_name)
        assert_that(len(unsized_dataset), greater_than(5 * (10 ** 5)))
