import os.path as path
from unittest import TestCase

from hamcrest import assert_that, equal_to

from detection.arguments import get_dataset_path
from detection.data.factory import collect, load_wikimatrix
from detection.utils import MockDataset, translations_to_torch_dataset


class TestFactory(TestCase):
    def test_collect_tatoeba(self):
        dataset_name, ext = 'tatoeba', 'bin'
        datasets = collect(dataset_name, save=True, ext=ext)
        assert_that(len(datasets), equal_to(6))
        dataset_path = get_dataset_path(dataset_name, langs=['de', 'en'], ext=ext)
        assert_that(path.exists(dataset_path), equal_to(True))
        dataset_path = get_dataset_path(dataset_name, langs=['fr', 'ru'], ext=ext)
        assert_that(path.exists(dataset_path), equal_to(True))

    def test_collect_wikimatrix(self):
        dataset = load_wikimatrix(lang1='de', lang2='en', size=10)
        assert_that(len(dataset), equal_to(10))
        assert_that(dataset[0]['de'], equal_to('Gott ist nicht nur der Allmächtige, sondern auch der Erbarmende.'))
        assert_that(dataset[0]['en'], equal_to('And He is The Almighty, The Compassionate."'))


class TestUtils(TestCase):
    def test_translations_list(self):
        targets, translations = MockDataset.targets(), MockDataset.translations()
        dataset = translations_to_torch_dataset(targets, translations, device='cpu')
        train_dataset, eval_dataset = dataset.split()

        assert_that(len(train_dataset), equal_to(3))
        assert_that(len(eval_dataset), equal_to(1))
