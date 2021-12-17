from typing import Any, Dict, List, Optional

from detection.models.smr.core import SuffixArray
from detection.models.language_model import LanguageModel


def check_paragraph(paragraph: str) -> bool:
    """
    TODO: понять, где вызывать предикат
    """
    return len(paragraph) >= 100


def retrieve_prefix(paragraph: str, sentence_num: int = 2) -> str:
    """
    TODO-Doc
    """
    sentences = paragraph.strip().split('.')
    sentences = [sent.strip() + '.' for sent in sentences if len(sent)]
    prefix = " ".join(sentences[:sentence_num])
    return prefix


def super_maximal_repeat(paragraph: str) -> str:
    suffix_array = SuffixArray(paragraph)
    return suffix_array.longest_repeated_substring()


def generate_language_model(
    paragraphs: List[str],
    sentence_num: int = 2,
    lm_params: Optional[Dict[str, Any]] = None,
    size: Optional[int] = None
) -> List[str]:
    """
    TODO-Doc
    """
    language_model = LanguageModel()
    prefixes = [
        retrieve_prefix(paragraph, sentence_num=sentence_num)
        for paragraph in paragraphs
    ]
    return language_model(prefixes, **(lm_params or {}))