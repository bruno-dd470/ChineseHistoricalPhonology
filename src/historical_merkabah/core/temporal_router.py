#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, Any

class TemporalRouter:
    def __init__(self):
        self.databases = self._load_minimal_databases()

    def _load_minimal_databases(self):
        archaic = {
            '道': {'reconstruction': 'lˤuʔ', 'initial': 'lˤ', 'final': 'uʔ', 'tone': '上'},
            '德': {'reconstruction': 'tˤək', 'initial': 'tˤ', 'final': 'ək', 'tone': '入'},
            '天': {'reconstruction': 'l̥ˤi[n]', 'initial': 'l̥ˤ', 'final': 'i[n]', 'tone': '平'},
            '地': {'reconstruction': 'lˤej-s', 'initial': 'lˤ', 'final': 'ej-s', 'tone': '去'},
            '人': {'reconstruction': 'ni[ŋ]', 'initial': 'n', 'final': 'i[ŋ]', 'tone': '平'},
            '之': {'reconstruction': 'tə', 'initial': 't', 'final': 'ə', 'tone': '平'},
            '不': {'reconstruction': 'pə', 'initial': 'p', 'final': 'ə', 'tone': '入'},
            '以': {'reconstruction': 'ləʔ', 'initial': 'l', 'final': 'əʔ', 'tone': '上'},
            '可': {'reconstruction': 'kʰaʔ', 'initial': 'kʰ', 'final': 'aʔ', 'tone': '上'},
            '非': {'reconstruction': 'pəj', 'initial': 'p', 'final': 'əj', 'tone': '平'},
            '常': {'reconstruction': 'djaŋ', 'initial': 'dj', 'final': 'aŋ', 'tone': '平'},            
            '名': {'reconstruction': 'C.meŋ', 'initial': 'm', 'final': 'eŋ', 'tone': '平'},
            '始': {'reconstruction': 'l̥əʔ', 'initial': 'l̥', 'final': 'əʔ', 'tone': '上'},
            '有': {'reconstruction': 'ɢʷəʔ', 'initial': 'ɢʷ', 'final': 'əʔ', 'tone': '上'},
            '物': {'reconstruction': 'C.mut', 'initial': 'm', 'final': 'ut', 'tone': '入'},
            '母': {'reconstruction': 'məʔ', 'initial': 'm', 'final': 'əʔ', 'tone': '上'},
        }
        modern = {
            '道': {'pinyin': 'dao4', 'initial': 'd', 'final': 'ao', 'tone': 4},
            '德': {'pinyin': 'de2', 'initial': 'd', 'final': 'e', 'tone': 2},
            '天': {'pinyin': 'tian1', 'initial': 't', 'final': 'ian', 'tone': 1},
            '地': {'pinyin': 'di4', 'initial': 'd', 'final': 'i', 'tone': 4},
            '人': {'pinyin': 'ren2', 'initial': 'r', 'final': 'en', 'tone': 2},
            '之': {'pinyin': 'zhi1', 'initial': 'zh', 'final': 'i', 'tone': 1},
            '不': {'pinyin': 'bu4', 'initial': 'b', 'final': 'u', 'tone': 4},
            '以': {'pinyin': 'yi3', 'initial': 'y', 'final': 'i', 'tone': 3},
            '可': {'pinyin': 'ke3', 'initial': 'k', 'final': 'e', 'tone': 3},
            '非': {'pinyin': 'fei1', 'initial': 'f', 'final': 'ei', 'tone': 1},
            '常': {'pinyin': 'chang2', 'initial': 'ch', 'final': 'ang', 'tone': 2},           
            '名': {'pinyin': 'ming2', 'initial': 'm', 'final': 'ing', 'tone': 2},
            '始': {'pinyin': 'shi3', 'initial': 'sh', 'final': 'i', 'tone': 3},
            '有': {'pinyin': 'you3', 'initial': 'y', 'final': 'ou', 'tone': 3},
            '物': {'pinyin': 'wu4', 'initial': 'w', 'final': 'u', 'tone': 4},
            '母': {'pinyin': 'mu3', 'initial': 'm', 'final': 'u', 'tone': 3},
        }
        return {'archaic': archaic, 'modern': modern}

    def get_analysis(self, character: str, period: str = 'modern') -> Dict[str, Any]:
        db = self.databases.get(period, self.databases['modern'])
        if character in db:
            data = db[character].copy()
        else:
            if period == 'archaic':
                data = {'reconstruction': f'*{character}*', 'initial': '?', 'final': '?', 'tone': '平'}
            else:
                data = {'pinyin': f'{character}?', 'initial': '?', 'final': '?', 'tone': 1}
        data['character'] = character
        data['period'] = period
        data['merkabah'] = 'A1'  # valeur par défaut
        data['confidence'] = 0.8 if character in db else 0.0
        return data
# Ajout des caractères manquants
        # Dans archaic (vers ligne 15, avant la fermeture de archaic_data)
        '名': {'reconstruction': 'C.meŋ', 'initial': 'm', 'final': 'eŋ', 'tone': '平'},
        '始': {'reconstruction': 'l̥əʔ', 'initial': 'l̥', 'final': 'əʔ', 'tone': '上'},
        '有': {'reconstruction': 'ɢʷəʔ', 'initial': 'ɢʷ', 'final': 'əʔ', 'tone': '上'},
        '物': {'reconstruction': 'C.mut', 'initial': 'm', 'final': 'ut', 'tone': '入'},
        '母': {'reconstruction': 'məʔ', 'initial': 'm', 'final': 'əʔ', 'tone': '上'},
        
        # Dans modern (vers ligne 35)
        '名': {'pinyin': 'ming2', 'initial': 'm', 'final': 'ing', 'tone': 2},
        '始': {'pinyin': 'shi3', 'initial': 'sh', 'final': 'i', 'tone': 3},
        '有': {'pinyin': 'you3', 'initial': 'y', 'final': 'ou', 'tone': 3},
        '物': {'pinyin': 'wu4', 'initial': 'w', 'final': 'u', 'tone': 4},
        '母': {'pinyin': 'mu3', 'initial': 'm', 'final': 'u', 'tone': 3},
