# 🐰 Talking Rabbitt

> **Conversational AI for Enterprise Analytics** — talk to your business data instead of building dashboards.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## What Is This?

Talking Rabbitt is an AI-powered conversational data interface. Instead of navigating complex dashboards in PowerBI or Tableau, business leaders can simply **ask a question in plain English** and get an instant answer with an auto-generated chart.

**The magic moment:** Replace a 10-minute Excel filter session with a 5-second conversation.

---

## Live Demo

> Upload any sales CSV → Ask a question → Get an answer + visualization instantly.

**Example queries you can try:**
- `Which region had the highest revenue?`
- `What is the average deal value?`
- `Show me the revenue trend over time`
- `Which product had the lowest sales?`

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/talking-rabbitt.git
cd talking-rabbitt

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Project Structure

```
talking-rabbitt/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── sample_data/
│   └── sales_sample.csv    # Sample dataset to test with
└── README.md
```

---

## Sample Dataset

A sample CSV is included in `sample_data/sales_sample.csv`. It contains:

| Column   | Description                  |
|----------|------------------------------|
| Region   | Sales region (North, South…) |
| Product  | Product line name            |
| Revenue  | Revenue in USD               |
| Quarter  | Reporting quarter            |
| Rep      | Sales representative name    |

---

## Requirements

```
streamlit>=1.28.0
pandas>=2.0.0
matplotlib>=3.7.0
```

---

## How It Works

1. **Upload** — User uploads a standard sales CSV file
2. **Ask** — User types a plain-English question
3. **Analyze** — The app detects intent (highest, average, trend, lowest) and maps it to the right columns
4. **Deliver** — An answer + chart is returned in under 5 seconds







