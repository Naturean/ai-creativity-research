# 毕业设计：AI辅助下的创造性表现

研究 AI 辅助对发散思维创造性表现的影响，聚焦于个体自愿使用 AI 的**时机与频率特征**及其与创造绩效的关系。

## 研究概要

### 研究问题

| 问题 | 描述                                                                                        |
| ---- | ------------------------------------------------------------------------------------------- |
| RQ1  | AI 调用行为的分布特征（调用次数、首次调用时间、调用间隔），能否通过聚类识别不同的调用模式？ |
| RQ2  | 调用行为特征是否与发散思维绩效（流畅性、原创性）相关？不同调用模式组的绩效是否存在差异？    |
| RQ3  | AI 调用前后的认知加工特征有何差异？调用前的行为特征和认知状态能否预测 AI 调用的有效性？     |

### 实验设计

- **任务**：Alternate Uses Task（AUT），4 个正式试次 × 5 分钟，加 1 个练习试次（3 分钟，物品"肥皂"）
- **物品**：16 个日常物品分入 4 组，按语义丰富度平衡，每组 2 个高丰富度 + 2 个低丰富度，按低-高-低-高顺序呈现
- **AI 交互**：工具型（非对话式）——被试点击按钮获取 AI 生成的 AUT 启发提示，不限调用次数，仅展示最新一次 AI 提示
- **AI 模型**：Doubao-1.5-pro-32k（max_tokens=300, temperature=1.3）
- **平台**：PsychoPy 2025.1.1（实验程序）+ Credamo 见数（被试招募与问卷）+ 腾讯云 SCF（AI API 代理）
- **样本**：有效被试约 500 名，通过 Credamo 见数平台招募

### 核心指标

- **流畅性（Fluency）**：每个被试在 4 个试次中的回答总数
- **原创性（Originality）**：通过 Ocsai（Organisciak et al., 2023）LLM 自动评分，中文模式，r=0.81（与人类评分者）
- **AI 调用特征**：调用次数、首次调用时间、调用前想法数、调用间隔、调用间隔标准差（作为"调用规律性"代理）
- 灵活性和精致性暂未计算（缺乏成熟的自动化方案）

## 环境配置

### 复现环境

```bash
# 从 environment.yml 创建 conda 环境
conda env create -f environment.yml

# 激活环境
conda activate graduation-design
```

`environment.yml` 位于仓库根目录，固定了主要依赖版本。

### 首次运行前必须做的事

1. **准备原始数据**。登录见数（Credamo）平台，点击左上角“下载数据”，选择“文本”变量类型、CSV格式，下载问卷数据后放入 `data/raw/questionnaire/` 目录。
2. **配置语义模型路径**。编辑 `modules/semantic_toolbox/corpustrain/model_path.py`，将其中的路径指向本机的 FastText 中文词向量文件（`.bin` 格式）。官方下载指南：[Word vectors for 157 languages - fastText](https://fasttext.cc/docs/en/crawl-vectors.html)。
3. **生成词表**。运行 `python modules/dat/get_words.py`，从原始问卷数据中提取 DAT 词典（`words.txt`），供后续评分使用。
4. **确认 conda 环境名为 `graduation-design`**。VS Code 的 `.vscode/settings.json` 已绑定此环境名。

## 数据分析流水线

分析按以下顺序执行，每个步骤依赖前一步的输出产物。所有 notebook 需从其所在目录运行（内部使用相对路径 `../../data/...`）。

```plaintext
原始数据 → 生成词表 → 预处理 → 加载数据 → 计算指标 → 报告/可视化
```

### 阶段〇：生成词表

| 脚本                       | 功能                         | 输入                      | 输出                    |
| -------------------------- | ---------------------------- | ------------------------- | ----------------------- |
| `modules/dat/get_words.py` | 从原始问卷数据提取 DAT 词典  | `data/raw/questionnaire/` | `modules/dat/words.txt` |

必须在预处理之前运行，因为 `dat.py` 导入时加载 `words.txt` 作为词表白名单。

### 阶段一：预处理

| Notebook                           | 功能                                         | 输入        | 输出                      |
| ---------------------------------- | -------------------------------------------- | ----------- | ------------------------- |
| `preprocess/data_preprocess.ipynb` | 清洗原始实验日志和问卷数据，生成标准化的 CSV | `data/raw/` | `data/preprocessed/*.csv` |

### 阶段二：加载数据与生成中间产物

| Notebook                                 | 功能                                                                 | 输入                      | 输出                                                                                                   |
| ---------------------------------------- | -------------------------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------ |
| `analysis/processing/01_load_data.ipynb` | 加载预处理后的 CSV，构建时间线，匹配点击与 AI 回复，生成 pickle 文件 | `data/preprocessed/*.csv` | `data/pickle/*.pkl`（participants、timeline、ai_events、user_msgs、assistant_msgs、semantic_richness） |

这一步是整个流水线的基础，后续所有分析都依赖它产出的 pickle 文件。主要操作包括：

- 从问卷数据中提取被试特质主表（人口学、人格、AI 态度等）
- 用 `merge_asof` 按时间就近匹配点击事件与 AI 回复（容差 10 秒）
- 为每个被试-物品组合构建按时间排序的事件时间线

### 阶段三：指标计算

| Notebook                                           | 功能                                                         | 输入                                     | 输出                                            |
| -------------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------- | ----------------------------------------------- |
| `analysis/processing/02_originality_scoring.ipynb` | 调用 Ocsai API 对所有用户回答进行原创性 LLM 评分             | `data/preprocessed/responses.csv`        | `data/analysis/scoring/originality.csv`         |
| `analysis/processing/performance_metrics.ipynb`    | 计算流畅性、原创性、高质量回答数                             | `data/analysis/scoring/originality.csv`  | `data/analysis/performance/performance.csv`     |
| `analysis/processing/ai_frequency.ipynb`           | 计算 AI 调用频率、时机、间隔、阶段分布                       | `data/pickle/ai_events.pkl`              | `data/analysis/ai_freq/ai_freq_metrics.csv`     |
| `analysis/processing/pre_call_metrics.ipynb`       | 计算每次 AI 调用前的认知状态（思考时间、语义距离）           | `data/pickle/timeline.pkl`               | `data/analysis/pre_call/pre_call_metrics.csv`   |
| `analysis/processing/post_call_metrics.ipynb`      | 计算每次 AI 调用后的行为特征（原创性提升、采纳率、语义跳跃） | `data/pickle/timeline.pkl` + originality | `data/analysis/post_call/post_call_metrics.csv` |

### 阶段四：报告与统计分析

| Notebook                                                     | 功能                   | 说明                                                             |
| ------------------------------------------------------------ | ---------------------- | ---------------------------------------------------------------- |
| `analysis/reporting/summarize.ipynb`                         | 数据概览与描述统计     | 总体想法数、调用数分布、零调用者比例                             |
| `analysis/reporting/performance_describe.ipynb`              | 绩效指标描述统计       | 按试次维度和物品维度的流畅性、原创性分布                         |
| `analysis/reporting/demographic.ipynb`                       | 人口学特征             | 性别、年龄分布                                                   |
| `analysis/reporting/by_trial/01_ai_call_features.ipynb`      | 试次级 AI 调用特征总览 | 聚合所有行为指标到试次维度，生成 `ai_call_features_by_trial.csv` |
| `analysis/reporting/by_trial/02_kmeans.ipynb`                | K-Means 聚类           | 基于调用行为特征的试次聚类（k=3），SVM 验证准确率 94%            |
| `analysis/reporting/by_trial/03a_correlation.ipynb`          | 相关分析               | 行为特征、人格特质与绩效指标的 Pearson 相关 + FDR 校正           |
| `analysis/reporting/by_trial/03b_cluster_main_effects.ipynb` | 簇间主效应             | LMM/GLMM 比较三个簇在原创性、流畅性、高质量回答上的差异          |
| `analysis/reporting/by_trial/03c_moderation.ipynb`           | 调节效应               | 人格特质 × 调用行为的交互作用 + Johnson-Neyman 简单斜率          |
| `analysis/reporting/by_trial/03d_zero_call.ipynb`            | 零调用分析             | 有调用 vs 无调用试次的绩效对比 + 贝叶斯因子                      |
| `analysis/reporting/by_trial/04_semantic_trace.ipynb`        | 语义搜索轨迹           | 相邻想法语义距离序列、AI 调用前后语义变化、ML 预测调用有效性     |
| `analysis/reporting/by_raw/01_raw_sequences.ipynb`           | 原始序列分析           | 300 个 0/1 数据点序列的原始输入分析                              |
| `analysis/reporting/by_raw/02_performance_relation.ipynb`    | 原始序列与绩效关系     | 序列模式与创造绩效的关联                                         |

## 目录结构

```plaintext
graduation/
├── preprocess/              # 原始数据预处理
│   └── data_preprocess.ipynb
├── analysis/
│   ├── processing/          # 指标计算，产出数据文件
│   │   ├── 01_load_data.ipynb
│   │   ├── 02_originality_scoring.ipynb
│   │   ├── performance_metrics.ipynb
│   │   ├── ai_frequency.ipynb
│   │   ├── pre_call_metrics.ipynb
│   │   └── post_call_metrics.ipynb
│   └── reporting/           # 可视化与统计推断
│       ├── summarize.ipynb
│       ├── performance_describe.ipynb
│       ├── demographic.ipynb
│       ├── by_trial/        # 试次级分析（主分析路径）
│       │   ├── 01_ai_call_features.ipynb
│       │   ├── 02_kmeans.ipynb
│       │   ├── 03a_correlation.ipynb
│       │   ├── 03b_cluster_main_effects.ipynb
│       │   ├── 03c_moderation.ipynb
│       │   ├── 03d_zero_call.ipynb
│       │   └── 04_semantic_trace.ipynb
│       └── by_raw/          # 原始序列分析
│           ├── 01_raw_sequences.ipynb
│           └── 02_performance_relation.ipynb
├── modules/                 # 本地 Python 模块
│   ├── semantic_toolbox/    # 语义处理工具（分词、向量加载、语义距离、聚类）
│   │   ├── textprocess/     # jieba 中文分词与停用词
│   │   ├── semdistance/     # 语义距离计算（余弦、欧氏、句子级）
│   │   ├── cluster/         # KMeans 聚类与 PCA 可视化
│   │   └── corpustrain/     # 模型路径配置 ⚠️ 首次运行必须修改
│   └── dat/                 # 发散联想任务（DAT）评分
├── data/
│   ├── raw/                 # 原始数据（不可修改）
│   │   ├── psychopy/        # 实验程序日志
│   │   └── questionnaire/   # 问卷数据
│   ├── preprocessed/        # 预处理后的 CSV
│   ├── pickle/              # 中间序列化产物（participants、timeline、ai_events 等）
│   ├── analysis/            # 计算出的指标输出
│   │   ├── ai_freq/         # AI 调用频率与时机
│   │   ├── post_call/       # 调用后行为特征
│   │   ├── pre_call/        # 调用前认知特征
│   │   ├── scoring/         # AUT 原创性评分
│   │   └── performance/     # 流畅性与原创性指标
│   ├── temp/                # 手动生成的临时 CSV
│   └── to_review/           # 待人工审核数据
├── review/                  # 数据审核与可视化
├── test/                    # 探索性/验证性测试
├── CONTEXT.md               # AI 辅助编程的详细上下文说明
└── README.md                # 本文件
```

## 本地模块说明

### `modules/semantic_toolbox`

语义处理工具集，在 `pre_call_metrics`、`post_call_metrics` 和 `04_semantic_trace` 等 notebook 中被导入使用。

- `textprocess/textcut.py`：基于 jieba 的中文分词与停用词处理
- `semdistance/get_vector.py`：加载 FastText/Word2Vec 模型，计算词/句/关系向量（**在导入时即加载模型**）
- `semdistance/distance.py`：余弦距离、欧氏距离、前向流距离、句子级语义距离、滑动窗口语义距离
- `cluster/kmeans.py`：KMeans 聚类与 PCA 可视化的封装工具
- `corpustrain/model_path.py`：**模型路径配置文件，首次运行前必须更新**

### `modules/dat`

发散联想任务（Divergent Association Task）评分工具，改编自[原始 DAT 实现](https://github.com/jayolson/divergent-association-task)以适配中文 FastText 向量。`scoring.py` 封装了共享 `Model` 实例的 `get_dat_score()` 函数。

## 数据文件约定

- `data/raw/` 为原始数据，**不可修改**
- `data/analysis/`、`data/pickle/`、`data/temp/` 下的文件均为衍生/生成产物。如需修改，应更新上游 notebook 而非手工编辑这些文件
- 路径使用：notebook 中均使用相对于 notebook 所在目录的相对路径（`../../data/...`），因此**必须从 notebook 所在目录运行**

## 常见问题

### 如何重新跑完整分析？

按流水线顺序执行：

0. `python modules/dat/get_words.py` — 从原始问卷提取 DAT 词典
1. `preprocess/data_preprocess.ipynb` — 从原始数据生成预处理 CSV
2. `analysis/processing/01_load_data.ipynb` — 生成所有中间 pickle 文件
3. `analysis/processing/02_originality_scoring.ipynb` — 评分（需网络访问 Ocsai API，耗时较长）
4. `analysis/processing/performance_metrics.ipynb` — 绩效指标
5. `analysis/processing/ai_frequency.ipynb` — 调用频率
6. `analysis/processing/pre_call_metrics.ipynb` — 调用前特征
7. `analysis/processing/post_call_metrics.ipynb` — 调用后特征
8. `analysis/reporting/by_trial/01_ai_call_features.ipynb` — 聚合特征
9. `analysis/reporting/by_trial/02_kmeans.ipynb` — 聚类
10. 其他 reporting notebook 可按需运行
