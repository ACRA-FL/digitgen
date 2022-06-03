from .digit_generator import DigitGenerator
from .utils.helper import test_annotations
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

__all__ = [
    'DigitGenerator',
    'test_annotations'
]


