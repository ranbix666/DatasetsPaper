"""Combine COLM 2024 and 2025 full transcript CSVs into one file with a year column."""
from pathlib import Path

import pandas as pd

COLM_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = COLM_DIR / "colm_2024_2025_full_transcript.csv"


def main():
    df_2024 = pd.read_csv(COLM_DIR / "2024" / "colm2024_full_transcript.csv")
    df_2025 = pd.read_csv(COLM_DIR / "2025" / "colm2025_full_transcript.csv")

    df_2024["year"] = 2024
    df_2025["year"] = 2025

    # year as first column for clarity
    combined = pd.concat([df_2024, df_2025], ignore_index=True)
    cols = ["year"] + [c for c in combined.columns if c != "year"]
    combined = combined[cols]

    combined.to_csv(OUTPUT_PATH, index=False)
    print(f"Combined {len(df_2024)} (2024) + {len(df_2025)} (2025) = {len(combined)} rows")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
