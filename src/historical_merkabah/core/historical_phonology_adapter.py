#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
historical_phonology_adapter.py

Adaptateur pour la phonologie historique chinoise.
"""

from __future__ import annotations
import sys
from pathlib import Path

# Ajout du chemin src pour les imports absolus
ROOT = Path(__file__).resolve().parents[3]  # jusqu'à src/
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Literal, Tuple

# Import des modules internes
from .period_detectors import (
    LexicalPeriodDetector,
    CharacterUsageDetector,
    SyntacticPeriodDetector,
)
from .temporal_router import TemporalRouter

# Import du module moderne (attracteurs)
from analysis.structural_attracteurs import analyser_phonetique, GroupesPhonetiques


PeriodLabel = Literal["archaic", "medieval", "early_mandarin", "modern"]


@dataclass
class PeriodScores:
    combined: Dict[PeriodLabel, float]
    lexical: Dict[PeriodLabel, float]
    character_usage: Dict[PeriodLabel, float]
    syntax: Dict[PeriodLabel, float]
    best_period: PeriodLabel


@dataclass
class HistoricalPhoneticInfo:
    period: PeriodLabel
    db_period_used: str
    character: str
    reconstruction: str
    initial: str
    final: str
    tone: str
    merkabah: str
    confidence: float


@dataclass
class ModernPhoneticInfo:
    pinyin: str
    initial: str
    final: str
    tone: int
    groupe_initiale: str
    groupe_finale: str


@dataclass
class HistoricalPhonologyResult:
    caractere: str
    period_scores: PeriodScores
    period_effective: PeriodLabel
    historical: HistoricalPhoneticInfo
    modern: ModernPhoneticInfo


class HistoricalPhonologyAdapter:
    PERIODS: List[PeriodLabel] = ["archaic", "medieval", "early_mandarin", "modern"]

    def __init__(self, weight_lexical=0.5, weight_character=0.3, weight_syntax=0.2):
        self.lexical_detector = LexicalPeriodDetector()
        self.char_detector = CharacterUsageDetector()
        self.syntax_detector = SyntacticPeriodDetector()
        self.router = TemporalRouter()
        total = weight_lexical + weight_character + weight_syntax
        self.weight_lexical = weight_lexical / total
        self.weight_character = weight_character / total
        self.weight_syntax = weight_syntax / total

    def detect_period(self, text: str) -> PeriodScores:
        lex = self.lexical_detector.analyze(text)
        ch = self.char_detector.analyze(text)
        syn = self.syntax_detector.analyze(text)

        def _normalize(block: Dict[str, float]) -> Dict[PeriodLabel, float]:
            full = {p: float(block.get(p, 0.0)) for p in self.PERIODS}
            s = sum(full.values())
            if s > 0:
                return {p: v / s for p, v in full.items()}
            return {p: 1.0 / len(self.PERIODS) for p in self.PERIODS}

        lex_n = _normalize(lex)
        ch_n = _normalize(ch)
        syn_n = _normalize(syn)

        combined = {}
        for p in self.PERIODS:
            combined[p] = (self.weight_lexical * lex_n[p] +
                           self.weight_character * ch_n[p] +
                           self.weight_syntax * syn_n[p])
        s_comb = sum(combined.values())
        if s_comb > 0:
            combined = {p: v / s_comb for p, v in combined.items()}
        best_period = max(combined, key=combined.get)
        return PeriodScores(combined=combined, lexical=lex_n,
                            character_usage=ch_n, syntax=syn_n,
                            best_period=best_period)

    @staticmethod
    def _map_period_to_router_db_period(period: PeriodLabel) -> str:
        if period == "archaic":
            return "archaic"
        if period == "medieval":
            return "archaic"
        if period == "early_mandarin":
            return "modern"
        return "modern"

    def analyze_character(self, caractere: str, pinyin_modern: str,
                          text_context: Optional[str] = None,
                          forced_period: Optional[PeriodLabel] = None) -> HistoricalPhonologyResult:
        # Détection de période
        if forced_period is not None:
            base_scores = {p: 0.0 for p in self.PERIODS}
            base_scores[forced_period] = 1.0
            period_scores = PeriodScores(combined=base_scores.copy(),
                                         lexical=base_scores.copy(),
                                         character_usage=base_scores.copy(),
                                         syntax=base_scores.copy(),
                                         best_period=forced_period)
            period_effective = forced_period
        else:
            if text_context is None:
                base_scores = {p: 0.0 for p in self.PERIODS}
                base_scores["modern"] = 1.0
                period_scores = PeriodScores(combined=base_scores.copy(),
                                             lexical=base_scores.copy(),
                                             character_usage=base_scores.copy(),
                                             syntax=base_scores.copy(),
                                             best_period="modern")
                period_effective = "modern"
            else:
                period_scores = self.detect_period(text_context)
                period_effective = period_scores.best_period

        db_period = self._map_period_to_router_db_period(period_effective)
        router_data = self.router.get_analysis(caractere, period=db_period)

        if db_period == "archaic":
            reconstruction = str(router_data.get("reconstruction", f"[{caractere}]"))
            hist_initial = str(router_data.get("initial", "?"))
            hist_final = str(router_data.get("final", "?"))
            hist_tone = str(router_data.get("tone", "?"))
        else:
            pinyin_db = str(router_data.get("pinyin", pinyin_modern))
            reconstruction = pinyin_db
            hist_initial = str(router_data.get("initial", "?"))
            hist_final = str(router_data.get("final", "?"))
            hist_tone = str(router_data.get("tone", "?"))
        merkabah = str(router_data.get("merkabah", "A1"))
        confidence = float(router_data.get("confidence", 0.5))

        historical_info = HistoricalPhoneticInfo(
            period=period_effective, db_period_used=db_period, character=caractere,
            reconstruction=reconstruction, initial=hist_initial, final=hist_final,
            tone=hist_tone, merkabah=merkabah, confidence=confidence
        )

        init_mod, fin_mod, ton_mod = analyser_phonetique(pinyin_modern)
        groupe_init = GroupesPhonetiques.get_groupe_initiale(init_mod)
        groupe_fin = GroupesPhonetiques.get_groupe_finale(fin_mod)
        modern_info = ModernPhoneticInfo(pinyin=pinyin_modern, initial=init_mod,
                                         final=fin_mod, tone=ton_mod,
                                         groupe_initiale=groupe_init, groupe_finale=groupe_fin)

        return HistoricalPhonologyResult(caractere=caractere, period_scores=period_scores,
                                         period_effective=period_effective,
                                         historical=historical_info, modern=modern_info)

    def analyze_text(self, texte: str, dictionnaire_pinyin: Dict[str, str],
                     forced_period: Optional[PeriodLabel] = None,
                     chinese_only: bool = True) -> Dict:
        if forced_period is not None:
            global_scores = {"combined": {p: (1.0 if p == forced_period else 0.0) for p in self.PERIODS}}
        else:
            ps = self.detect_period(texte)
            global_scores = {
                "combined": ps.combined,
                "lexical": ps.lexical,
                "character_usage": ps.character_usage,
                "syntax": ps.syntax,
                "best_period": ps.best_period,
            }
        analyses = []
        total_chars = 0
        total_analysed = 0
        for c in texte:
            if chinese_only and not ("\u4e00" <= c <= "\u9fff"):
                continue
            total_chars += 1
            if c not in dictionnaire_pinyin:
                continue
            pinyin = dictionnaire_pinyin[c]
            res = self.analyze_character(c, pinyin, text_context=texte, forced_period=forced_period)
            total_analysed += 1
            analyses.append({
                "caractere": res.caractere,
                "period_effective": res.period_effective,
                "period_scores": {
                    "combined": res.period_scores.combined,
                    "lexical": res.period_scores.lexical,
                    "character_usage": res.period_scores.character_usage,
                    "syntax": res.period_scores.syntax,
                },
                "historical": asdict(res.historical),
                "modern": asdict(res.modern),
            })
        return {
            "metadonnees": {"total_caracteres_chinois": total_chars, "total_caracteres_analyse": total_analysed},
            "global_period_scores": global_scores,
            "analyses_detaillees_historique": analyses,
        }