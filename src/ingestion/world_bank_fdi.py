import requests
import pandas as pd
import yaml
from pathlib import Path

CONFIG_PATH = Path("config/config.yml")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def fetch_world_bank_fdi(indicator, start_year, end_year):
    url = (
        f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
        f"?format=json&per_page=20000&date={start_year}:{end_year}"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()[1]
    return pd.DataFrame(data)


def transform(df):
    df = df[["country", "date", "value"]].copy()
    df["country"] = df["country"].apply(lambda x: x["value"])
    df["year"] = df["date"].astype(int)
    df.drop(columns=["date"], inplace=True)
    return df


def main():
    config = load_config()
    dataset = config["datasets"]["world_bank_fdi"]

    df_raw = fetch_world_bank_fdi(
        indicator=dataset["indicator"],
        start_year=config["project"]["start_year"],
        end_year=config["project"]["end_year"],
    )

    df_clean = transform(df_raw)

    output_path = Path(config["paths"]["raw_data"])
    output_path.mkdir(parents=True, exist_ok=True)

    df_clean.to_parquet(
        output_path / "world_bank_fdi.parquet",
        index=False,
    )

    print("FDI data ingestion completed successfully.")


if __name__ == "__main__":
    main()
