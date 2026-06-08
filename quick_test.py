#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from historical_merkabah.core import HistoricalPhonologyAdapter
from analysis.structural_attracteurs import analyser_phonetique, GroupesPhonetiques

def test_phonology():
    print("=== Test phonologie historique ===")
    adapter = HistoricalPhonologyAdapter()
    text = "道可道，非常道。"
    scores = adapter.detect_period(text)
    print(f"Période: {scores.best_period}")
    pinyin = {"道":"dao4","可":"ke3","非":"fei1","常":"chang2"}
    res = adapter.analyze_text(text, pinyin)
    print(f"Caractères analysés: {res['metadonnees']['total_caracteres_analyse']}")
    return True

def test_attractors():
    print("\n=== Test attracteurs ===")
    for p in ["dao4","ke3","fei1"]:
        i,f,t = analyser_phonetique(p)
        gi = GroupesPhonetiques.get_groupe_initiale(i)
        gf = GroupesPhonetiques.get_groupe_finale(f)
        print(f"{p} -> initiale {i} ({gi}), finale {f} ({gf})")
    return True

if __name__ == "__main__":
    test_phonology()
    test_attractors()