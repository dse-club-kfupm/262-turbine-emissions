<p align="center">
  <a href="https://github.com/dse-club-kfupm"><img src=".github/assets/logo.svg" alt="Data Engineering &amp; Science Club, KFUPM" width="150"></a>
</p>

<h1 align="center">Gas Turbine Emissions</h1>

<p align="center">
  <b>Predicting NOx emissions from gas turbine sensor data</b><br>
  A term 262 applied project of the <a href="https://github.com/dse-club-kfupm">Data Engineering &amp; Science Club, KFUPM</a>
</p>

<p align="center">
  <a href="https://docs.python.org/3/tutorial/"><img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="https://jupyter.org"><img alt="Jupyter" src="https://img.shields.io/badge/Jupyter-notebooks-F37626?logo=jupyter&logoColor=white"></a>
  <a href="https://pandas.pydata.org"><img alt="pandas" src="https://img.shields.io/badge/pandas-2.x-150458?logo=pandas&logoColor=white"></a>
  <a href="https://scikit-learn.org"><img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E?logo=scikitlearn&logoColor=white"></a>
  <a href="https://matplotlib.org"><img alt="Matplotlib and seaborn" src="https://img.shields.io/badge/charts-matplotlib%20%C2%B7%20seaborn-11557C"></a>
  <a href="https://www.manim.community"><img alt="Manim" src="https://img.shields.io/badge/animation-Manim-0E1E3A"></a>
</p>

<p align="center">
  <a href="https://github.com/dse-club-kfupm"><img alt="Term 262" src="https://img.shields.io/badge/term-262-1D3A6B"></a>
  <img alt="Energy and environment" src="https://img.shields.io/badge/field-Energy%20and%20environment-47ABD6">
  <a href="#evaluation"><img alt="Metric" src="https://img.shields.io/badge/metric-mean%20absolute%20error-3DD2A8"></a>
  <a href="data/README.md"><img alt="Data licence" src="https://img.shields.io/badge/data-CC%20BY%204.0-16A34A"></a>
  <a href="LICENSE"><img alt="Code licence" src="https://img.shields.io/badge/code-MIT-6B7280"></a>
  <a href="https://github.com/dse-club-kfupm/262-turbine-emissions/actions/workflows/format-check.yml"><img alt="Format check" src="https://github.com/dse-club-kfupm/262-turbine-emissions/actions/workflows/format-check.yml/badge.svg"></a>
</p>

<p align="center">
  <a href="#overview"><b>Overview</b></a> ·
  <a href="#dataset"><b>Dataset</b></a> ·
  <a href="#learning-path"><b>Learning path</b></a> ·
  <a href="#getting-started"><b>Getting started</b></a> ·
  <a href="#workflow"><b>Workflow</b></a> ·
  <a href="#deliverables"><b>Deliverables</b></a> ·
  <a href="#evaluation"><b>Evaluation</b></a> ·
  <a href="#rules"><b>Rules</b></a>
</p>

## Overview

Gas turbines burning natural gas produce a large share of the world's electricity, including in Saudi Arabia. Their exhaust contains nitrogen oxides (NOx), pollutants that contribute to smog and acid rain, so power plants must keep emissions within regulatory limits. Plants measure NOx with continuous emission monitoring systems, which are expensive to run and need regular calibration.

A predictive emission monitoring system (PEMS) estimates emissions from the turbine's own process measurements and can back up the analysers when they are offline. In this project you build the core of a PEMS: a regression model that predicts the hourly NOx concentration from ambient conditions and turbine sensor readings.

> [!NOTE]
> This is a case study. You will not operate a turbine or certify a monitoring system. You work with five years of hourly sensor data from one gas turbine in north-western Turkey, published with the benchmark study of Kaya, Tüfekci and Uzun (2019), and show how the data science workflow (understanding, cleaning, exploring, modelling and communicating) answers the question on that table.

### Project summary

|  |  |
| --- | --- |
| **Stakeholder** | The environmental compliance team of a gas-fired power plant that needs a software estimate of NOx to back up its stack analysers |
| **Question** | Given the turbine's hourly sensor readings and the ambient conditions, what is the NOx concentration in the exhaust? |
| **Target** | `NOX`: nitrogen oxides in the exhaust gas, in mg/m³ |
| **Evaluation** | Average error in mg/m³ on the 2015 data; lower is better ([details](#evaluation)) |
| **Training data** | 29,349 hourly records × 11 columns in `data/train.csv` |
| **Level** | Introductory: DATA 211, Introduction to Data Science |
| **Assessment** | 100 points: 50 for the prediction, 50 for charts, slides and an animation |

## Dataset

`data/train.csv` holds one row per hour of operation from 2011 to 2014, in time order. The committee keeps 2015 (7,384 hours) as the hidden test set, so the model is tested on a year it has never seen.

Carbon monoxide (CO) was removed from the table: it is measured by the same stack analysers as NOx, so a system that backs them up cannot rely on it.

| Column | Description | Unit |
| --- | --- | --- |
| `year` | Year of the record; the rows are in time order but have no date or hour | year |
| `AT` | Ambient temperature | °C |
| `AP` | Ambient pressure | mbar |
| `AH` | Ambient humidity | % |
| `AFDP` | Air filter differential pressure | mbar |
| `GTEP` | Gas turbine exhaust pressure | mbar |
| `TIT` | Turbine inlet temperature | °C |
| `TAT` | Turbine after temperature (exhaust temperature) | °C |
| `TEY` | Turbine energy yield | MWh |
| `CDP` | Compressor discharge pressure | mbar |
| `NOX` | **Target:** nitrogen oxides (NO + NO₂) in the exhaust gas | mg/m³ |

Test rows contain every column except `NOX`.

### Data considerations

- **The turbine changes over time.** The yearly average of NOx is about 68 to 70 mg/m³ in 2011 to 2013 and about 60 mg/m³ in 2014. Recent years describe the test year better than early ones, so check how much the older data helps.
- **Validate on a later year.** Split by year, as the hidden test does: for example, train on 2011 to 2013 and validate on 2014. Neighbouring hours are almost identical, so a random split makes the score look far better than it will be on the test.
- **Correlated sensors.** `TEY`, `CDP` and `GTEP` are almost perfectly correlated (above 0.98), because they all follow the turbine's load. Keep this in mind when you interpret a model or its feature importances.
- **A different split from the paper.** The original benchmark trains on 2011 to 2013 and tests on 2014 and 2015, so scores here are not directly comparable with the published results.

**Source.** Kaya, H., Tüfekci, P. and Uzun, E. (2019). Predicting CO and NOx emissions from gas turbines: novel data and a benchmark PEMS. *Turkish Journal of Electrical Engineering and Computer Sciences*, 27(6), 4783–4796. DOI [10.3906/elk-1807-87](https://doi.org/10.3906/elk-1807-87). Dataset: Gas Turbine CO and NOx Emission Data Set, UCI Machine Learning Repository, DOI [10.24432/C5WC95](https://doi.org/10.24432/C5WC95). Licence: CC BY 4.0.

## Learning path

The project assumes the level of DATA 211, Introduction to Data Science. If you have completed it, review the list and open only the topics you are unsure about. Each topic is needed by a specific milestone, so you can learn it just before that milestone. Most Kaggle Learn courses take a few hours and run in the browser.

| When | Topic | Why it is needed | Start with | Go further |
| --- | --- | --- | --- | --- |
| Before you start | Git and GitHub | Every change reaches `main` through a reviewed pull request | [Introduction to GitHub](https://github.com/skills/introduction-to-github) · GitHub Skills | [Pro Git](https://git-scm.com/book/en/v2), chapters 1 to 3 |
| Before you start | Python | The notebooks and `predict.py` are written in Python | [Python](https://www.kaggle.com/learn/python) · Kaggle Learn | [The Python Tutorial](https://docs.python.org/3/tutorial/) · python.org |
| Before you start | Environments | Install the project's packages in isolation | [Virtual environments and packages](https://docs.python.org/3/tutorial/venv.html) · python.org |  |
| Milestone 1 | pandas | Load, inspect and reshape the table | [Pandas](https://www.kaggle.com/learn/pandas) · Kaggle Learn | [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html) · pandas docs |
| Milestone 1 | Data cleaning | Handle missing and unusual values | [Data Cleaning](https://www.kaggle.com/learn/data-cleaning) · Kaggle Learn | [Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html) · pandas docs |
| Milestone 1 | Domain background | Understand what each column measures | [Dataset page](https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set) · UCI Machine Learning Repository |  |
| Milestone 2 | Visualisation | Show how the features relate to the target | [Data Visualization](https://www.kaggle.com/learn/data-visualization) · Kaggle Learn | [Ten Simple Rules for Better Figures](https://doi.org/10.1371/journal.pcbi.1003833) · PLOS |
| Milestone 3 | Modelling | Train a first model and compare it with the baseline | [Intro to Machine Learning](https://www.kaggle.com/learn/intro-to-machine-learning) · Kaggle Learn | [Getting started](https://scikit-learn.org/stable/getting_started.html) · scikit-learn |
| Milestone 3 | Better models | Pipelines, categorical features, missing values and leakage | [Intermediate Machine Learning](https://www.kaggle.com/learn/intermediate-machine-learning) · Kaggle Learn | [Feature Engineering](https://www.kaggle.com/learn/feature-engineering) · Kaggle Learn |
| Milestone 3 | Evaluation | Mean absolute error and validation on a later year | [Mean absolute error](https://scikit-learn.org/stable/modules/model_evaluation.html#mean-absolute-error) · scikit-learn | [Time series split](https://scikit-learn.org/stable/modules/cross_validation.html#time-series-split) · scikit-learn |
| Milestone 3 | Emission monitoring | What a PEMS is and how the benchmark was built | [The benchmark paper](https://doi.org/10.3906/elk-1807-87) · Kaya et al., 2019 | [Dataset description](https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set) · UCI |
| Milestone 4 | Animation | Explain the result in motion, in up to 2 minutes | [Quickstart](https://docs.manim.community/en/stable/tutorials/quickstart.html) · Manim | [Animations using Matplotlib](https://matplotlib.org/stable/users/explain/animations/animations.html) · Matplotlib |
| Milestone 4 | Presentation | Take the stakeholder from the question to the answer in 5 to 7 slides | [Ten Simple Rules for Making Good Oral Presentations](https://doi.org/10.1371/journal.pcbi.0030077) · PLOS |  |

## Getting started

You need Python 3.10 or newer and Git.

```bash
git clone https://github.com/dse-club-kfupm/262-turbine-emissions.git
cd 262-turbine-emissions
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Then open `notebooks/01_data_understanding.ipynb` and work through its questions.

- **No local setup?** Google Colab also works: upload `data/train.csv`, and commit your notebooks back to this repository.
- **Preparing the animation?** Install Manim separately with `pip install manim`, after the system packages listed in the [Manim installation guide](https://docs.manim.community/en/stable/installation.html).
- **Questions?** Ask in the organization's [Discussions](https://github.com/orgs/dse-club-kfupm/discussions) or open an issue with the Question template.

## Workflow

The work is divided into four milestones. Each milestone has its own issues in the [Issues tab](https://github.com/dse-club-kfupm/262-turbine-emissions/issues) and is complete when all of them are closed.

| Milestone | Complete when |
| --- | --- |
| 1. Data understanding | Notebook 01 and the cleaning functions in `src/features.py` are merged |
| 2. Exploration | Notebook 02, with charts and written findings, is merged |
| 3. Prediction submission | Notebook 03 and `src/predict.py` are merged and pass the format check |
| 4. Visual communication | The slides and the animation or video are merged |

For every change:

1. Choose an open issue and assign yourself to it.
2. Create a branch for it: `git switch -c short-description`.
3. Commit in small steps with clear messages, then push the branch.
4. Open a pull request into `main` and write `Closes #<issue number>` in its description.
5. A teammate reviews it. Once it is approved and the format check has passed, merge it.

Files in `data/`, `tests/` and `.github/` are owned by the committee: a pull request that changes them also needs a committee review.

**Validation guidance for milestone 3.** Split by year, as the hidden test does: for example, train on 2011 to 2013 and validate on 2014.

## Deliverables

**Part A · Prediction (50 points)**

- [ ] `src/predict.py` with a function `predict(df)`. It receives a table with the test columns and returns a number (NOx in mg/m³) for each row, in the same order as the rows of `df`.
- [ ] Notebooks 01 to 03, run from top to bottom, documenting how the model was developed.
- [ ] A passing format check. Run `python tests/check_submission.py` from the repository root before the final pull request; the same check runs automatically on every pull request.

**Part B · Visual communication (50 points)**

- [ ] Clear, labelled charts in the notebooks.
- [ ] 5 to 7 slides that take the stakeholder from the question to the answer, saved as PDF in `visuals/slides/`.
- [ ] An animation or a short video of up to 2 minutes made with Python (Manim or matplotlib), with its source code and the rendered file in `visuals/animation/`. A suggested subject: a period of turbine operation hour by hour, with the measured NOx drawn against the model's prediction, or how a change in ambient temperature shifts the predicted emissions.

## Evaluation

`predict.py` is run once on the hidden test set after the submission deadline. A team receives the points of the highest level it reaches; the levels are not added together.

| Level | Requirement | Points |
| --- | --- | --- |
| Runs | Returns a valid prediction for every test row | 10 |
| Bronze | Average error below the baseline's 11.11 mg/m³ (the baseline predicts the training average) | 30 |
| Silver | Average error of at most 9.24 mg/m³ | 40 |
| Gold | Average error of at most 7.36 mg/m³, the committee's reference model | 50 |

Average error is the mean absolute difference between the prediction and the measured NOx, in mg/m³. Lower is better.

| Part B | Missing | Basic | Good | Excellent |
| --- | --- | --- | --- | --- |
| Charts in the notebooks | 0 | 5 | 10 | 15 |
| Slides, 5 to 7, as PDF | 0 | 5 | 10 | 15 |
| Animation or video, made with Python, up to 2 minutes | 0 | 7 | 14 | 20 |

> [!IMPORTANT]
> Any team member may be asked to explain any part of the work. If no one can, the Part A points do not count.

## Rules

- Train only on `data/train.csv`.
- Using the 2015 data, or any other copy of this dataset, for training or prediction is not allowed.
- Every change reaches `main` through a pull request reviewed by a teammate.
- `predict.py` may use only pandas, NumPy and scikit-learn, so that it runs in the grading environment. Notebooks and visuals may also use matplotlib, seaborn, plotly and Manim.
- AI tools are allowed if they are declared in the Credits section, and every member must be able to explain the work.
- Follow the organization's [code of conduct](https://github.com/dse-club-kfupm/.github/blob/main/CODE_OF_CONDUCT.md).

## Repository structure

```text
262-turbine-emissions/
├── README.md
├── LICENSE                     MIT licence for the code
├── requirements.txt
├── data/
│   ├── train.csv
│   └── README.md               source and licence of the data
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_cleaning_and_exploration.ipynb
│   └── 03_modelling.ipynb
├── src/
│   ├── features.py             cleaning and feature functions
│   └── predict.py              submission entry point
├── models/                     saved model, if predict.py loads one
├── tests/
│   └── check_submission.py     format check, run before submitting
└── visuals/
    ├── slides/                 presentation as PDF
    └── animation/              animation source code and rendered video
```

## Credits

- **Project leads:** Name (@github), Name (@github)
- **Contributors:** Name (@github)
- **Organized by:** Applied Projects Committee, Data Engineering & Science Club, KFUPM
- **Data:** Kaya, Tüfekci and Uzun (2019), Gas Turbine CO and NOx Emission Data Set, UCI Machine Learning Repository, DOI 10.24432/C5WC95. Licence: CC BY 4.0.
- **AI tools used:** none, or name the tool and what it was used for
- **Licence:** the code is released under the [MIT licence](LICENSE); the data keeps its own licence, described in [data/README.md](data/README.md).

---

<p align="center">
  <sub>Applied Projects Committee · <a href="https://github.com/dse-club-kfupm">Data Engineering &amp; Science Club, KFUPM</a> · نادي هندسة وعلوم البيانات</sub>
</p>
