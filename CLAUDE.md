# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a notebook-driven research project studying **AI-assisted creative performance in divergent thinking tasks**. A graduation thesis (Department of Psychology) investigates the **timing and frequency characteristics of voluntary AI use** during individual divergent thinking activities and their relationship with creative performance.

Most work happens in Jupyter notebooks under `analysis/`, `preprocess/`, and `review/`. There are no build steps, test suites, or package configs — this is a research codebase, not a deployable application.

Read `CONTEXT.md` first when orienting yourself.

## Research Context

### Research Questions

- **RQ1**: What distribution characteristics do individuals' AI invocation behaviors exhibit (call frequency, first-call time, call interval)? Can distinct AI call patterns be identified via clustering?
- **RQ2**: Are call behavior characteristics correlated with divergent thinking performance? Do different AI call patterns show performance differences?
- **RQ3**: How do individual cognitive processing characteristics differ before vs. after AI calls? Can pre-call behavioral features and cognitive state predict the effectiveness of AI calls?

### Experiment Design

- **Task**: Alternate Uses Task (AUT) — 4 formal rounds, 5 minutes each, plus 1 practice round (3 min, item: "soap")
- **Items**: 16 everyday objects divided into 4 balanced groups by semantic richness (based on Li et al., 2024 Chinese word association norms). Each group has 2 high- and 2 low-richness items, presented in low-high-low-high order:
  - Group 1: 罐头(can), 气球(balloon), 勺子(spoon), 雨伞(umbrella)
  - Group 2: 钥匙(key), 绳子(rope), 砖头(brick), 刀(knife)
  - Group 3: 衣架(hanger), 盒子(box), 螺丝刀(screwdriver), 袜子(sock)
  - Group 4: 床单(bedsheet), 报纸(newspaper), 轮胎(tire), 鞋子(shoe)
- **AI interaction**: Tool-based (not conversational) — subjects click a button to request an AI-generated AUT prompt. No limit on calls. Only the latest AI prompt is displayed (previous ones not accessible).
- **AI model**: Doubao-1.5-pro-32k (max_tokens=300, temperature=1.3, thinking mode off)
- **Platform**: PsychoPy 2025.1.1 for the experiment program; Credamo (见数) for subject recruitment and questionnaire; Tencent Cloud SCF for AI API proxy (avoids API key leakage, reduces PsychoPy bundle size)
- **Sample**: 500 valid participants (female 272, 54.4%; male 228, 45.6%), age M=29.4, SD=9.11, range 16–66. Data collection complete.

### Questionnaire Instruments (post-task)

| #       | Instrument                                                           | Items     | Scale                   |
| ------- | -------------------------------------------------------------------- | --------- | ----------------------- |
| Q1-Q2   | Demographics (gender, age)                                           | 2         | —                       |
| Q3      | Item familiarity                                                     | 16        | Likert 5                |
| Q4      | TIPI-C (Chinese Big Five; 李金德, 2013)                              | 10        | Likert 7                |
| Q5      | Creative Self-Efficacy (Gong et al., 2009; Tierney & Farmer, 2002)   | 4         | Likert 5                |
| Q6      | RIBS-S (Runco Ideational Behavior Scale - Short; Runco et al., 2014) | 19        | Likert 5                |
| Q7-Q10  | Creative task experience (difficulty, interest, effort, agency %)    | 4         | mixed                   |
| Q11-Q12 | AI use attribution (reasons, adoption approach)                      | multi + 4 | multi-select / Likert 5 |
| Q13-Q16 | AI attitude (familiarity, usage frequency)                           | 4         | mixed                   |

### Key Metrics

- **Fluency**: Total number of responses per subject (sum across 4 rounds).
- **Originality**: Scored via **Ocsai** (Organisciak et al., 2023), an LLM-based automated scoring method (r=0.81 with human raters). Language set to Chinese, other parameters default.
- **AI call features** (per round): call count, first-call time, pre-call idea count, call interval, call interval std (used as "call regularity" proxy).
- Flexibility and Elaboration are not currently computed (no mature automated solution identified).

## Environment

- VS Code is configured to use **conda** for both environment and package management (`.vscode/settings.json`). The conda environment is always **`graduation-design`**.
- Two local modules must be on `sys.path`: `modules/semantic_toolbox` and `modules/dat`. Notebooks typically add them with `sys.path.append("../../modules/...")` or rely on the `.vscode/settings.json` `extraPaths` configuration.
- Key dependencies visible from imports: `gensim`, `jieba`, `scipy`, `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `nltk`.
- Python 3.12. Significance level α = 0.05 throughout.

## Pipeline Order

Rerun analysis in this sequence; each stage depends on outputs from the previous:

1. **Preprocess** — `preprocess/data_preprocess.ipynb`
2. **Load data** — `analysis/processing/01_load_data.ipynb`
3. **Compute metrics** — `analysis/processing/02_originality_scoring.ipynb`, `analysis/processing/performance_metrics.ipynb`, `analysis/processing/pre_call_metrics.ipynb`, `analysis/processing/post_call_metrics.ipynb`, `analysis/processing/ai_frequency.ipynb`
4. **Report** — `analysis/reporting/*.ipynb`, especially `analysis/reporting/summarize.ipynb`

## Local Modules

### `modules/semantic_toolbox`

Fork of an open-source semantic processing tool. Provides:

- `textprocess/textcut.py` — Chinese text segmentation (jieba-based) and stopword handling
- `semdistance/get_vector.py` — Loads FastText/Word2Vec models, computes word/sentence/relation vectors. **Loads the model at import time** from the path in `corpustrain/model_path.py`.
- `semdistance/distance.py` — Cosine, Euclidean, forward-flow, sentence-level, and windowed semantic distances
- `cluster/kmeans.py` — KMeans clustering and PCA visualization for word vectors
- `corpustrain/model_path.py` — **Must be updated** before running any semantic analysis. Points to a `.bin` FastText model downloaded from [Chinese-Word-Vectors](https://github.com/Embedding/Chinese-Word-Vectors).

### `modules/dat`

Divergent Association Task scoring (creativity measure based on semantic distance between unrelated words). Adapted from the original [DAT implementation](https://github.com/jayolson/divergent-association-task) to use Chinese FastText vectors. `scoring.py` wraps `dat.py` with a shared `Model` instance; notebooks import `get_dat_score()` from here.

## Data Directory Conventions

- `data/raw/` — Canonical source data (experiment logs, questionnaire responses). **Do not modify.**
- `data/preprocessed/` — Cleaned tabular inputs.
- `data/pickle/` — Intermediate serialized artifacts (AI call events, user responses, etc.).
- `data/analysis/` — Computed metric outputs, organized by subtask (`ai_freq/`, `post_call/`, `pre_call/`, `scoring/`).
- `data/temp/` — Manually generated CSVs for short-lived exchange.
- `data/to_review/` — Files staged for manual review.

Treat everything under `data/analysis/`, `data/pickle/`, and `data/temp/` as derived/generated. When a change is needed, update the upstream notebook rather than hand-editing these files.

## Path Caveats

- Notebooks use relative paths like `../../data/...`. Run them from their own directory.
- The semantic toolbox model path (`modules/semantic_toolbox/corpustrain/model_path.py`) is an absolute Windows path hardcoded to the author's machine. Any fresh checkout must update this.
- `modules/dat/dat.py` also hardcodes a default model path in `DEFAULT_MODEL`.
