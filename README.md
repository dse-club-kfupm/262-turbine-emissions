# World Cup Oracle: Can a Model Call the Match?

Data Engineering & Science Club, Applied Projects Committee, KFUPM. Term 262. Prediction case study.

On 22 November 2022, Saudi Arabia beat Argentina 2-1 at the World Cup in Qatar, one of the great upsets of the tournament. Football results are uncertain, but they are not random: stronger teams win more often, playing at home helps, and recent form matters.

In this project you build a model that predicts the result of an international match (a win for the first-listed team, a draw, or a win for the second-listed team) from the history of past results.

## Scope

This is a case study. You will not build a betting tool or a live service. You work with one table of past results and show how the data science workflow (understanding, cleaning, exploring, modelling and communicating) answers the question on that table. Your model is tested on the matches of the 2026 FIFA World Cup, which it has never seen.

## The client and the question

| Item | Description |
| --- | --- |
| Client | An analyst preparing match reports for a national team's technical staff |
| Question | Given two teams, the date and the venue, which result is most likely? |
| Prediction | `result`: `home_win`, `draw` or `away_win`, where "home" means the first-listed team |
| Score | Balanced accuracy on the hidden test set (see Grading) |

## The data

`data/train.csv` contains every men's full international match in the source from 30 November 1872 to 10 June 2026, the day before the 2026 World Cup began. The committee holds the World Cup matches as the hidden test set. For a test match your model receives the date, the teams, the tournament and the venue; the score is what it must predict.

Scores include extra time but not penalty shoot-outs, so a knockout match decided on penalties counts as a draw. Teams appear under their current names; countries appear under the name they had at the time of the match.

| Column | Meaning | Unit |
| --- | --- | --- |
| `date` | Match date | YYYY-MM-DD |
| `home_team` | First-listed team; the host when `neutral` is FALSE | text |
| `away_team` | Second-listed team | text |
| `home_score` | Goals by the first-listed team, including extra time | goals |
| `away_score` | Goals by the second-listed team, including extra time | goals |
| `tournament` | Competition, for example FIFA World Cup or Friendly | text |
| `city` | City where the match was played | text |
| `country` | Country where the match was played | text |
| `neutral` | TRUE if neither team played at home | TRUE or FALSE |
| `result` | Target: `home_win`, `draw` or `away_win` | label |

Test rows contain every column except `home_score`, `away_score` and `result`.

Source: International football results from 1872 to 2026, compiled by Mart Jürisoo. Licence: CC0 1.0 (public domain). <https://github.com/martj42/international_results>

## Prerequisites

Learn these before you start. Each row gives one source to start with and one to go further.

| Skill | Start with | Go further |
| --- | --- | --- |
| Git and GitHub | [Introduction to GitHub](https://github.com/skills/introduction-to-github), GitHub Skills | [Pro Git](https://git-scm.com/book/en/v2), chapters 1 to 3 |
| Python | [Python](https://www.kaggle.com/learn/python), Kaggle Learn | [The Python Tutorial](https://docs.python.org/3/tutorial/) |
| pandas | [Pandas](https://www.kaggle.com/learn/pandas), Kaggle Learn | [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html) |
| Data cleaning | [Data Cleaning](https://www.kaggle.com/learn/data-cleaning), Kaggle Learn | [Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html) |
| Charts | [Data Visualization](https://www.kaggle.com/learn/data-visualization), Kaggle Learn | [Ten Simple Rules for Better Figures](https://doi.org/10.1371/journal.pcbi.1003833) |
| Prediction | [Intro to Machine Learning](https://www.kaggle.com/learn/intro-to-machine-learning), Kaggle Learn | [scikit-learn: Getting started](https://scikit-learn.org/stable/getting_started.html) |
| Animation | [Manim Community quickstart](https://docs.manim.community/en/stable/tutorials/quickstart.html) | [Animations using Matplotlib](https://matplotlib.org/stable/users/explain/animations/animations.html) |
| Slides | [Ten Simple Rules for Making Good Oral Presentations](https://doi.org/10.1371/journal.pcbi.0030077) |  |

Background on the data: [the dataset page](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017), which explains every file and column.

## Getting started

```bash
git clone https://github.com/dse-club-kfupm/262-world-cup-oracle.git
cd 262-world-cup-oracle
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Open `notebooks/01_data_understanding.ipynb`. Google Colab is also acceptable; upload `data/train.csv` and keep your notebooks in the repository.

## Repository structure

```text
262-world-cup-oracle/
├── README.md
├── requirements.txt
├── data/
│   ├── train.csv
│   └── README.md               source and licence
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_cleaning_and_exploration.ipynb
│   └── 03_modelling.ipynb
├── src/
│   ├── features.py             cleaning and feature functions
│   └── predict.py              submission entry point
├── models/                     saved model, if predict.py loads one
├── tests/
│   └── check_submission.py     run before submitting
└── visuals/
    ├── slides/                 presentation as PDF
    └── animation/              animation source code and rendered video
```

## What you submit

Part A, prediction (50 points)

- `src/predict.py` containing a function `predict(df)`. It receives a table with the test columns described above and returns one of "home_win", "draw" or "away_win" per row, in the same order.
- The three notebooks showing how you reached the model.
- Run `python tests/check_submission.py` before your final pull request. It confirms that `predict.py` loads and returns predictions in the right format.

Part B, visual communication (50 points)

- Clear, labelled charts in the notebooks.
- Slides: 5 to 7 slides that take the client from the question to the answer, saved as PDF in `visuals/slides/`.
- An animation or a short video of up to 2 minutes made with Python (Manim or matplotlib), with its source code and the rendered file in `visuals/animation/`. A good subject: how the strength of a few national teams rises and falls over the decades, or how your model's predicted chances change from match to match during a tournament.

## Grading

Your `predict.py` is run once on the hidden test set after the submission deadline.

| Level | Requirement | Points |
| --- | --- | --- |
| Runs | Returns a valid prediction for every test row | 10 |
| Bronze | Scores above the baseline, which always predicts a win for the first-listed team: 33.3% | 30 |
| Silver | Balanced accuracy of at least 45.3% | 40 |
| Gold | Balanced accuracy of at least 57.4%, the committee's reference model | 50 |

Balanced accuracy is the average, over the three results, of the share of matches with that result that your model predicts correctly. A model that always gives the same answer scores 33.3%.

| Part B | Missing | Basic | Good | Excellent |
| --- | --- | --- | --- | --- |
| Charts in the notebooks | 0 | 5 | 10 | 15 |
| Slides, 5 to 7, as PDF | 0 | 5 | 10 | 15 |
| Animation or video, made with Python, up to 2 minutes | 0 | 7 | 14 | 20 |

Any team member may be asked to explain any part of the work. If no one can, the Part A points do not count.

## Milestones

Progress is tracked with four milestones, each with its own issues.

| Milestone | Complete when |
| --- | --- |
| 1. Data understanding | Notebook 01 and the cleaning functions are merged |
| 2. Exploration | Notebook 02, with charts and written findings, is merged |
| 3. Prediction submission | Notebook 03 and `src/predict.py` are merged and pass the format check |
| 4. Visual communication | The slides and the animation or video are merged |

## Rules

- Train only on `data/train.csv`.
- History for a test match may come only from `data/train.csv`. Results of matches played on or after 11 June 2026 may not be used.
- Every change reaches `main` through a pull request reviewed by a teammate.
- AI tools are allowed if declared in the Credits section, and every member must be able to explain the work.
- `predict.py` may use only pandas, NumPy and scikit-learn, so that it runs in the grading environment. Notebooks and visuals may also use matplotlib, seaborn, plotly and Manim.

## Credits

- Project Leads: Name (@github), Name (@github)
- Contributors: Name (@github)
- Organized by: Applied Projects Committee, Data Engineering & Science Club, KFUPM
- Data: International football results from 1872 to 2026, compiled by Mart Jürisoo. Licence: CC0 1.0 (public domain).
- AI tools used: none, or name the tool and what it was used for
