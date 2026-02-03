import pandas as pd
from pathlib import Path


def run_quality_checks():
    data_path = Path("data/raw/world_bank_fdi.parquet")

    if not data_path.exists():
        raise FileNotFoundError("FDI parquet file not found")

    df = pd.read_parquet(data_path)

    # Required keys must be present
    assert df["country"].notna().all(), "Null values found in country column"
    assert df["year"].notna().all(), "Null values found in year column"
    assert df["year"].between(2013, 2023).all(), "Year out of expected range"

    # Value can be null in BRONZE, but we enforce a minimum completeness threshold
    value_non_null_ratio = df["value"].notna().mean()
    min_ratio = 0.60  # 60% completeness threshold (tunable)

    assert value_non_null_ratio >= min_ratio, (
        f"FDI value completeness too low: {value_non_null_ratio:.2%} "
        f"(minimum required: {min_ratio:.0%})"
    )

    print(
        f"FDI data quality checks passed. value completeness: {value_non_null_ratio:.2%}"
    )


if __name__ == "__main__":
    run_quality_checks()
