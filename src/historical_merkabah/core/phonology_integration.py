#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from historical_merkabah.core import HistoricalPhonologyAdapter
from analysis.structural_attracteurs import analyser_phonetique, GroupesPhonetiques

@dataclass
class IntegratedPhonologyResult:
    caractere: str
    pinyin: str
    period: str
    reconstruction: str
    merkabah_historical: str
    initial: str
    final: str
    tone: int
    groupe_initiale: str
    groupe_finale: str
    confidence: float
    metadata: Dict[str, Any]

class TianDaoPhonologyIntegrator:
    def __init__(self, config_path: Optional[str] = None,
                 use_historical: bool = True, use_modern: bool = True):
        self.use_historical = use_historical
        self.use_modern = use_modern
        if use_historical:
            self.historical_adapter = HistoricalPhonologyAdapter()

    def process_text(self, text: str, pinyin_dict: Dict[str, str],
                     context: Optional[str] = None,
                     forced_period: Optional[str] = None) -> Dict:
        results = {'text': text, 'characters': [], 'global_analysis': {}, 'phonology_summary': {}}
        if self.use_historical:
            global_result = self.historical_adapter.analyze_text(text, pinyin_dict, forced_period)
            results['global_analysis'] = {
                'period_scores': global_result['global_period_scores'],
                'best_period': global_result['global_period_scores']['best_period']
            }
        for char in text:
            if char not in pinyin_dict:
                continue
            pinyin = pinyin_dict[char]
            char_result = self._process_character(char, pinyin, text, forced_period)
            results['characters'].append(asdict(char_result))
        results['phonology_summary'] = self._generate_summary(results['characters'])
        return results

    def _process_character(self, character: str, pinyin: str,
                           text_context: str, forced_period: Optional[str]) -> IntegratedPhonologyResult:
        hist = {}
        if self.use_historical:
            hr = self.historical_adapter.analyze_character(character, pinyin, text_context, forced_period)
            hist = {
                'period': hr.period_effective,
                'reconstruction': hr.historical.reconstruction,
                'merkabah_historical': hr.historical.merkabah,
                'confidence': hr.historical.confidence
            }
        else:
            hist = {'period': 'modern', 'reconstruction': pinyin, 'merkabah_historical': 'A1', 'confidence': 1.0}
        if self.use_modern:
            init_mod, fin_mod, ton_mod = analyser_phonetique(pinyin)
            groupe_init = GroupesPhonetiques.get_groupe_initiale(init_mod)
            groupe_fin = GroupesPhonetiques.get_groupe_finale(fin_mod)
        else:
            init_mod, fin_mod, ton_mod = '', '', 1
            groupe_init, groupe_fin = '', ''
        return IntegratedPhonologyResult(
            caractere=character, pinyin=pinyin, initial=init_mod, final=fin_mod,
            tone=ton_mod, groupe_initiale=groupe_init, groupe_finale=groupe_fin,
            metadata={'timestamp': datetime.now().isoformat()}, **hist
        )

    def _generate_summary(self, characters):
        if not characters:
            return {}
        summary = {'total_characters': len(characters), 'period_distribution': {},
                   'merkabah_distribution': {}, 'initial_groups': {}, 'final_groups': {}}
        for c in characters:
            p = c.get('period', 'unknown')
            summary['period_distribution'][p] = summary['period_distribution'].get(p, 0) + 1
            m = c.get('merkabah_historical', 'unknown')
            summary['merkabah_distribution'][m] = summary['merkabah_distribution'].get(m, 0) + 1
            ig = c.get('groupe_initiale', 'unknown')
            summary['initial_groups'][ig] = summary['initial_groups'].get(ig, 0) + 1
            fg = c.get('groupe_finale', 'unknown')
            summary['final_groups'][fg] = summary['final_groups'].get(fg, 0) + 1
        return summary