import streamlit as st
import pandas as pd

st.set_page_config(page_title="Talking Rabbitt AI", layout="wide")
def find_best_column(df, cols, question_words):
    """Return the column whose name appears in the question, else first col."""
    for col in cols:
        if col.lower() in question_words:
            return col
    return cols[0]

def try_parse_date_column(df):
    """Return the first column that looks like dates, or None."""
    for col in df.select_dtypes(include="object").columns:
        try:
            parsed = pd.to_datetime(df[col], infer_format=True, errors="coerce")
            if parsed.notna().mean() > 0.8:   # 80 %+ parsed successfully
                return col, parsed
        except Exception:
            pass
    return None, None

st.title("🐰 Talking Rabbitt")
st.caption("Conversational Intelligence for Business Data")
st.divider()

uploaded_file = st.file_uploader("Upload your business dataset (CSV)", type=["csv"])

if not uploaded_file:
    st.info("Upload a CSV dataset to start exploring your data.")
    st.stop()

df = pd.read_csv(uploaded_file)

with st.expander("📋 Dataset preview", expanded=True):
    st.dataframe(df, use_container_width=True)
    st.caption(f"Columns: {', '.join(df.columns)}")

st.divider()

numeric_cols  = df.select_dtypes(include="number").columns.tolist()
category_cols = df.select_dtypes(include="object").columns.tolist()

if not numeric_cols:
    st.error("No numeric columns found — please upload a dataset with at least one number column.")
    st.stop()

question = st.text_input(
    "Ask a question about your data",
    placeholder='e.g. "Which region had the highest revenue?"',
)

if not question:
    st.stop()

q      = question.lower()
words  = set(q.split())
metric = find_best_column(df, numeric_cols, words)

st.subheader("🤖 AI Answer")

if any(kw in q for kw in ("highest", "max", "top", "most", "best")):
    if not category_cols:
        st.warning("No categorical column found to group by.")
        st.stop()

    category = find_best_column(df, category_cols, words)
    grouped  = df.groupby(category)[metric].sum().sort_values(ascending=False)
    top_cat  = grouped.idxmax()
    top_val  = grouped.max()
    total    = grouped.sum()
    pct      = (top_val / total * 100) if total else 0

    st.success(f"**{top_cat}** has the highest **{metric}**: {top_val:,.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Breakdown by category**")
        st.bar_chart(grouped)
    with col2:
        st.metric("Top contributor", top_cat, f"{pct:.1f}% of total")
        st.metric("Total " + metric, f"{total:,.2f}")
        st.metric("Entries analysed", len(df))

elif any(kw in q for kw in ("trend", "over time", "time", "monthly", "daily")):
    date_col, parsed = try_parse_date_column(df)
    if date_col is None:
        st.warning("No date-like column detected. Try including a date column in your CSV.")
    else:
        df["_date"] = parsed
        trend = df.groupby("_date")[metric].sum()
        st.markdown(f"**{metric} over time**")
        st.line_chart(trend)

elif any(kw in q for kw in ("average", "mean", "avg")):
    avg = df[metric].mean()
    st.success(f"The average **{metric}** is **{avg:,.2f}**")
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df[metric])
    with col2:
        st.metric("Mean",   f"{avg:,.2f}")
        st.metric("Median", f"{df[metric].median():,.2f}")
        st.metric("Std dev",f"{df[metric].std():,.2f}")

elif any(kw in q for kw in ("lowest", "min", "least", "worst")):
    if not category_cols:
        st.warning("No categorical column found to group by.")
        st.stop()
    category = find_best_column(df, category_cols, words)
    grouped  = df.groupby(category)[metric].sum().sort_values()
    bot_cat  = grouped.idxmin()
    bot_val  = grouped.min()
    st.success(f"**{bot_cat}** has the lowest **{metric}**: {bot_val:,.2f}")
    st.bar_chart(grouped)

else:
    st.markdown(f"**Quick summary of `{metric}`**")
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df[metric])
    with col2:
        st.metric("Total",   f"{df[metric].sum():,.2f}")
        st.metric("Average", f"{df[metric].mean():,.2f}")
        st.metric("Max",     f"{df[metric].max():,.2f}")
        st.metric("Min",     f"{df[metric].min():,.2f}")