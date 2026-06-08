"""
Module core de la phonologie historique.
"""
from .historical_phonology_adapter import HistoricalPhonologyAdapter
from .temporal_router import TemporalRouter
from .period_detectors import LexicalPeriodDetector, CharacterUsageDetector, SyntacticPeriodDetector

__all__ = [
    'HistoricalPhonologyAdapter',
    'TemporalRouter',
    'LexicalPeriodDetector',
    'CharacterUsageDetector',
    'SyntacticPeriodDetector',
]
