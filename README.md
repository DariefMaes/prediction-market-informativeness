# When Do Prediction Markets Become Informative?

This project analyzes historical Kalshi prediction markets to measure **when markets become stably informative** prior to event resolution.

## Key Idea

Rather than asking whether prediction markets are correct at the end, we measure the **first time** each market’s implied probability crosses a confidence threshold in favor of the realized outcome and remains there.

## Methodology

- **Data source:** Kalshi public API
- **Markets:** settled binary markets
- **Informativeness:** A market is defined as informative at the first snapshot where its implied probability crosses a 0.55 confidence threshold in favor of the realized outcome and remains on that side thereafter
- **Snapshots:** 30d, 14d, 7d, 3d, 1d, 12h, 1h before resolution
- **Liquidity filter:** Markets below the 25th percentile of total traded volume are excluded to reduce noise from illiquid markets
- **30d availability:** All markets in the final sample are available at the earliest snapshot (30d), ensuring that category comparisons are not confounded by market listing times

## Result

Most markets only become informative close to resolution, with roughly half converging in the final hours. Informativeness varies substantially by category: markets related to **Financials** and **Crypto** tend to become informative earlier, while categories such as **Mentions** and **Climate** converge much later.

## Limitations

This approach treats each market independently and does not extend cleanly to mutually exclusive multi-outcome events. In addition, the analysis focuses exclusively on Kalshi markets and does not incorporate data from other prediction platforms such as Polymarket.

## Files

- `analysis.ipynb`: Main notebook
- `figures/`: Generated plots
- `get-events.py`: Script for fetching historical event metadata from the Kalshi API.
- `get-markets.py`: Script for fetching market-level data and historical prices from the Kalshi API.

## How to Reproduce

1. Run `get-events.py` to fetch the full set of historical events (≈10,000) used in the analysis.
2. Run `get-markets.py` to retrieve market data for each event, selecting the highest-volume market per event.
3. Open `analysis.ipynb` and execute the notebook using the generated JSON files as inputs.
