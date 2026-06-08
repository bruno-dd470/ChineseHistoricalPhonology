#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict

class LexicalPeriodDetector:
    def analyze(self, text: str) -> Dict[str, float]:
        # Simplifié : retourne des scores fixes pour l'exemple
        return {'archaic': 0.0, 'medieval': 1.0, 'early_mandarin': 0.0, 'modern': 0.0}

class CharacterUsageDetector:
    def analyze(self, text: str) -> Dict[str, float]:
        return {'archaic': 0.0, 'medieval': 0.5, 'early_mandarin': 0.5, 'modern': 0.0}

class SyntacticPeriodDetector:
    def analyze(self, text: str) -> Dict[str, float]:
        return {'archaic': 0.25, 'medieval': 0.25, 'early_mandarin': 0.25, 'modern': 0.25}