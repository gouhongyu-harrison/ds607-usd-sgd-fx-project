"""Compare CLT/Wald and percentile-bootstrap CIs for mean USD/SGD returns."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "DEXSIUS_cleaned.csv"
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURE_DIR = PROJECT_ROOT / "outputs" / "figures"

B = 10_000
SEED = 60702
Z_975 = 1.96


def main() -> None:
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

    n = returns.size
    mean = returns.mean()
    sample_sd = returns.std(ddof=1)
    standard_error = sample_sd / np.sqrt(n)

    clt_lower = mean - Z_975 * standard_error
    clt_upper = mean + Z_975 * standard_error

    rng = np.random.default_rng(SEED)
    bootstrap_samples = rng.choice(returns, size=(B, n), replace=True)
    bootstrap_means = bootstrap_samples.mean(axis=1)
    bootstrap_se = bootstrap_means.std(ddof=1)
    bootstrap_lower, bootstrap_upper = np.quantile(
        bootstrap_means, [0.025, 0.975]
    )
    bootstrap_sample_sds = bootstrap_samples.std(axis=1, ddof=1)
    bootstrap_sample_ses = bootstrap_sample_sds / np.sqrt(n)
    studentized_statistics = (bootstrap_means - mean) / bootstrap_sample_ses
    studentized_q025, studentized_q975 = np.quantile(
        studentized_statistics, [0.025, 0.975]
    )
    studentized_lower = mean - studentized_q975 * standard_error
    studentized_upper = mean - studentized_q025 * standard_error
    clt_width = clt_upper - clt_lower
    bootstrap_width = bootstrap_upper - bootstrap_lower
    studentized_width = studentized_upper - studentized_lower

    results = pd.DataFrame(
        [
            {
                "n": n,
                "mean_estimate_pct": mean,
                "sample_sd_pct": sample_sd,
                "se_clt_pct": standard_error,
                "se_bootstrap_pct": bootstrap_se,
                "clt_ci_lower_pct": clt_lower,
                "clt_ci_upper_pct": clt_upper,
                "clt_ci_width_pct": clt_width,
                "clt_ci_includes_zero": clt_lower <= 0 <= clt_upper,
                "bootstrap_ci_lower_pct": bootstrap_lower,
                "bootstrap_ci_upper_pct": bootstrap_upper,
                "bootstrap_ci_width_pct": bootstrap_width,
                "bootstrap_ci_includes_zero": bootstrap_lower <= 0 <= bootstrap_upper,
                "studentized_ci_lower_pct": studentized_lower,
                "studentized_ci_upper_pct": studentized_upper,
                "studentized_ci_width_pct": studentized_width,
                "studentized_ci_includes_zero": (
                    studentized_lower <= 0 <= studentized_upper
                ),
                "bootstrap_replicates": B,
                "random_seed": SEED,
            },
        ]
    )

    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    table_path = TABLE_DIR / "method1_location_uncertainty.csv"
    figure_path = FIGURE_DIR / "method1_bootstrap_mean_distribution.png"
    results.to_csv(table_path, index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(
        bootstrap_means,
        bins=50,
        density=True,
        alpha=0.65,
        color="steelblue",
        edgecolor="white",
        label="Bootstrap means",
    )
    ax.axvline(mean, color="black", linewidth=1.5, label="Sample mean")
    ax.axvline(
        clt_lower,
        color="darkorange",
        linestyle="--",
        linewidth=1.5,
        label="CLT/Wald 95% CI endpoints",
    )
    ax.axvline(clt_upper, color="darkorange", linestyle="--", linewidth=1.5)
    ax.axvline(
        bootstrap_lower,
        color="crimson",
        linestyle=":",
        linewidth=1.8,
        label="Bootstrap percentile 95% CI endpoints",
    )
    ax.axvline(bootstrap_upper, color="crimson", linestyle=":", linewidth=1.8)
    ax.axvline(
        studentized_lower,
        color="forestgreen",
        linestyle="-.",
        linewidth=1.5,
        label="Studentized bootstrap 95% CI endpoints",
    )
    ax.axvline(studentized_upper, color="forestgreen", linestyle="-.", linewidth=1.5)
    ax.set_xlabel("Bootstrap replicate mean daily log return (%)")
    ax.set_ylabel("Density")
    ax.set_title("Bootstrap Distribution of Mean Daily Log Return")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figure_path, dpi=150)
    plt.close(fig)

    print(results.to_string(index=False))
    print(
        "\nInterpretation: "
        f"the Bootstrap SE is {bootstrap_se:.6f}% versus "
        f"{standard_error:.6f}% for CLT/Wald; "
        f"the Bootstrap CI width is {bootstrap_width:.6f}% versus "
        f"{clt_width:.6f}% for CLT/Wald. "
        f"The studentized Bootstrap CI width is {studentized_width:.6f}%. "
        f"All three intervals include zero: "
        f"{clt_lower <= 0 <= clt_upper and bootstrap_lower <= 0 <= bootstrap_upper and studentized_lower <= 0 <= studentized_upper}."
    )
    print(f"\nSaved table to: {table_path}")
    print(f"Saved figure to: {figure_path}")


if __name__ == "__main__":
    main()
