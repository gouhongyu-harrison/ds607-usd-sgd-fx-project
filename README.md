# ds607-usd-sgd-fx-project

DS607 Group Project: Statistical Analysis of USD/SGD Exchange Rate Dynamics

This repository is DS607 group work for AY2026/27 August Term.

**Team members:** Gou Hongyu, Jiang Liuru, and Sun Jiayi.

## 1. Executive Summary and Research Question

### Research Question

Does the mean of the observed USD/SGD log returns differ from zero, and do CLT/Wald and resampling-based confidence intervals and tests lead to consistent conclusions?

### Motivation

As a trade-dependent small open economy, Singapore utilizes the Singapore Dollar Nominal Effective Exchange Rate (S$NEER) policy band managed by the Monetary Authority of Singapore (MAS) as its primary monetary policy tool. Testing whether the daily USD/SGD return has a non-zero drift is crucial for currency risk management and evaluating market efficiency under MAS's exchange rate regime.

## 2. Data Description and Ethics

- **Source:** NBER Macrohistory Database, series `DEXSIUS` ([database and access information](https://www.nber.org/research/data/nber-macrohistory-database)). The source workbook is included at `data/raw/DEXSIUS.xlsx`; the analysis-ready CSV is `data/processed/DEXSIUS_cleaned.csv`.
- **Sample window:** 2021-09-27 to 2026-09-25. The raw file contains 1,305 dated rows; 55 have no exchange-rate value. The processed file contains 1,250 valid exchange rates and 1,249 non-missing log returns.
- **Data dictionary:** `observation_date` is the observation date; `DEXSIUS` is the exchange-rate series as published by NBER; `log_return_pct` is $100\ln(S_t/S_{t-1})$. The first return is missing because there is no preceding observation.
- **Cleaning and access:** The source workbook and processed CSV are committed, so running the analyses does not require separate data access. The processed CSV is used directly by the scripts; the transformation from workbook to CSV is not included as a script and should be documented or added for full end-to-end reproducibility. Missing return values are excluded during analysis. Missing dates in the source mean some intervals may span more than one day, so not every return necessarily represents a one-calendar-day change.
- **Data ethics:** The repository contains the NBER source workbook and derived CSV. No SMU-licensed extract is used. Do not add licensed extracts, credentials, or `.env` files to a public repository.

---

## 3. Statistical Methodology

This project evaluates two course methods on the 1,249 available return observations. Both resampling procedures use 10,000 replicates and seed `60702`.

### Method 1: Location and Uncertainty (CLT vs. Non-Parametric Bootstrap 95% CIs)

- **Parametric CLT (Wald):**
  $$\bar{r} = \frac{1}{N}\sum r_t, \quad \hat{\text{se}}(\bar{r}) = \frac{S_N}{\sqrt{N}}, \quad \text{CI}_{\text{CLT}} = \bar{r} \pm 1.96 \cdot \hat{\text{se}}(\bar{r})$$
- **Non-Parametric Percentile Bootstrap:** Resample $B = 10{,}000$ samples of size $N$ with replacement from $\{r_t\}$. The standard error is the sample standard deviation of the bootstrap means, and the $95\%$ percentile confidence interval is given by their 2.5th and 97.5th percentiles.
- **Non-Parametric Studentized Bootstrap:** For each resample, calculate $t^* = (\bar{r}^* - \bar{r}) / \widehat{\mathrm{se}}^*$, where $\widehat{\mathrm{se}}^*$ is that resample's standard error. The interval is $[\bar{r} - q_{0.975}(t^*)\widehat{\mathrm{se}}(\bar{r}),\; \bar{r} - q_{0.025}(t^*)\widehat{\mathrm{se}}(\bar{r})]$.

#### Method 1 implementation and results

The script saves the comparison table to [method1_location_uncertainty.csv](outputs/tables/method1_location_uncertainty.csv) and the bootstrap-mean histogram to [method1_bootstrap_mean_distribution.png](outputs/figures/method1_bootstrap_mean_distribution.png). The histogram marks the CLT/Wald, percentile-bootstrap, and studentized-bootstrap interval endpoints with distinct line styles and colors.

For the $N = 1{,}249$ daily log returns, the estimated mean is $-0.004664\%$. The CLT/Wald standard error is $0.008242\%$, compared with the bootstrap standard error of $0.008196\%$. The CLT/Wald 95% CI is $[-0.020819\%, 0.011491\%]$ (width $0.032310$ percentage points); the percentile-bootstrap 95% CI is $[-0.020702\%, 0.011136\%]$ (width $0.031838$ percentage points); and the studentized-bootstrap 95% CI is $[-0.020769\%, 0.011241\%]$ (width $0.032010$ percentage points). The three intervals are very similar and all include zero. This interval comparison is consistent with uncertainty around a mean close to zero; it is not a replacement for the formal zero-drift tests in Method 2.

### Method 2: Hypothesis Testing for Zero Drift (Wald $z$-Test vs. Permutation Test)

- **Hypotheses:** $H_0: \mu = 0$ (No daily drift) vs. $H_1: \mu \neq 0$
- **Parametric Wald Test:**
  $$z = \frac{\bar{r} - 0}{\hat{\text{se}}(\bar{r})}, \quad p_{\text{CLT}} = 2\left(1 - \Phi(|z|)\right)$$
- **Sign-Flip Permutation Test:** Under $H_0$, the returns are symmetric around zero, so independently multiply each return $r_t$ by a random $+1$ or $-1$ and calculate the mean for each of $B = 10{,}000$ sign-flip samples. The two-sided p-value uses the observed mean and a $+1$ protection term:
  $$p_{\text{perm}} = \frac{1 + \sum_{b=1}^{B} \mathbf{1}(|\bar{r}^{*(b)}| \ge |\bar{r}|)}{B + 1}$$

#### Method 2 implementation and results

The script saves the test table to [method2_hypothesis_test.csv](outputs/tables/method2_hypothesis_test.csv), the sign-flip permutation distribution to [method2_permutation_distribution.png](outputs/figures/method2_permutation_distribution.png), and the return-density comparison to [method2_returns_vs_normal.png](outputs/figures/method2_returns_vs_normal.png). For $N = 1{,}249$, the Wald statistic is $-0.565826$ ($p=0.571512$), and the sign-flip permutation test gives $p=0.570343$. Both tests fail to reject $H_0$ at the 5% level; this is insufficient evidence of a non-zero mean, not proof that the mean is exactly zero.

---

## 4. Repository Structure and Reproducibility

```text
ds607-usd-sgd-fx-project/
├── README.md                    # Main project overview and documentation
├── AI_USAGE.md                  # Generative AI usage disclosure
├── CONTRIBUTIONS.md             # Team contribution summary
├── requirements.txt             # Python package dependencies
├── data/
│   ├── raw/                     # Raw NBER exchange-rate data
│   └── processed/               # Cleaned and processed datasets
├── src/                         # Analysis scripts
├── outputs/
│   ├── figures/                 # Visualization outputs
│   ├── tables/                  # Summary tables and model results
│   └── presentation/            # Required presentation PDF (not yet included)
└── .gitignore                  # Repository ignore rules
```

### Dependencies

The analysis dependencies and tested versions are pinned in `requirements.txt`.

Install dependencies and run both analyses from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/method1_location_uncertainty.py
python src/method2_hypothesis_test.py
```

Both scripts read the committed processed CSV using paths relative to the script and regenerate their tables and figures under `outputs/`. Bootstrap and permutation sampling use a fixed seed (`60702`) and 10,000 replicates.

---

## 5. Summary of Results ($N = 1,249$)

### Key Takeaway

The estimated mean return is $-0.004664\%$. All three 95% confidence intervals include zero: CLT/Wald $[-0.020819\%, 0.011491\%]$, percentile bootstrap $[-0.020702\%, 0.011136\%]$, and studentized bootstrap $[-0.020769\%, 0.011241\%]$. Their similar widths indicate that these methods give comparable uncertainty estimates for this sample.

The Wald and sign-flip tests also give similar, non-significant results ($p=0.571512$ and $p=0.570343$). At the 5% level we do not reject a zero mean. See the linked tables and figures above for the full estimates and distributions.

## 6. Limitations

1. **Observation intervals:** Missing values in the source series mean some retained observations may be more than one day apart. A dedicated cleaning script and interval-level sensitivity analysis would improve traceability.
2. **Inference assumptions:** The Wald standard error treats observations as independent; FX returns can exhibit serial dependence and volatility clustering. The sign-flip test additionally relies on symmetry under the null. A block bootstrap or dependence-robust analysis would be useful follow-up work.
3. **Policy regimes and sample window:** The 2021–2026 sample includes changing monetary-policy regimes; sub-period analysis could assess stability. Failure to reject the null does not establish that the true mean is zero.

---

## 7. Presentation

The DS607 guidelines require a presentation PDF in `outputs/presentation/`. That deck is not included in this repository snapshot and must be added before submission.

## 8. AI Usage and Contributions

- [AI_USAGE.md](AI_USAGE.md) documents the tools used and how outputs were checked.
- [CONTRIBUTIONS.md](CONTRIBUTIONS.md) lists each member's project contributions.