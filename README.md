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
- **Non-Parametric Percentile Bootstrap:** Resample $B = 10{,}000$ times with replacement from $\{r_t\}$ to derive empirical $95\%$ percentile confidence limits $[\bar{r}^{*(250)}, \bar{r}^{*(9750)}]$.

### Method 2: Hypothesis Testing for Zero Drift (Wald $z$-Test vs. Permutation Test)

- **Hypotheses:** $H_0: \mu = 0$ (No daily drift) vs. $H_1: \mu \neq 0$
- **Parametric Wald Test:**
  $$z = \frac{\bar{r} - 0}{\hat{\text{se}}(\bar{r})}, \quad p_{\text{CLT}} = 2\left(1 - \Phi(|z|)\right)$$
- **Null-Centered Permutation Test:** Shift data under $H_0$ ($r_t^0 = r_t - \bar{r}$), resample $B = 10{,}000$ times, and compute p-value with a $+1$ protection term:
  $$p_{\text{perm}} = \frac{1 + \sum_{b=1}^{B} \mathbf{1}(|\bar{r}^{*(b)}| \ge |\bar{r}|)}{B + 1}$$

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