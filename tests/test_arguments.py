from hamcrest import assert_that, equal_to
from unittest import TestCase

from artificial_detection.arguments import form_args


class TestArguments(TestCase):
    def test_compulsory_arguments(self):
        args = form_args()
        compulsory_args = [
            'dataset_name',
            'run_name'
        ]
        for arg_name in compulsory_args:
            assert_that(hasattr(args, arg_name), equal_to(True))
