"""
Stratified sampler for the SAML-D dataset.

Keeps 100% of suspicious (Is_laundering = 1) rows and stratified-samples
normal rows down to a target total (~1M). Preserves the class imbalance
realistically enough for AML pattern analysis while staying fast on a laptop.

Usage:
    python scripts/01_prepare_data.py --input data/raw/SAML-D.csv \
                                      --output data/sample/SAML-D_sample_1M.csv \
                                      --target 1000000
"""
import argparse

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Stratified sampler for SAML-D")
    parser.add_argument("--input", required=True, help="Path to full SAML-D CSV")
    parser.add_argument("--output", required=True, help="Path to write the sample")
    parser.add_argument("--target", type=int, default=1_000_000)
    args = parser.parse_args()

    chunks = pd.read_csv(args.input, chunksize=500_000)
    suspicious_parts, normal_parts = [], []
    for chunk in chunks:
        suspicious_parts.append(chunk[chunk["Is_laundering"] == 1])
        normal_parts.append(chunk[chunk["Is_laundering"] == 0])

    suspicious = pd.concat(suspicious_parts, ignore_index=True)
    normal = pd.concat(normal_parts, ignore_index=True)

    n_normal = max(args.target - len(suspicious), 0)
    normal_sampled = normal.sample(n=n_normal, random_state=42)

    sample = (
        pd.concat([suspicious, normal_sampled], ignore_index=True)
        .sample(frac=1, random_state=42)  # shuffle
    )
    sample.to_csv(args.output, index=False)

    print(f"Suspicious kept: {len(suspicious):,} (100%)")
    print(f"Normal sampled:  {len(normal_sampled):,}")
    print(f"Total written:   {len(sample):,} -> {args.output}")


if __name__ == "__main__":
    main()
