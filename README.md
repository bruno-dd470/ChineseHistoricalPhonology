# ChineseHistoricalPhonology

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/Code%20style-black-000000.svg)](https://github.com/psf/black)

**A comprehensive system for historical and structural Chinese phonology analysis**

---

## 📖 Overview

**ChineseHistoricalPhonology** is an automated analysis system for Chinese phonology that combines:

- **Historical Phonology**: Period detection (archaic, medieval, early Mandarin, modern) and phonetic reconstruction
- **Modern Phonology**: Pinyin structural analysis, phonetic groups (B*, D*, G*, -ong*, -ang*, etc.)
- **Phonetic Attractors**: Comparative analysis, rhyme detection, similarity matrices

The project follows a **Tian-Dao-AI** approach, blending Sinitic linguistics with computational analysis.

---

## ✨ Features

### 🔍 Historical Phonology

| Feature | Description |
|---------|-------------|
| Period Detection | Automatic identification of historical period (archaic, medieval, early Mandarin, modern) |
| Reconstruction | Restitution of ancient pronunciations (Baxter-Sagart system, custom reconstructions) |
| Merkabah Mapping | Attribution of a symbolic orientation for each character |

### 🗣️ Modern Phonology

| Feature | Description |
|---------|-------------|
| Pinyin Analysis | Initial/final/tone extraction, Unicode normalization |
| Phonetic Groups | Classification into B*, D*, G*, J*, Z*, Y*, W*, V* |
| Syllable Structure | CVC, CV, VC, V identification |
| Nucleus/Coda Analysis | Onset, nucleus, and coda extraction |

### 🎯 Attractors

| Feature | Description |
|---------|-------------|
| Pinyin Comparison | Similarity calculation between two pronunciations |
| Rhyme Detection | Identification of rhyming pinyin |
| Attractor Matrices | Calculation of phonetic co-occurrences |

---

## 🏗️ Architecture

```
ChineseHistoricalPhonology/
├── bin/                          # Executable bash scripts
│   ├── tian                      # Main interface
│   ├── tian-analyze              # File analysis
│   ├── tian-test                 # Tests
│   ├── tian-clean                # Cleanup
│   ├── tian-stats                # Statistics
│   ├── tian-check                # Installation check
│   └── tian-help                 # Help
├── src/
│   ├── historical_merkabah/      # Historical phonology core
│   │   ├── core/
│   │   │   ├── historical_phonology_adapter.py   # Main adapter
│   │   │   ├── temporal_router.py                # Temporal router
│   │   │   └── period_detectors.py               # Period detectors
│   │   └── databases/                            # Phonological databases
│   ├── analysis/
│   │   └── structural_attracteurs.py             # Structural analysis
│   └── core/
│       └── phonology_integration.py              # Integration layer
├── data/                         # Data
│   ├── corpora/                  # Texts to analyze
│   ├── pinyin/                   # Pinyin dictionaries
│   └── historical/               # Historical databases
├── config/                       # Configuration
├── results/                      # Analysis results
├── logs/                         # Execution logs
├── main.py                       # Entry point
├── quick_test.py                 # Quick tests
└── demo_attracteurs.py           # Feature demonstration
```

---

## 🚀 Installation

### Prerequisites

```bash
# Python 3.11 or higher required
python3 --version

# Clone the repository
git clone https://github.com/yourusername/ChineseHistoricalPhonology.git
cd ChineseHistoricalPhonology
```

### Quick Install

```bash
# Make scripts executable
chmod +x bin/*

# Run the test suite
./bin/tian-test

# Check installation
./bin/tian-check
```

### Virtual Environment (recommended)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pyyaml
```

---

## 📖 Usage

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
# Launch the interactive interface
./bin/tian
```

### Python API

```python
import sys
sys.path.insert(0, 'src')

from historical_merkabah.core import HistoricalPhonologyAdapter
from analysis.structural_attracteurs import analyser_phonetique_complet

# Initialize the adapter
adapter = HistoricalPhonologyAdapter()

# Detect period
text = "道可道，非常道。"
scores = adapter.detect_period(text)
print(f"Detected period: {scores.best_period}")

# Analyze a character
result = adapter.analyze_character("道", "dao4")
print(f"Reconstruction: {result.historical.reconstruction}")
print(f"Merkabah: {result.historical.merkabah}")

# Modern phonetic analysis
analysis = analyser_phonetique_complet("zhōng")
print(f"Initial: {analysis.initiale} ({analysis.groupe_initiale})")
print(f"Final: {analysis.finale} ({analysis.groupe_finale})")
print(f"Syllable structure: {analysis.structure}")
```

### Analyzing a Text File

```bash
# Create a test file
cat > data/corpora/example.txt << 'EOF'
道可道，非常道。
名可名，非常名。
EOF

# Analyze it
./bin/tian-analyze data/corpora/example.txt
```

---

## 📊 Example Output

```
📖 Analyzing: data/corpora/example.txt

📝 Text (33 characters):
道可道，非常道。
名可名，非常名。

📅 Detected period: medieval
   Scores:
     archaic: 5.0%
     medieval: 70.0%
     early_mandarin: 20.0%
     modern: 5.0%

📊 Results:
   Characters analyzed: 22/24

📜 Historical reconstructions:
   道 (dao4): lˤuʔ (Merkabah: A1)
   可 (ke3): kʰaʔ (Merkabah: A1)
   非 (fei1): pəj (Merkabah: A1)
   常 (chang2): djaŋ (Merkabah: A1)
```

---

## 📁 Data Structure

### Pinyin Dictionary (`data/pinyin/common.json`)

```json
{
  "道": "dao4",
  "可": "ke3",
  "非": "fei1",
  "常": "chang2",
  "天": "tian1",
  "地": "di4"
}
```

### Configuration (`config/phonology_config.yaml`)

```yaml
phonology:
  historical:
    enabled: true
    weights:
      lexical: 0.5
      character: 0.3
      syntax: 0.2
  modern:
    enabled: true
  output:
    format: json
    include_confidence: true
```

---

## 🧪 Testing

```bash
# Run all tests
./bin/tian-test

# Quick test
python3 quick_test.py

# Demo of attractors
python3 demo_attracteurs.py
```

---

## 📚 Phonetic Groups

### Initial Groups

| Group | Sounds | Description |
|-------|--------|-------------|
| B* | b, p, m, f | Bilabials / Labiodentals |
| D* | d, t, n, l | Alveolars |
| G* | g, k, h | Velars |
| J* | j, q, x | Palatals |
| Z* | zh, ch, sh, r, z, c, s | Retroflexes / Dentals |
| Y* | y | Palatal approximant |
| W* | w | Labial approximant |
| V* | (none) | Vowel-initial |

### Final Groups

| Group | Sounds | Description |
|-------|--------|-------------|
| -ong* | ong, iong | Velar nasal |
| -ang* | ang, iang, uang | Open nasal |
| -an* | an, ian, uan | Alveolar nasal |
| -ai* | ai, ei, uai, ui | Front diphthongs |
| -ao* | ao, iao, ou, iu | Back diphthongs |
| -i* | i, i | High front vowel |
| -u* | u | High back vowel |

---

## 🔧 Development

### Adding New Characters

Edit `src/historical_merkabah/core/temporal_router.py`:

```python
# Archaic database
'新': {'reconstruction': 'si[n]', 'initial': 's', 'final': 'i[n]', 'tone': '平'},

# Modern database
'新': {'pinyin': 'xin1', 'initial': 'x', 'final': 'in', 'tone': 1},
```

### Extending Pinyin Dictionary

```bash
# Edit the JSON file
nano data/pinyin/common.json
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Baxter-Sagart reconstruction system for Old Chinese
- CEDICT for modern pinyin data
- The Tian-Dao-AI philosophy for inspiration

---

## 📧 Contact

For questions, suggestions, or contributions, please open an issue on GitHub.

---

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐ on GitHub!

---

**Built with ❤️ for Chinese linguistics and computational analysis**
```

## 📝 **Fichiers supplémentaires pour GitHub**

### `LICENSE` (MIT)

```markdown
MIT License

Copyright (c) 2024 ChineseHistoricalPhonology

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# Project specific
logs/
results/*.json
results/*.png
*.log
.DS_Store

# Environment
merkahah_env/
venv/

# Temporary files
*.tmp
*.bak
*.orig
```

### `requirements.txt`

```txt
pyyaml>=6.0
```

### `setup.py` (optionnel)

```python
from setuptools import setup, find_packages

setup(
    name="chinese-historical-phonology",
    version="1.0.0",
    description="Comprehensive system for historical and structural Chinese phonology analysis",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/ChineseHistoricalPhonology",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "pyyaml>=6.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Linguistics",
    ],
)
