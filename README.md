# ds607-usd-sgd-fx-project

DS607 Group Project: Statistical Analysis of Daily USD/SGD Exchange Rate Dynamics

## 1. Executive Summary and Research Question

### Research Question

"Does the daily log return of the USD/SGD exchange rate exhibit a statistically significant non-zero mean drift, and how do parametric CLT/Wald frameworks compare with non-parametric Bootstrap and Permutation inference in quantifying exchange rate location and uncertainty?"

### Motivation

As a trade-dependent small open economy, Singapore utilizes the Singapore Dollar Nominal Effective Exchange Rate (S$NEER) policy band managed by the Monetary Authority of Singapore (MAS) as its primary monetary policy tool. Testing whether the daily USD/SGD return has a non-zero drift is crucial for currency risk management and evaluating market efficiency under MAS's exchange rate regime.

## 2. Data Description and Ethics

- **Data Source:** NBER (National Bureau of Economic Research)
- **Sample Window:** 2021-09-27 to 2026-09-25 (1,305 dated rows in the raw file; 55 have no exchange-rate value, leaving 1,250 valid rates and 1,249 daily log returns)
- **Target Variable:** Daily Log Returns ($r_t = \ln(S_t / S_{t-1}) \times 100\%$)
- **Data Ethics:** Fully open public dataset. Raw data files are placed in `data/raw/` (git-ignored).

---

## 3. Statistical Methodology

This project evaluates two core course methods on the 1,249 daily log return observations:

### Method 1: Location and Uncertainty (CLT vs. Non-Parametric Bootstrap 95% CIs)

- **Parametric CLT (Wald):**
  $$\bar{r} = \frac{1}{N}\sum r_t, \quad \hat{\text{se}}(\bar{r}) = \frac{S_N}{\sqrt{N}}, \quad \text{CI}_{\text{CLT}} = \bar{r} \pm 1.96 \cdot \hat{\text{se}}(\bar{r})$$
- **Non-Parametric Percentile Bootstrap:** Resample $B = 10{,}000$ samples of size $N$ with replacement from $\{r_t\}$. The standard error is the sample standard deviation of the bootstrap means, and the $95\%$ percentile confidence interval is given by their 2.5th and 97.5th percentiles.
- **Non-Parametric Studentized Bootstrap:** For each resample, calculate $t^* = (\bar{r}^* - \bar{r}) / \widehat{\mathrm{se}}^*$, where $\widehat{\mathrm{se}}^*$ is that resample's standard error. The interval is $[\bar{r} - q_{0.975}(t^*)\widehat{\mathrm{se}}(\bar{r}),\; \bar{r} - q_{0.025}(t^*)\widehat{\mathrm{se}}(\bar{r})]$.

#### Method 1 implementation and results

The script saves the comparison table to `outputs/tables/method1_location_uncertainty.csv` and the bootstrap-mean histogram to `outputs/figures/method1_bootstrap_mean_distribution.png`. The histogram marks the CLT/Wald, percentile-bootstrap, and studentized-bootstrap interval endpoints with distinct line styles and colors.

For the $N = 1{,}249$ daily log returns, the estimated mean is $-0.004664\%$. The CLT/Wald standard error is $0.008242\%$, compared with the bootstrap standard error of $0.008196\%$. The CLT/Wald 95% CI is $[-0.020819\%, 0.011491\%]$ (width $0.032310$ percentage points); the percentile-bootstrap 95% CI is $[-0.020702\%, 0.011136\%]$ (width $0.031838$ percentage points); and the studentized-bootstrap 95% CI is $[-0.020769\%, 0.011241\%]$ (width $0.032010$ percentage points). The three intervals are very similar and all include zero. This interval comparison is consistent with uncertainty around a mean close to zero; it is not a replacement for the formal zero-drift tests in Method 2.

### Method 2: Hypothesis Testing for Zero Drift (Wald $z$-Test vs. Permutation Test)

- **Hypotheses:** $H_0: \mu = 0$ (No daily drift) vs. $H_1: \mu \neq 0$
- **Parametric Wald Test:**
  $$z = \frac{\bar{r} - 0}{\hat{\text{se}}(\bar{r})}, \quad p_{\text{CLT}} = 2\left(1 - \Phi(|z|)\right)$$
- **Sign-Flip Permutation Test:** Under $H_0$, the returns are symmetric around zero, so independently multiply each return $r_t$ by a random $+1$ or $-1$ and calculate the mean for each of $B = 10{,}000$ sign-flip samples. The two-sided p-value uses the observed mean and a $+1$ protection term:
  $$p_{\text{perm}} = \frac{1 + \sum_{b=1}^{B} \mathbf{1}(|\bar{r}^{*(b)}| \ge |\bar{r}|)}{B + 1}$$

#### Method 2 implementation and results

The script saves the test table to `outputs/tables/method2_hypothesis_test.csv`, the sign-flip permutation distribution to `outputs/figures/method2_permutation_distribution.png`, and the return-density comparison to `outputs/figures/method2_returns_vs_normal.png`. For the $N = 1{,}249$ daily log returns, the Wald z statistic is $-0.565826$, with a two-sided Wald p-value of $0.571512$ and a sign-flip permutation p-value of $0.570343$. At the 5% significance level, both tests fail to reject $H_0$, so the results do not support a non-zero mean daily return.

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
├── notebooks/                  # Analysis notebooks and exploratory work
├── src/                        # Source scripts for data handling and inference
├── outputs/
│   ├── figures/                 # Visualization outputs
│   ├── tables/                  # Summary tables and model results
│   └── presentation/            # Presentation materials and deck exports
└── .gitignore                  # Repository ignore rules
```

### Dependencies

The project dependencies are managed in `requirements.txt` and include the core packages required for data cleaning, inference, and visualization:

- `pandas>=2.0.0`
- `numpy>=1.24.0`
- `scipy>=1.10.0`
- `matplotlib>=3.7.0`
- `statsmodels>=0.14.0`
- `yfinance>=0.2.0`

Install them via:

```bash
pip install -r requirements.txt
```

### Reproducibility

- All random sampling algorithms enforce a fixed random seed (`RNG = np.random.default_rng(60702)`).
- Project scripts and analysis can be run after installing the dependencies above.

---

## 5. Summary of Results ($N = 1,249$)

### Key Takeaway

---

## 6. Limitations

1. **Independence Assumption:** Daily FX returns exhibit ARCH/GARCH volatility clustering. Block Bootstrap could be used in future work to handle autocorrelation.
2. **Policy Regimes:** The 2021–2026 window includes Fed rate hikes and MAS policy tightening; sub-period analysis can further verify regime stability.

---

## 7. AI Usage and Contributions

- **AI Usage:** Generative AI, primarily Gemini, was used as a coding assistant and writing support tool for code refinement, debugging, and documentation formatting.
- **Human Verification:** All core statistical methods, empirical logic, hypothesis testing decisions, and final interpretations were designed, reviewed, and verified by the team.
- **Contribution Statement:** This project reflects the team’s own analysis and judgment; AI was used as an assistive tool rather than a substitute for methodological reasoning.