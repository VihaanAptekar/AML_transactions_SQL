"""
Stratified sampler for the SAML-D dataset.

Keeps 100% of suspicious rows and samples normal rows
until the requested target size is reached.
"""

import argparse
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(
        description="Create a stratified SAML-D sample"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the full SAML-D CSV"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path for the generated sample CSV"
    )

    parser.add_argument(
        "--target",
        type=int,
        default=1_000_000,
        help="Target number of rows"
    )

    args = parser.parse_args()

    suspicious_parts = []
    normal_parts = []

    print("Reading the dataset in chunks...")

    for chunk in pd.read_csv(args.input, chunksize=500_000):
        suspicious_parts.append(
            chunk[chunk["Is_laundering"] == 1]
        )

        normal_parts.append(
            chunk[chunk["Is_laundering"] == 0]
        )

    suspicious = pd.concat(
        suspicious_parts,
        ignore_index=True
    )

    normal = pd.concat(
        normal_parts,
        ignore_index=True
    )

    normal_count = args.target - len(suspicious)

    if normal_count <= 0:
        raise ValueError(
            "The target size must be greater than the suspicious-row count."
        )

    if normal_count > len(normal):
        raise ValueError(
            "The requested sample is larger than the available normal rows."
        )

    normal_sampled = normal.sample(
        n=normal_count,
        random_state=42
    )

    sample = pd.concat(
        [suspicious, normal_sampled],
        ignore_index=True
    )

    sample = sample.sample(
        frac=1,
        random_state=42
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    sample.to_csv(
        output_path,
        index=False
    )

    print()
    print(f"Suspicious kept: {len(suspicious):,} (100%)")
    print(f"Normal sampled:  {len(normal_sampled):,}")
    print(f"Total written:   {len(sample):,}")
    print(f"Output file:     {output_path}")


if __name__ == "__main__":
    main()