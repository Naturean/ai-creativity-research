# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Notebook-driven research project studying **AI-assisted creative performance in divergent thinking tasks**. A graduation thesis (Department of Psychology) investigating the **timing and frequency characteristics of voluntary AI use** during individual divergent thinking and their relationship with creative performance.

No build steps, test suites, or package configs — this is a research codebase, not a deployable application. Read `CONTEXT.md` first when orienting yourself.

## Research Context

### Research Questions

- **RQ1**: What distribution characteristics do individuals' AI invocation behaviors exhibit (call frequency, first-call time, call interval)? Can distinct AI call patterns be identified via clustering?
- **RQ2**: Are call behavior characteristics correlated with divergent thinking performance? Do different AI call pattern groups show performance differences?
- **RQ3**: How do individual cognitive processing characteristics differ before vs. after AI calls? Can pre-call behavioral features and cognitive state predict the effectiveness of AI calls?

### Experiment Design

- **Task**: Alternate Uses Task (AUT) — 4 formal rounds, 5 minutes each, plus 1 practice round (3 min, item: "soap")
- **Items**: 16 everyday objects divided into 4 balanced groups by semantic richness (Li et al., 2024 Chinese word association norms). Each group: 2 high- + 2 low-richness items, presented low-high-low-high:
  - Group 1: 罐头(can), 气球(balloon), 勺子(spoon), 雨伞(umbrella)
  - Group 2: 钥匙(key), 绳子(rope), 砖头(brick), 刀(knife)
  - Group 3: 衣架(hanger), 盒子(box), 螺丝刀(screwdriver), 袜子(sock)
  - Group 4: 床单(bedsheet), 报纸(newspaper), 轮胎(tire), 鞋子(shoe)
- **AI interaction**: Tool-based (not conversational) — subjects click a button to request an AI-generated AUT prompt. No limit on calls. Only the latest AI prompt is displayed.
- **AI model**: Doubao-1.5-pro-32k (max_tokens=300, temperature=1.3, thinking mode off)
- **Platform**: PsychoPy 2025.1.1 (experiment); Credamo 见数 (subjects + questionnaire); Tencent Cloud SCF (AI API proxy)
- **Sample**: ~500 valid participants. Data collection complete.

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

- **Fluency**: Total responses per subject (sum across 4 rounds).
- **Originality**: Scored via **Ocsai** (Organisciak et al., 2023), LLM-based automated scoring (r=0.81 with human raters). Chinese mode, default parameters.
- **AI call features** (per round): call count, first-call time, pre-call idea count, call interval, call interval std (proxy for "call regularity").
- Flexibility and Elaboration are not computed (no mature automated solution).

## Environment

- Conda environment: **`graduation-design`** (Python 3.12). Create from `environment.yml` at repo root.
- Key dependencies: `gensim`, `jieba`, `fasttext-wheel`, `scipy`, `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `nltk`, `statsmodels`, `umap-learn`, `kneed`, `seaborn`, `patsy`, `tqdm`, `requests`.
- Two local modules on `sys.path`: `modules/semantic_toolbox` and `modules/dat`. Notebooks add them via `sys.path.append("../../modules/...")` or rely on `.vscode/settings.json` `extraPaths`.
- Significance level α = 0.05 throughout.

## Pipeline Order

Run in this sequence; each stage depends on previous outputs. All notebooks must be run from their own directory (internal paths use `../../data/...`).

0. **Generate words.txt** — `python modules/dat/get_words.py` — extracts DAT word dictionary from raw questionnaire CSV. Must run before preprocess because `dat.py` loads `words.txt` at import time.
1. **Preprocess** — `preprocess/data_preprocess.ipynb`
2. **Load data** — `analysis/processing/01_load_data.ipynb`
3. **Compute metrics**:
   - `analysis/processing/02_originality_scoring.ipynb` — Ocsai API scoring (requires network; slow)
   - `analysis/processing/performance_metrics.ipynb` — fluency, originality, high-quality response count
   - `analysis/processing/ai_frequency.ipynb` — AI call frequency, timing, interval, phase distribution
   - `analysis/processing/pre_call_metrics.ipynb` — pre-call cognitive state (thinking time, semantic distance)
   - `analysis/processing/post_call_metrics.ipynb` — post-call behavioral features (originality gain, adoption, semantic jump)
4. **Report** — `analysis/reporting/`:
   - `summarize.ipynb`, `performance_describe.ipynb`, `demographic.ipynb`
   - `by_trial/01_ai_call_features.ipynb` — aggregate metrics to trial level
   - `by_trial/02_kmeans.ipynb` — K-Means clustering (k=3), SVM validation accuracy 94%
   - `by_trial/03a_correlation.ipynb` — Pearson correlations + FDR correction
   - `by_trial/03b_cluster_main_effects.ipynb` — LMM/GLMM cluster comparisons
   - `by_trial/03c_moderation.ipynb` — personality × call behavior interactions + Johnson-Neyman
   - `by_trial/03d_zero_call.ipynb` — call vs. no-call trial comparison + Bayes factors
   - `by_trial/04_semantic_trace.ipynb` — semantic distance sequences, ML prediction of call effectiveness
   - `by_raw/01_raw_sequences.ipynb` — raw 0/1 sequence analysis
   - `by_raw/02_performance_relation.ipynb` — sequence patterns vs. creative performance

## Local Modules

### `modules/semantic_toolbox`

Fork of an open-source semantic processing tool. Used by `pre_call_metrics`, `post_call_metrics`, and `04_semantic_trace`.

- `textprocess/textcut.py` — Chinese text segmentation (jieba-based) and stopword handling
- `semdistance/get_vector.py` — Loads FastText/Word2Vec models; computes word/sentence/relation vectors. **Loads the model at import time** from `corpustrain/model_path.py`.
- `semdistance/distance.py` — Cosine, Euclidean, forward-flow, sentence-level, and windowed semantic distances
- `cluster/kmeans.py` — KMeans clustering and PCA visualization
- `corpustrain/model_path.py` — **Model path config. Must be updated before first run.** Points to a FastText `.bin` model from [fastText Crawl Vectors](https://fasttext.cc/docs/en/crawl-vectors.html) (use `cc.zh.300.bin`).

### `modules/dat`

Divergent Association Task scoring, adapted from the [original DAT](https://github.com/jayolson/divergent-association-task) for Chinese FastText vectors. `scoring.py` wraps `dat.py` with a shared `Model` instance; import `get_dat_score()` from here.

## Data Directory Conventions

- `data/raw/` — Canonical source data. **Do not modify.**
- `data/preprocessed/` — Cleaned tabular inputs.
- `data/pickle/` — Intermediate serialized artifacts.
- `data/analysis/` — Computed metric outputs (`ai_freq/`, `post_call/`, `pre_call/`, `scoring/`, `performance/`).
- `data/temp/` — Temporary CSVs for short-lived exchange.
- `data/to_review/` — Files staged for manual review.

Everything under `data/analysis/`, `data/pickle/`, and `data/temp/` is derived. Update the upstream notebook rather than hand-editing these files.

## Path Caveats

- Notebooks use relative paths like `../../data/...`. Run them from their own directory.
- `modules/semantic_toolbox/corpustrain/model_path.py` hardcodes an absolute Windows path. Any fresh checkout must update this.
- `modules/dat/dat.py` also hardcodes a default model path in `DEFAULT_MODEL`.
