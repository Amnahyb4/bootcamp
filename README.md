# CSV Profiler 📊

A simple **Streamlit web application** that profiles CSV files and generates
summary statistics with export options in **JSON** and **Markdown** formats.

---

## 🚀 Features

- Upload a CSV file
- Preview the first rows of the dataset
- Generate a profiling report:
  - Number of rows and columns
  - Column-wise statistics
  - Automatic type detection (number / text)
  - Missing values analysis
- Export the report as:
  - `report.json`
  - `report.md`

---

## 📁 Project Structure

```text
bootcamp/
├── data/
│   └── sample.csv              # Example CSV file
│
├── output/                     # Generated reports (legacy)
│   ├── report.json
│   └── report.md
│
├── src/
│   └── csv_profiler/
│       ├── __init__.py
│       ├── app.py              # Streamlit application
│       ├── profile.py          # CSV profiling logic
│       ├── render.py           # JSON & Markdown export
│       ├── strings.py          # UI / text helpers
│       ├── io.py               # CSV reading utilities
│       └── models.py           # Data structures
│
├── main.py                     # App entry point
├── README.md                   # Project documentation
├── .gitignore
├── pyproject.toml              # Project dependencies
├── uv.lock                     # Dependency lock file
└── .python-version

---


## 📝 Notes

This project was built as part of an **AI bootcamp assignment** to practice:

- Data profiling
- Writing modular Python functions
- Building interactive UIs with Streamlit
- Using Git and GitHub for version control




