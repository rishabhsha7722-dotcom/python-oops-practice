# Task 10 – CSV Data Pipeline & EDA

## Requirements
- Python 3.10+
- pandas
- numpy

## Run in VS Code
1. Open this project folder in VS Code.
2. Open Terminal (`View > Terminal`).
3. Create/activate a virtual environment:
   - macOS: `python3 -m venv .venv`
   - macOS: `source .venv/bin/activate`
4. Install packages: `python -m pip install pandas numpy`
5. Run: `python src/customer_data_pipeline.py`

## Output files
- `output/data_quality_report.csv`
- `output/eda_summary.csv`
- `output/cleaned_customer_data.csv`

## Notes
The sample dataset includes missing values and one duplicate row as specified in the assignment.
`IncomePerExperience` is set to 0 when Experience is 0 to prevent division by zero.
The validation stage checks the required numeric ranges and target values.
