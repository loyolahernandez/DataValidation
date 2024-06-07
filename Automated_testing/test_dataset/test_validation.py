import pandas as pd
import pytest

def validate_column(data, column_name, expected_dtype):
    assert data[column_name].dtype == expected_dtype, f"Expected {expected_dtype} but got {data[column_name].dtype}"

def test_data_validation():
    df = pd.read_csv('test_dataset.csv')
    validate_column(df, 'age', 'int64')