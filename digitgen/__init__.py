import logging

from . import augmentation
from . import digit
from . import utils
from .digit_generator import DigitGenerator
from .utils.helper import test_annotations

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

__all__ = [
    'DigitGenerator',
    'test_annotations',
    'augmentation',
    'utils',
    'digit'
]
