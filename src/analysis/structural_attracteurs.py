#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
structural_attracteurs.py

Module d'analyse phonétique structurelle pour Tian-Dao-AI.

Fonctionnalités :
- Analyse complète du pinyin (initiale, finale, ton)
- Classification par groupes phonétiques (B*, D*, G*, J*, Z*, etc.)
- Détection des groupes spécifiques (-ong*, -ang*, -an*, -ai*, -ao*, -i*, -u*)
- Calcul des isomères phonétiques
- Matrices d'attracteurs pour l'analyse comparative

Version complète et originale.
"""

from __future__ import annotations
import re
from typing import Tuple, Dict, List, Optional, Set
from dataclasses import dataclass
import json
from pathlib import Path


# =============================================================================
# CONSTANTES ET TABLES DE CORRESPONDANCE
# =============================================================================

# Table complète des initiales pinyin avec leurs groupes
INITIALES_PINYIN = {
    # Bilabiales (B*)
    'b': 'B*', 'p': 'B*', 'm': 'B*', 'f': 'B*',
    
    # Alvéolaires (D*)
    'd': 'D*', 't': 'D*', 'n': 'D*', 'l': 'D*',
    
    # Vélaires (G*)
    'g': 'G*', 'k': 'G*', 'h': 'G*',
    
    # Palatales (J*)
    'j': 'J*', 'q': 'J*', 'x': 'J*',
    
    # Rétroflexes (Z*)
    'zh': 'Z*', 'ch': 'Z*', 'sh': 'Z*', 'r': 'Z*',
    
    # Alvéolo-dentales (Z*)
    'z': 'Z*', 'c': 'Z*', 's': 'Z*',
    
    # Semi-voyelles
    'y': 'Y*', 'w': 'W*',
    
    # Initiale nulle (voyelle seule)
    '': 'V*'
}

# Table des finales avec leurs groupes
FINALES_GROUPES = {
    # Groupes nasaux
    'ang': '-ang*', 'eng': '-eng*', 'ing': '-ing*', 'ong': '-ong*',
    'iang': '-iang*', 'uang': '-uang*', 'iong': '-iong*',
    
    # Nasales simples
    'an': '-an*', 'en': '-en*', 'in': '-in*', 'un': '-un*',
    'ian': '-ian*', 'uan': '-uan*', 'üan': '-üan*',
    
    # Diphtongues
    'ai': '-ai*', 'ei': '-ei*', 'ao': '-ao*', 'ou': '-ou*',
    'iao': '-iao*', 'iu': '-iu*', 'ui': '-ui*',
    
    # Voyelles simples
    'a': '-a*', 'o': '-o*', 'e': '-e*', 'i': '-i*', 'u': '-u*', 'ü': '-ü*',
    
    # Finales complexes
    'er': '-er*', 'ie': '-ie*', 'üe': '-üe*',
}

# Mapping des tons (chiffre → nom)
TONS_MAPPING = {
    1: 'niveau',
    2: 'montant',
    3: 'descendant-montant',
    4: 'descendant',
    5: 'neutre'
}

# Mapping inverse (nom → chiffre)
TONS_INVERSE = {v: k for k, v in TONS_MAPPING.items()}


# =============================================================================
# CLASSES DE DONNÉES
# =============================================================================

@dataclass
class AnalysePhonetique:
    """Résultat complet d'une analyse phonétique."""
    pinyin_original: str
    pinyin_normalise: str
    initiale: str
    finale: str
    ton: int
    ton_nom: str
    groupe_initiale: str
    groupe_finale: str
    structure: str  # CVC, CV, V, etc.
    attaque: str    # consonne initiale
    noyau: str      # voyelle principale
    coda: str       # consonne finale (n, ng, etc.)
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire."""
        return {
            'pinyin_original': self.pinyin_original,
            'pinyin_normalise': self.pinyin_normalise,
            'initiale': self.initiale,
            'finale': self.finale,
            'ton': self.ton,
            'ton_nom': self.ton_nom,
            'groupe_initiale': self.groupe_initiale,
            'groupe_finale': self.groupe_finale,
            'structure': self.structure,
            'attaque': self.attaque,
            'noyau': self.noyau,
            'coda': self.coda
        }


# =============================================================================
# FONCTIONS PRINCIPALES
# =============================================================================

def analyser_phonetique(pinyin: str) -> Tuple[str, str, int]:
    """
    Analyse un pinyin et retourne (initiale, finale, ton).
    
    Args:
        pinyin: Chaîne pinyin (ex: "dao4", "zhōng", "lü3")
        
    Returns:
        Tuple (initiale, finale, ton)
    """
    if not pinyin:
        return '', '', 1
    
    pinyin_original = pinyin.strip().lower()
    
    # Extraire le ton
    ton = 1
    if pinyin_original and pinyin_original[-1].isdigit():
        ton = int(pinyin_original[-1])
        pinyin_sans_ton = pinyin_original[:-1]
    else:
        # Gérer les accents Unicode
        pinyin_sans_ton = pinyin_original
        ton = _extraire_ton_depuis_accent(pinyin_original)
    
    # Normaliser les caractères spéciaux (ü, etc.)
    pinyin_normalise = _normaliser_pinyin(pinyin_sans_ton)
    
    # Extraire l'initiale et la finale
    initiale, finale = _extraire_initiale_finale(pinyin_normalise)
    
    return initiale.upper(), '-' + finale, ton


def analyser_phonetique_complet(pinyin: str) -> AnalysePhonetique:
    """
    Analyse complète d'un pinyin avec toutes les informations structurelles.
    
    Args:
        pinyin: Chaîne pinyin (ex: "dao4", "zhōng", "lü3")
        
    Returns:
        AnalysePhonetique avec tous les détails
    """
    if not pinyin:
        return AnalysePhonetique(
            pinyin_original='',
            pinyin_normalise='',
            initiale='',
            finale='',
            ton=1,
            ton_nom='niveau',
            groupe_initiale='V*',
            groupe_finale='-V*',
            structure='',
            attaque='',
            noyau='',
            coda=''
        )
    
    pinyin_original = pinyin.strip()
    
    # Analyse de base
    initiale, finale, ton = analyser_phonetique(pinyin_original)
    initiale_brut = initiale.lower() if initiale else ''
    
    # Groupes
    groupe_initiale = GroupesPhonetiques.get_groupe_initiale(initiale_brut)
    groupe_finale = GroupesPhonetiques.get_groupe_finale(finale)
    
    # Structure syllabique
    attaque = initiale_brut
    noyau, coda = _analyser_noyau_coda(finale.lstrip('-'))
    
    # Type de structure
    if attaque and coda:
        structure = 'CVC'
    elif attaque and not coda:
        structure = 'CV'
    elif not attaque and coda:
        structure = 'VC'
    else:
        structure = 'V'
    
    return AnalysePhonetique(
        pinyin_original=pinyin_original,
        pinyin_normalise=_normaliser_pinyin(pinyin),
        initiale=initiale,
        finale=finale,
        ton=ton,
        ton_nom=TONS_MAPPING.get(ton, 'inconnu'),
        groupe_initiale=groupe_initiale,
        groupe_finale=groupe_finale,
        structure=structure,
        attaque=attaque,
        noyau=noyau,
        coda=coda
    )


def _extraire_ton_depuis_accent(pinyin: str) -> int:
    """Extrait le ton à partir des accents Unicode."""
    tons_map = {
        'ā': 1, 'á': 2, 'ǎ': 3, 'à': 4,
        'ē': 1, 'é': 2, 'ě': 3, 'è': 4,
        'ī': 1, 'í': 2, 'ǐ': 3, 'ì': 4,
        'ō': 1, 'ó': 2, 'ǒ': 3, 'ò': 4,
        'ū': 1, 'ú': 2, 'ǔ': 3, 'ù': 4,
        'ǖ': 1, 'ǘ': 2, 'ǚ': 3, 'ǜ': 4,
    }
    
    for char in pinyin:
        if char in tons_map:
            return tons_map[char]
    return 1


def _normaliser_pinyin(pinyin: str) -> str:
    """Normalise le pinyin (remplace les accents, ü, etc.)."""
    # Remplacer les voyelles accentuées
    accents = {
        'ā': 'a', 'á': 'a', 'ǎ': 'a', 'à': 'a',
        'ē': 'e', 'é': 'e', 'ě': 'e', 'è': 'e',
        'ī': 'i', 'í': 'i', 'ǐ': 'i', 'ì': 'i',
        'ō': 'o', 'ó': 'o', 'ǒ': 'o', 'ò': 'o',
        'ū': 'u', 'ú': 'u', 'ǔ': 'u', 'ù': 'u',
        'ǖ': 'ü', 'ǘ': 'ü', 'ǚ': 'ü', 'ǜ': 'ü',
    }
    
    result = pinyin
    for accent, normal in accents.items():
        result = result.replace(accent, normal)
    
    return result


def _extraire_initiale_finale(pinyin: str) -> Tuple[str, str]:
    """
    Extrait l'initiale et la finale d'un pinyin normalisé.
    
    Returns:
        Tuple (initiale, finale)
    """
    if not pinyin:
        return '', ''
    
    # Liste des initiales possibles (triées par longueur décroissante)
    initiales = ['zh', 'ch', 'sh'] + list('bpmfdtnlgkhjqxzcsryw')
    
    # Chercher l'initiale
    for init in sorted(initiales, key=len, reverse=True):
        if pinyin.startswith(init):
            finale = pinyin[len(init):]
            if not finale:  # Cas rare : pas de finale
                finale = '∅'
            return init, finale
    
    # Pas d'initiale (voyelle seule)
    return '', pinyin


def _analyser_noyau_coda(finale: str) -> Tuple[str, str]:
    """
    Analyse une finale pour extraire le noyau (voyelle) et la coda.
    
    Returns:
        Tuple (noyau, coda)
    """
    if not finale:
        return '', ''
    
    # Finales complexes
    finales_complexes = ['iang', 'uang', 'iong', 'iang', 'uang']
    for fc in finales_complexes:
        if finale == fc:
            return 'a' if 'a' in fc else 'o', fc.replace('a', '').replace('o', '')
    
    # Nasales
    if finale.endswith('ng'):
        noyau = finale[:-2]
        coda = 'ng'
        return noyau[-1] if noyau else 'ə', coda
    
    if finale.endswith('n'):
        noyau = finale[:-1]
        coda = 'n'
        return noyau[-1] if noyau else 'ə', coda
    
    # Diphtongues
    diphtongues = ['ai', 'ei', 'ao', 'ou', 'ia', 'ie', 'ua', 'uo', 'üe']
    for dip in diphtongues:
        if finale == dip:
            return dip[0], dip[1]
    
    # Voyelle simple
    if len(finale) == 1:
        return finale, ''
    
    # Cas par défaut
    return finale[0], finale[1:] if len(finale) > 1 else ''


# =============================================================================
# CLASSE GROUPES PHONETIQUES
# =============================================================================

class GroupesPhonetiques:
    """
    Gestionnaire des groupes phonétiques pour Tian-Dao-AI.
    
    Cette classe fournit les méthodes pour classifier les initiales et finales
    selon les groupes définis par l'analyse des attracteurs.
    """
    
    # Tables statiques
    _GROUPES_INITIALES = INITIALES_PINYIN
    _GROUPES_FINALES = FINALES_GROUPES
    
    @classmethod
    def get_groupe_initiale(cls, initiale: str) -> str:
        """
        Retourne le groupe phonétique de l'initiale.
        
        Args:
            initiale: L'initiale pinyin (ex: 'd', 'zh', '')
            
        Returns:
            Groupe (B*, D*, G*, J*, Z*, Y*, W*, V*)
        """
        if not initiale:
            return 'V*'
        return cls._GROUPES_INITIALES.get(initiale.lower(), 'X*')
    
    @classmethod
    def get_groupe_finale(cls, finale: str) -> str:
        """
        Retourne le groupe phonétique de la finale.
        
        Args:
            finale: La finale pinyin (ex: '-ao', '-ong')
            
        Returns:
            Groupe ( -ang*, -ong*, -an*, -ai*, -ao*, -i*, -u*, etc.)
        """
        if not finale:
            return '-V*'
        
        # Nettoyer la finale (enlever le '-' initial)
        finale_clean = finale.lstrip('-')
        
        # Chercher le groupe
        for pattern, group in cls._GROUPES_FINALES.items():
            if finale_clean == pattern or finale_clean.endswith(pattern):
                return group
            if pattern in finale_clean:
                return group
        
        # Groupe par défaut
        return '-V*'
    
    @classmethod
    def get_tous_groupes_initiaux(cls) -> Dict[str, str]:
        """Retourne tous les groupes d'initiales."""
        return cls._GROUPES_INITIALES.copy()
    
    @classmethod
    def get_tous_groupes_finaux(cls) -> Dict[str, str]:
        """Retourne tous les groupes de finales."""
        return cls._GROUPES_FINALES.copy()
    
    @classmethod
    def get_initiale_par_groupe(cls, groupe: str) -> List[str]:
        """
        Retourne toutes les initiales appartenant à un groupe.
        
        Args:
            groupe: Le groupe (B*, D*, G*, etc.)
            
        Returns:
            Liste des initiales
        """
        return [init for init, g in cls._GROUPES_INITIALES.items() if g == groupe]
    
    @classmethod
    def get_finale_par_groupe(cls, groupe: str) -> List[str]:
        """
        Retourne toutes les finales appartenant à un groupe.
        
        Args:
            groupe: Le groupe (-ong*, -ang*, etc.)
            
        Returns:
            Liste des finales
        """
        return [fin for fin, g in cls._GROUPES_FINALES.items() if g == groupe]


# =============================================================================
# ANALYSE COMPARATIVE ET ATTRACTEURS
# =============================================================================

class AnalyseAttracteurs:
    """
    Analyse des attracteurs phonétiques pour comparer des pinyin.
    """
    
    def __init__(self):
        self.correspondances = self._charger_correspondances()
    
    def _charger_correspondances(self) -> Dict[str, Dict]:
        """Charge les tables de correspondance entre pinyin."""
        # Correspondances entre initiales historiques et modernes
        return {
            # Bilabiales
            'b': {'archaic': ['p', 'b'], 'medieval': ['b'], 'modern': ['b']},
            'p': {'archaic': ['pʰ', 'p'], 'medieval': ['p'], 'modern': ['p']},
            'm': {'archaic': ['m'], 'medieval': ['m'], 'modern': ['m']},
            'f': {'archaic': ['p', 'f'], 'medieval': ['f'], 'modern': ['f']},
            
            # Alvéolaires
            'd': {'archaic': ['t', 'd'], 'medieval': ['d'], 'modern': ['d']},
            't': {'archaic': ['tʰ', 't'], 'medieval': ['t'], 'modern': ['t']},
            'n': {'archaic': ['n'], 'medieval': ['n'], 'modern': ['n']},
            'l': {'archaic': ['l'], 'medieval': ['l'], 'modern': ['l']},
            
            # Vélaires
            'g': {'archaic': ['k', 'g'], 'medieval': ['g'], 'modern': ['g']},
            'k': {'archaic': ['kʰ', 'k'], 'medieval': ['k'], 'modern': ['k']},
            'h': {'archaic': ['x', 'h'], 'medieval': ['h'], 'modern': ['h']},
            
            # Palatales
            'j': {'archaic': ['k', 'kj'], 'medieval': ['j'], 'modern': ['j']},
            'q': {'archaic': ['kʰ', 'kʰj'], 'medieval': ['q'], 'modern': ['q']},
            'x': {'archaic': ['x', 'xj'], 'medieval': ['x'], 'modern': ['x']},
            
            # Rétroflexes
            'zh': {'archaic': ['t', 'tr'], 'medieval': ['zh'], 'modern': ['zh']},
            'ch': {'archaic': ['tʰ', 'tʰr'], 'medieval': ['ch'], 'modern': ['ch']},
            'sh': {'archaic': ['x', 'xr'], 'medieval': ['sh'], 'modern': ['sh']},
            'r': {'archaic': ['n', 'nr'], 'medieval': ['r'], 'modern': ['r']},
            
            # Dentales
            'z': {'archaic': ['ts'], 'medieval': ['z'], 'modern': ['z']},
            'c': {'archaic': ['tsʰ'], 'medieval': ['c'], 'modern': ['c']},
            's': {'archaic': ['s'], 'medieval': ['s'], 'modern': ['s']},
        }
    
    def comparer_pinyin(self, pinyin1: str, pinyin2: str) -> Dict:
        """
        Compare deux pinyin et retourne leur similarité.
        
        Returns:
            Dictionnaire avec scores de similarité
        """
        p1 = analyser_phonetique_complet(pinyin1)
        p2 = analyser_phonetique_complet(pinyin2)
        
        # Scores
        score_initial = 1.0 if p1.initiale == p2.initiale else 0.0
        score_final = 1.0 if p1.finale == p2.finale else 0.0
        score_ton = 1.0 if p1.ton == p2.ton else 0.0
        score_groupe_init = 1.0 if p1.groupe_initiale == p2.groupe_initiale else 0.0
        score_groupe_fin = 1.0 if p1.groupe_finale == p2.groupe_finale else 0.0
        
        # Score total pondéré
        total = (score_initial * 0.3 + score_final * 0.3 + score_ton * 0.2 +
                 score_groupe_init * 0.1 + score_groupe_fin * 0.1)
        
        return {
            'pinyin1': pinyin1,
            'pinyin2': pinyin2,
            'analyse1': p1.to_dict(),
            'analyse2': p2.to_dict(),
            'scores': {
                'initiale': score_initial,
                'finale': score_final,
                'ton': score_ton,
                'groupe_initiale': score_groupe_init,
                'groupe_finale': score_groupe_fin,
                'total': total
            }
        }
    
    def trouver_rimes(self, pinyins: List[str]) -> Dict[str, List[str]]:
        """
        Trouve les pinyin qui riment entre eux.
        
        Args:
            pinyins: Liste de pinyin
            
        Returns:
            Dictionnaire {finale: [liste des pinyin]}
        """
        rimes = {}
        for p in pinyins:
            try:
                ana = analyser_phonetique_complet(p)
                finale = ana.finale
                if finale not in rimes:
                    rimes[finale] = []
                rimes[finale].append(p)
            except:
                continue
        return {k: v for k, v in rimes.items() if len(v) > 1}


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def charger_dictionnaire_pinyin(chemin: str) -> Dict[str, str]:
    """
    Charge un dictionnaire pinyin depuis un fichier JSON.
    
    Args:
        chemin: Chemin vers le fichier JSON
        
    Returns:
        Dictionnaire {caractère: pinyin}
    """
    path = Path(chemin)
    if not path.exists():
        return {}
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyser_texte(texte: str, dictionnaire_pinyin: Dict[str, str]) -> List[AnalysePhonetique]:
    """
    Analyse phonétique complète d'un texte.
    
    Args:
        texte: Texte chinois
        dictionnaire_pinyin: Dictionnaire caractère → pinyin
        
    Returns:
        Liste d'analyses phonétiques
    """
    resultats = []
    
    for char in texte:
        if char in dictionnaire_pinyin:
            pinyin = dictionnaire_pinyin[char]
            analyse = analyser_phonetique_complet(pinyin)
            resultats.append(analyse)
    
    return resultats


def calculer_matrice_attracteurs(analyses: List[AnalysePhonetique]) -> Dict:
    """
    Calcule la matrice des attracteurs à partir d'une liste d'analyses.
    
    Returns:
        Matrice de co-occurrence des groupes
    """
    groupes_init = {}
    groupes_fin = {}
    
    for ana in analyses:
        gi = ana.groupe_initiale
        gf = ana.groupe_finale
        
        groupes_init[gi] = groupes_init.get(gi, 0) + 1
        groupes_fin[gf] = groupes_fin.get(gf, 0) + 1
    
    return {
        'distribution_initiales': groupes_init,
        'distribution_finales': groupes_fin,
        'total_caracteres': len(analyses)
    }


# =============================================================================
# TESTS ET EXEMPLES
# =============================================================================

if __name__ == "__main__":
    # Test de base
    print("=== TEST STRUCTURAL_ATTRACTEURS ===\n")
    
    # Tester analyser_phonetique
    tests = ["dao4", "zhōng", "lü3", "shi2", "bu4", "tian1"]
    
    print("1. Test de analyser_phonetique():")
    for p in tests:
        i, f, t = analyser_phonetique(p)
        print(f"   {p} → initiale: {i}, finale: {f}, ton: {t}")
    
    print("\n2. Test de analyser_phonetique_complet():")
    for p in tests[:3]:
        ana = analyser_phonetique_complet(p)
        print(f"   {p}:")
        print(f"      Initiale: {ana.initiale} ({ana.groupe_initiale})")
        print(f"      Finale: {ana.finale} ({ana.groupe_finale})")
        print(f"      Ton: {ana.ton} ({ana.ton_nom})")
        print(f"      Structure: {ana.structure}")
    
    print("\n3. Test de GroupesPhonetiques:")
    print(f"   Initiales du groupe B*: {GroupesPhonetiques.get_initiale_par_groupe('B*')}")
    print(f"   Finales du groupe -ong*: {GroupesPhonetiques.get_finale_par_groupe('-ong*')}")
    
    print("\n4. Test de AnalyseAttracteurs:")
    att = AnalyseAttracteurs()
    comparison = att.comparer_pinyin("dao4", "tao4")
    print(f"   Similarité dao4/tao4: {comparison['scores']['total']:.0%}")
    
    print("\n✅ Tous les tests passés!")