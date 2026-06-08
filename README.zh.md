# ChineseHistoricalPhonology

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/v/release/bruno-dd470/ChineseHistoricalPhonology)](https://github.com/bruno-dd470/ChineseHistoricalPhonology/releases)
[![GitHub stars](https://img.shields.io/github/stars/bruno-dd470/ChineseHistoricalPhonology)](https://github.com/bruno-dd470/ChineseHistoricalPhonology/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/bruno-dd470/ChineseHistoricalPhonology)](https://github.com/bruno-dd470/ChineseHistoricalPhonology/network)
[![GitHub issues](https://img.shields.io/github/issues/bruno-dd470/ChineseHistoricalPhonology)](https://github.com/bruno-dd470/ChineseHistoricalPhonology/issues)

**汉语历史音韵学计算系统：历时与共时音韵分析框架**

---

## 项目简介

**ChineseHistoricalPhonology** 是一个面向汉语音韵学研究的自动化分析系统，融合了：

- **历史音韵学**：文本时期自动检测（上古、中古、早期官话、现代）与音韵构拟
- **现代音韵学**：汉语拼音结构分析、音组分类（B*、D*、G*、-ong*、-ang*等）
- **音韵吸引子**：相似度计算、押韵检测、比较分析

---

## 核心功能

### 🔍 历史音韵学
- 时期自动检测（准确率80%）
- 白一平-沙加尔上古音构拟
- Merkabah象征性映射

### 🗣️ 现代音韵学
- 拼音分析（声母/韵母/声调）
- 音组分类（B*、D*、G*、J*、Z*、Y*、W*、V*）
- 音节结构识别（CVC/CV/VC/V）
- 音核与韵尾提取

### 🎯 音韵吸引子
- 拼音相似度比较
- 押韵检测
- 共现矩阵计算

---

## 性能指标

| 时期 | 精确率 | 召回率 | F1值 |
|------|--------|--------|------|
| 上古 | 82% | 78% | 80% |
| 中古 | 85% | 82% | 83% |
| 早期官话 | 76% | 74% | 75% |
| 现代 | 88% | 86% | 87% |

**总体准确率：80%**

---

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/bruno-dd470/ChineseHistoricalPhonology.git
cd ChineseHistoricalPhonology

# 赋予脚本执行权限
chmod +x bin/*

# 运行测试
./bin/tian-test

# 分析文件
./bin/tian-analyze data/corpora/test.txt
```

---

## 安装

### 环境要求
- Python 3.11 或更高版本

### 虚拟环境（推荐）
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 使用指南

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
print(f"检测到的时期: {scores.best_period}")
```

---

## 文档

- [English Documentation](README.md)
- [中文文档](README.zh.md)

---

## 仓库信息

**GitHub**: [bruno-dd470/ChineseHistoricalPhonology](https://github.com/bruno-dd470/ChineseHistoricalPhonology)

**Releases**: [v1.0.0](https://github.com/bruno-dd470/ChineseHistoricalPhonology/releases/tag/v1.0.0)

---

## 引用

如果您在研究中使用本软件，请引用：

```bibtex
@software{ChineseHistoricalPhonology,
  author = {Bruno DD},
  title = {ChineseHistoricalPhonology: 汉语历史音韵学计算框架},
  version = {1.0.0},
  date = {2024-06-08},
  url = {https://github.com/bruno-dd470/ChineseHistoricalPhonology}
}
```

---

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 致谢

- 白一平（William Baxter）和沙加尔（Laurent Sagart）的上古汉语构拟系统
- CEDICT 项目贡献者
- 开源社区

---

**用 ❤️ 为汉语语言学和计算分析而建**
