# Chapter Clarity

A free Streamlit web tool that estimates chapter readability and highlights five potentially difficult sentences.

## Run locally
1. Install Python 3.10+.
2. In this folder, run: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`

## Deploy for a live link (free)
1. Upload `app.py`` and `requirements.txt` to a public GitHub repository.
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Choose the repository, branch, and `app.py`.
4. Click Deploy. Streamlit will provide a live URL.

## Limitation
Sentence ranking uses a transparent heuristic based on sentence length and the proportion of long words. It can miss difficult ideas in short sentences and may split abbreviations or dialogue incorrectly. Readability scores are estimates.
