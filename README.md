# AI-Driven Claims Verification — Variable Explainer

Interactive Streamlit dashboard explaining every PLS-SEM variable from the IBR research
*"AI-Driven Claims Verification in the Indian Insurance Industry"* — what the numbers found,
what it means in plain language, and real supporting quotes from expert interviews and
94 open-text survey answers.

## What it shows

For each of 10 constructs (Relative Advantage, Fraud Detection Capacity, Decision-Making
Speed, Customer Digital Adoption, Data Quality, System Integration, Employee Competence,
Top Management Support, Regulatory Clarity, and Operational Efficiency):

- The quantitative result (path coefficients, p-values, effect sizes, reliability)
- A plain-language explanation of what the result means
- A verbatim quote from one of two expert interviews
- Verbatim quotes from the 94 open-text survey responses

All data is embedded directly in `streamlit_app.py` — no external files or database needed.

## Run it locally

```bash
git clone <this-repo-url>
cd <this-repo-folder>
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app opens automatically in your browser at `http://localhost:8501`.

## Deploy it (free, shareable link)

The easiest option is [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push this repo to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Click **New app**, pick this repo, set the main file to `streamlit_app.py`, and deploy.
4. You'll get a public `*.streamlit.app` link you can share with your committee.

## Project background

Built from:
- SmartPLS 4 structural equation model, n=105 survey respondents
- 2 expert interviews (a zonal claims manager and a senior claims/risk executive)
- 94 open-text responses to "What would need to change for AI to be more effective
  in claims verification at your organization?"

## License

For academic use as part of an Independent Business Research (IBR) project.
