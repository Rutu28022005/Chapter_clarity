import re
import streamlit as st
import textstat
import streamlit.components.v1 as components

st.set_page_config(page_title="Chapter Clarity", page_icon="📚", layout="wide")

st.title("📚 Chapter Clarity")
st.write("Paste a chapter to estimate readability and find the five sentences that may be hardest to read.")

chapter = st.text_area(
    "Your chapter",
    height=260,
    placeholder="Paste your chapter here...",
)

def split_sentences(text):
    # Simple sentence splitting; abbreviations and dialogue may need manual review.
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def difficulty(sentence):
    words = re.findall(r"\b[\w'-]+\b", sentence)
    if not words:
        return 0
    long_words = sum(1 for w in words if len(re.findall(r"[aeiouy]+", w.lower())) >= 3)
    avg_len = len(words)
    # Transparent heuristic: long sentences and multisyllabic words raise the score.
    return round(avg_len * 0.6 + (long_words / len(words)) * 12, 2)

if st.button("Analyze chapter", type="primary"):
    if len(chapter.split()) < 20:
        st.warning("Please paste at least 20 words for a more useful estimate.")
    else:
        sentences = split_sentences(chapter)
        score = textstat.flesch_reading_ease(chapter)
        grade = textstat.flesch_kincaid_grade(chapter)
        words = len(re.findall(r"\b[\w'-]+\b", chapter))

        c1, c2, c3 = st.columns(3)
        c1.metric("Flesch Reading Ease", f"{score:.1f}/100")
        c2.metric("Estimated US grade level", f"{grade:.1f}")
        c3.metric("Word count", f"{words:,}")

        if score >= 70:
            st.caption("Overall: generally easier to read.")
        elif score >= 50:
            st.caption("Overall: moderately difficult; consider simplifying dense passages.")
        else:
            st.caption("Overall: difficult; shorter sentences and simpler wording may help.")

        ranked = sorted(enumerate(sentences), key=lambda item: difficulty(item[1]), reverse=True)[:5]
        hard_ids = {idx for idx, _ in ranked}
        st.subheader("Five sentences to review")
        if not sentences:
            st.info("No sentences were detected. Check the punctuation and try again.")
        else:
            for rank, (idx, sentence) in enumerate(ranked, start=1):
                st.markdown(f"**{rank}.** {sentence}")
                st.caption(f"Sentence-length / word-complexity heuristic: {difficulty(sentence):.2f}")

        st.subheader("Chapter with difficult sentences highlighted")
        # Render escaped text to avoid treating pasted text as HTML.
        import html
        rendered = []
        for idx, sentence in enumerate(sentences):
            safe = html.escape(sentence)
            if idx in hard_ids:
                rendered.append(
                    f'<span style="background:#ffe08a; padding:2px 4px; border-radius:4px;">{safe}</span>'
                )
            else:
                rendered.append(safe)
        html_text = " ".join(rendered)
        components.html(
            f"""<div style="font-family:Arial,sans-serif;line-height:1.8;font-size:16px;">{html_text}</div>""",
            height=300,
            scrolling=True,
        )
        st.caption("Note: readability scores and the five-sentence ranking are estimates, not editorial judgments. Review the highlighted sentences in context.")

st.divider()
st.caption("Free prototype • Readability powered by textstat • No account required")
