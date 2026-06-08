# ChineseHistoricalPhonology

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**汉语历史音韵学计算系统：历时与共时音韵分析框架**

---

## 📖 项目简介

**ChineseHistoricalPhonology** 是一个面向汉语音韵学研究的自动化分析系统，融合了：

- **历史音韵学**：文本时期自动检测（上古、中古、早期官话、现代）与音韵构拟
- **现代音韵学**：汉语拼音结构分析、音组分类（B*、D*、G*、-ong*、-ang*等）
- **音韵吸引子**：相似度计算、押韵检测、比较分析

本项目秉承**天道AI**理念，将汉语语言学与计算分析相结合。

---

## ✨ 核心功能

### 🔍 历史音韵学

| 功能 | 说明 |
|------|------|
| 时期检测 | 自动识别文本的历史时期（上古、中古、早期官话、现代） |
| 音韵构拟 | 基于白一平-沙加尔系统的上古音构拟 |
| Merkabah映射 | 为每个字符分配象征性取向 |

### 🗣️ 现代音韵学

| 功能 | 说明 |
|------|------|
| 拼音分析 | 声母/韵母/声调提取，Unicode归一化 |
| 音组分类 | B*、D*、G*、J*、Z*、Y*、W*、V* 声母分组 |
| 音节结构 | CVC、CV、VC、V 结构识别 |
| 音核/韵尾分析 | 声母、韵核、韵尾提取 |

### 🎯 音韵吸引子

| 功能 | 说明 |
|------|------|
| 拼音比较 | 两个发音之间的相似度计算 |
| 押韵检测 | 识别相互押韵的拼音 |
| 吸引子矩阵 | 音韵共现关系计算 |

---

## 🏗️ 系统架构

```
ChineseHistoricalPhonology/
├── bin/                          # 可执行脚本
│   ├── tian                      # 主界面
│   ├── tian-analyze              # 文件分析
│   ├── tian-test                 # 测试
│   ├── tian-clean                # 清理
│   ├── tian-stats                # 统计
│   ├── tian-check                # 安装检查
│   └── tian-help                 # 帮助
├── src/
│   ├── historical_merkabah/      # 历史音韵学核心
│   │   ├── core/
│   │   │   ├── historical_phonology_adapter.py   # 主适配器
│   │   │   ├── temporal_router.py                # 时空调度器
│   │   │   └── period_detectors.py               # 时期检测器
│   │   └── databases/                            # 音韵数据库
│   ├── analysis/
│   │   └── structural_attracteurs.py             # 结构分析
│   └── core/
│       └── phonology_integration.py              # 整合层
├── data/                         # 数据
│   ├── corpora/                  # 待分析文本
│   ├── pinyin/                   # 拼音词典
│   └── historical/               # 历史数据库
├── config/                       # 配置文件
├── results/                      # 分析结果
├── logs/                         # 运行日志
├── main.py                       # 入口程序
└── quick_test.py                 # 快速测试
```

---

## 🚀 安装与使用

### 环境要求

```bash
# 需要 Python 3.11 或更高版本
python3 --version

# 克隆仓库
git clone https://github.com/yourusername/ChineseHistoricalPhonology.git
cd ChineseHistoricalPhonology
```

### 快速安装

```bash
# 赋予脚本执行权限
chmod +x bin/*

# 运行测试套件
./bin/tian-test

# 检查安装
./bin/tian-check
```

### 虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install pyyaml
```

---

## 📖 使用指南

### 命令行界面

```bash
# 分析文件
./bin/tian-analyze data/corpora/test.txt

# 运行所有测试
./bin/tian-test

# 清理临时文件
./bin/tian-clean

# 查看统计信息
./bin/tian-stats

# 检查安装
./bin/tian-check

# 显示帮助
./bin/tian-help
```

### 交互式菜单

```bash
# 启动交互式界面
./bin/tian
```

### Python API

```python
import sys
sys.path.insert(0, 'src')

from historical_merkabah.core import HistoricalPhonologyAdapter
from analysis.structural_attracteurs import analyser_phonetique_complet

# 初始化适配器
adapter = HistoricalPhonologyAdapter()

# 检测时期
text = "道可道，非常道。"
scores = adapter.detect_period(text)
print(f"检测到的时期: {scores.best_period}")

# 分析单个字符
result = adapter.analyze_character("道", "dao4")
print(f"构拟读音: {result.historical.reconstruction}")
print(f"Merkabah: {result.historical.merkabah}")

# 现代音韵分析
analysis = analyser_phonetique_complet("zhōng")
print(f"声母: {analysis.initiale} ({analysis.groupe_initiale})")
print(f"韵母: {analysis.finale} ({analysis.groupe_finale})")
print(f"音节结构: {analysis.structure}")
```

### 分析文本文件

```bash
# 创建测试文件
cat > data/corpora/example.txt << 'EOF'
道可道，非常道。
名可名，非常名。
无名天地之始，有名万物之母。
EOF

# 执行分析
./bin/tian-analyze data/corpora/example.txt
```

---

## 📊 输出示例

```
📖 分析文件: data/corpora/example.txt

📝 文本（33字符）:
道可道，非常道。
名可名，非常名。
无名天地之始，有名万物之母。

📅 检测到的时期: 中古
   得分详情:
     上古: 5.0%
     中古: 70.0%
     早期官话: 20.0%
     现代: 5.0%

📊 结果:
   已分析字符: 22/24

📜 历史构拟:
   道 (dao4): lˤuʔ (Merkabah: A1)
   可 (ke3): kʰaʔ (Merkabah: A1)
   非 (fei1): pəj (Merkabah: A1)
   常 (chang2): djaŋ (Merkabah: A1)
```

---

## 📁 数据结构

### 拼音词典 (`data/pinyin/common.json`)

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

### 配置文件 (`config/phonology_config.yaml`)

```yaml
phonology:
  historical:
    enabled: true
    weights:
      lexical: 0.5      # 词汇权重
      character: 0.3    # 用字权重
      syntax: 0.2       # 句法权重
  modern:
    enabled: true
  output:
    format: json
    include_confidence: true
```

---

## 🧪 测试

```bash
# 运行所有测试
./bin/tian-test

# 快速测试
python3 quick_test.py

# 吸引子演示
python3 demo_attracteurs.py
```

---

## 📚 音组分类

### 声母组

| 组别 | 声母 | 发音部位 |
|------|------|----------|
| B* | b、p、m、f | 双唇音/唇齿音 |
| D* | d、t、n、l | 齿龈音 |
| G* | g、k、h | 软腭音 |
| J* | j、q、x | 腭音 |
| Z* | zh、ch、sh、r、z、c、s | 卷舌音/齿音 |
| Y* | y | 腭近音 |
| W* | w | 唇近音 |
| V* | （零声母） | 元音开头 |

### 韵母组

| 组别 | 韵母 | 音韵特征 |
|------|------|----------|
| -ong* | ong、iong | 软腭鼻音韵尾 |
| -ang* | ang、iang、uang | 开鼻音韵尾 |
| -an* | an、ian、uan、en、in | 齿龈鼻音韵尾 |
| -ai* | ai、ei、uai、ui | 前响复元音 |
| -ao* | ao、iao、ou、iu | 后响复元音 |
| -i* | i | 高前元音 |
| -u* | u | 高后元音 |

---

## 🔧 开发指南

### 添加新字符

编辑 `src/historical_merkabah/core/temporal_router.py`：

```python
# 上古音数据库
'新': {'reconstruction': 'si[n]', 'initial': 's', 'final': 'i[n]', 'tone': '平'},

# 现代音数据库
'新': {'pinyin': 'xin1', 'initial': 'x', 'final': 'in', 'tone': 1},
```

### 扩展拼音词典

```bash
# 编辑 JSON 文件
nano data/pinyin/common.json
```

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- 白一平（William Baxter）和沙加尔（Laurent Sagart）的上古汉语构拟系统
- CEDICT 项目贡献者提供的现代拼音数据
- Python 及开源社区

---

## 📧 联系方式

如有问题、建议或贡献意向，请在 GitHub 上提交 Issue。

---

## 🌟 星标历史

如果您觉得本项目有用，请在 GitHub 上点亮星标 ⭐！

---

**用 ❤️ 为汉语语言学和计算分析而建**
