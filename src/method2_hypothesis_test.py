"""Test whether the mean daily USD/SGD log return is zero."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "DEXSIUS_cleaned.csv"
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURE_DIR = PROJECT_ROOT / "outputs" / "figures"

B = 10_000
SEED = 60702
ALPHA = 0.05


def main() -> None:
    # Load and validate the daily log returns.
    df = pd.read_csv(INPUT_FILE)
    if "log_return_pct" not in df.columns:
        raise ValueError(f"Column 'log_return_pct' not found in {INPUT_FILE}")

    returns = (
        pd.to_numeric(df["log_return_pct"], errors="raise")
        .dropna()
        .to_numpy(dtype=float)
    )
    if returns.size < 2:
        raise ValueError("At least two valid log returns are required.")
    if not np.isfinite(returns).all():
        raise ValueError("Log returns contain non-finite values.")

    # Compute the sample statistics and two-sided Wald z-test.
    n = returns.size
    mean = returns.mean()
    sample_sd = returns.std(ddof=1)
    standard_error = sample_sd / np.sqrt(n)
    z_statistic = mean / standard_error
    p_wald = 2 * (1 - stats.norm.cdf(abs(z_statistic)))

    # Generate null means by independently flipping each return's sign.
    rng = np.random.default_rng(SEED)
    sign_flips = rng.choice([-1, 1], size=(B, n))
    permutation_means = (sign_flips * returns).mean(axis=1)
    p_permutation = (
        1 + np.count_nonzero(np.abs(permutation_means) >= abs(mean))
    ) / (B + 1)

    # Store both tests with their respective rejection decisions.
    results = pd.DataFrame(
        [
            {
                "test": "Wald z-test",
                "n": n,
                "mean": mean,
                "SD": sample_sd,
                "SE": standard_error,
                "z": z_statistic,
                "p_wald": p_wald,
                "p_permutation": p_permutation,
                "reject_H0_at_5pct": p_wald < ALPHA,
                "B": B,
                "seed": SEED,
            },
            {
                "test": "Sign-flip permutation test",
                "n": n,
                "mean": mean,
                "SD": sample_sd,
                "SE": standard_error,
                "z": z_statistic,
                "p_wald": p_wald,
                "p_permutation": p_permutation,
                "reject_H0_at_5pct": p_permutation < ALPHA,
                "B": B,
                "seed": SEED,
            },
        ]
    )

    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    table_path = TABLE_DIR / "method2_hypothesis_test.csv"
    permutation_figure_path = (
        FIGURE_DIR / "method2_permutation_distribution.png"
    )
    returns_figure_path = FIGURE_DIR / "method2_returns_vs_normal.png"
    results.to_csv(table_path, index=False)

    # Plot the sign-flip null distribution and the observed two-sided cutoffs.
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(
        permutation_means,
        bins=50,
        density=True,
        alpha=0.65,
        color="steelblue",
        edgecolor="white",
        label="Sign-flip permutation means",
    )
    ax.axvline(
        mean,
        color="crimson",
        linewidth=1.8,
        label="Observed mean and two-sided cutoffs",
    )
    ax.axvline(-mean, color="crimson", linewidth=1.8)
    ax.set_xlabel("Sign-flip mean daily log return (%)")
    ax.set_ylabel("Density")
    ax.set_title("Sign-Flip Permutation Distribution of Mean Daily Log Return")
    ax.legend()
    fig.tight_layout()
    fig.savefig(permutation_figure_path, dpi=150)
    plt.close(fig)

    # Compare the return density with a normal curve fitted to its mean and SD.
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(
        returns,
        bins=50,
        density=True,
        alpha=0.65,
        color="steelblue",
        edgecolor="white",
        label="Daily log returns",
    )
    x_values = np.linspace(returns.min(), returns.max(), 500)
    ax.plot(
        x_values,
        stats.norm.pdf(x_values, loc=mean, scale=sample_sd),
        color="darkorange",
        linewidth=2,
        label="Fitted normal curve",
    )
    ax.set_xlabel("Daily log return (%)")
    ax.set_ylabel("Density")
    ax.set_title("Daily Log Returns Compared with a Fitted Normal Distribution")
    ax.legend()
    fig.tight_layout()
    fig.savefig(returns_figure_path, dpi=150)
    plt.close(fig)

    # Summarize distribution shape, test results, and output locations.
    skewness = stats.skew(returns)
    excess_kurtosis = stats.kurtosis(returns)
    print(results.to_string(index=False))
    print(f"\nSkewness: {skewness:.6f}")
    print(f"Excess kurtosis: {excess_kurtosis:.6f}")
    print(
        "\nInterpretation: "
        f"the estimated mean daily log return is {mean:.6f}%, "
        f"with a Wald z statistic of {z_statistic:.6f} "
        f"(two-sided p-value {p_wald:.6g}) and a sign-flip permutation "
        f"p-value of {p_permutation:.6g}. "
        f"At the 5% significance level, the Wald test "
        f"{'rejects' if p_wald < ALPHA else 'does not reject'} H0 and the "
        f"permutation test "
        f"{'rejects' if p_permutation < ALPHA else 'does not reject'} H0; "
        "the evidence "
        f"{'supports' if p_wald < ALPHA and p_permutation < ALPHA else 'does not support'} "
        "a non-zero mean daily return."
    )
    print(f"\nSaved table to: {table_path}")
    print(f"Saved permutation figure to: {permutation_figure_path}")
    print(f"Saved returns figure to: {returns_figure_path}")


if __name__ == "__main__":
    main()
