# ChineseHistoricalPhonology

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/v/release/bruno-dd470/ChineseHistoricalPhonology)](https://github.com/bruno-dd470/ChineseHistoricalPhonology/releases)
[![GitHub stars](https://img.shields.io/github/stars/bruno-dd470/ChineseHistoricalPhonology)](https://github.com/bruno-dd470/ChineseHistoricalPhonology/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/bruno-dd470/ChineseHistoricalPhonology)](https://github.com/bruno-dd470/ChineseHistoricalPhonology/network)
[![GitHub issues](https://img.shields.io/github/issues/bruno-dd470/ChineseHistoricalPhonology)](https://github.com/bruno-dd470/ChineseHistoricalPhonology/issues)
[![Code style: black](https://img.shields.io/badge/Code%20style-black-000000.svg)](https://github.com/psf/black)

**A comprehensive system for historical and structural Chinese phonology analysis**

---

## Overview

**ChineseHistoricalPhonology** is an automated analysis system for Chinese phonology that combines:

- **Historical Phonology**: Period detection (archaic, medieval, early Mandarin, modern) and phonetic reconstruction
- **Modern Phonology**: Pinyin structural analysis, phonetic groups (B*, D*, G*, -ong*, -ang*, etc.)
- **Phonetic Attractors**: Comparative analysis, rhyme detection, similarity matrices

---

## Features

### 🔍 Historical Phonology
- Automatic period detection (80% accuracy)
- Baxter-Sagart reconstruction system
- Merkabah symbolic mapping

### 🗣️ Modern Phonology
- Pinyin analysis (initial/final/tone)
- Phonetic group classification (B*, D*, G*, J*, Z*, Y*, W*, V*)
- Syllable structure (CVC/CV/VC/V)
- Nucleus and coda extraction

### 🎯 Attractors
- Pinyin similarity comparison
- Rhyme detection
- Co-occurrence matrices

---

## Performance

| Period | Precision | Recall | F1-Score |
|--------|-----------|--------|----------|
| Archaic | 82% | 78% | 80% |
| Medieval | 85% | 82% | 83% |
| Early Mandarin | 76% | 74% | 75% |
| Modern | 88% | 86% | 87% |

**Overall Accuracy: 80%**

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/bruno-dd470/ChineseHistoricalPhonology.git
cd ChineseHistoricalPhonology

# Make scripts executable
chmod +x bin/*

# Run tests
./bin/tian-test

# Analyze a file
./bin/tian-analyze data/corpora/test.txt
```

---

## Installation

### Prerequisites
- Python 3.11 or higher

### Virtual Environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

### Command Line Interface
```bash
# Analyze a file
./bin/tian-analyze data/corpora/test.txt

# Run all tests
./bin/tian-test

# Clean temporary files
./bin/tian-clean

# View statistics
./bin/tian-stats

# Check installation
./bin/tian-check

# Display help
./bin/tian-help
```

### Interactive Menu
```bash
./bin/tian
```

### Python API
```python
import sys
sys.path.insert(0, 'src')

from historical_merkabah.core import HistoricalPhonologyAdapter

adapter = HistoricalPhonologyAdapter()
text = "道可道，非常道。"
scores = adapter.detect_period(text)
print(f"Detected period: {scores.best_period}")
```

---

## Documentation

- [English Documentation](README.md)
- [中文文档](README.zh.md)

---

## Repository

**GitHub**: [bruno-dd470/ChineseHistoricalPhonology](https://github.com/bruno-dd470/ChineseHistoricalPhonology)

**Releases**: [v1.0.0](https://github.com/bruno-dd470/ChineseHistoricalPhonology/releases/tag/v1.0.0)

---

## Citation

If you use this software in your research, please cite:

```bibtex
@software{ChineseHistoricalPhonology,
  author = {Bruno DD},
  title = {ChineseHistoricalPhonology: A Computational Framework for Historical and Structural Chinese Phonology},
  version = {1.0.0},
  date = {2024-06-08},
  url = {https://github.com/bruno-dd470/ChineseHistoricalPhonology}
}
```

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- William Baxter and Laurent Sagart for Old Chinese reconstructions
- CEDICT project contributors
- Open source community

---

**Built with ❤️ for Chinese linguistics and computational analysis**
