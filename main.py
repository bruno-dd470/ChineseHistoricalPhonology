#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from historical_merkabah.core import HistoricalPhonologyAdapter

def main():
    print("=== TIAN-DAO-AI ===")
    print("Système d'analyse phonologique du chinois\n")
    adapter = HistoricalPhonologyAdapter()
    texte = "道可道，非常道。"
    pinyin_dict = {"道": "dao4", "可": "ke3", "非": "fei1", "常": "chang2"}
    print(f"Texte: {texte}")
    scores = adapter.detect_period(texte)
    print(f"Période détectée: {scores.best_period}")
    print("Scores:", scores.combined)
    res = adapter.analyze_text(texte, pinyin_dict)
    print(f"\nCaractères analysés: {res['metadonnees']['total_caracteres_analyse']}")
    for a in res['analyses_detaillees_historique']:
        print(f"{a['caractere']}: {a['historical']['reconstruction']} (Merkabah {a['historical']['merkabah']})")
    return 0

if __name__ == "__main__":
    sys.exit(main())