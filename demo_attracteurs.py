#!/usr/bin/env python3
"""Démonstration d'utilisation des attracteurs (À METTRE DANS UN NOUVEAU FICHIER)"""

import sys
sys.path.insert(0, 'src')

from analysis.structural_attracteurs import (
    analyser_phonetique_complet,
    AnalyseAttracteurs,
    GroupesPhonetiques
)

# Analyse détaillée
print("=== Analyse phonétique complète ===")
analyse = analyser_phonetique_complet("zhōng")
print(f"Caractère: 中")
print(f"Pinyin: zhōng")
print(f"Initiale: {analyse.initiale} ({analyse.groupe_initiale})")
print(f"Finale: {analyse.finale} ({analyse.groupe_finale})")
print(f"Structure: {analyse.structure} (Attaque: {analyse.attaque}, Noyau: {analyse.noyau}, Coda: {analyse.coda})")

# Comparer deux prononciations
print("\n=== Comparaison de pinyin ===")
att = AnalyseAttracteurs()
comparaison = att.comparer_pinyin("dao4", "tao4")
print(f"Similarité dao4/tao4: {comparaison['scores']['total']:.0%}")

# Trouver des rimes
print("\n=== Recherche de rimes ===")
pinyins = ["dao4", "mao4", "gao4", "tian1", "nian1"]
rimes = att.trouver_rimes(pinyins)
for finale, mots in rimes.items():
    print(f"Finale {finale}: {', '.join(mots)}")
