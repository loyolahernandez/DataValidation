# README.txt

This script performs data validation on a specific column within a DataFrame.

## Function `validate_column`

### Parameters:

- `data`: The DataFrame containing the data to be validated.
- `column_name`: The name of the column to be validated.
- `expected_dtype`: The expected data type for the column (e.g., `int64` for 64-bit integers).

### Function Body:

- The line `assert data[column_name].dtype == expected_dtype` checks that the data type of the specified column matches the expected data type.
- If the condition is `True`, the script continues without any issues.
- If the condition is `False`, an assertion error is raised with the specified message, indicating the expected data type and the actual data type.

## Test Function `test_data_validation`

### Workflow:

1. **Reading Data**: The data is read from the `test_dataset.csv` file and loaded into a DataFrame.
2. **Column Validation**: The `validate_column` function is called to verify that the `age` column has the `int64` data type.
3. **Running the Test**: `pytest` executes the test and verifies the validation. If there is an issue with the data type, an error is reported.

## Example Script

```python
import pandas as pd
import pytest

def validate_column(data, column_name, expected_dtype):
    assert data[column_name].dtype == expected_dtype, f"Expected {expected_dtype} but got {data[column_name].dtype}"

def test_data_validation():
    df = pd.read_csv('test_dataset.csv')
    validate_column(df, 'age', 'int64')
