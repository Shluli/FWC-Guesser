# World Cup EV Model

A probabilistic expected-value engine that played a 104-match World Cup prediction pool for me — fetching live odds, modeling every match, and submitting the optimal bet. It won first place by a wide margin winning 800₪ first prize on a 100₪ investment.

## What it does

For every match, the Google Sheets engine:

1. **Fetches live odds** from Pinnacle sportsbook using the football-odds-api extention for google sheets.
2. **Converts the odds into expected goals** for each team, de-vigging the market first.
3. **Builds a Poisson distribution** over every possible final scoreline.
4. **Submits the highest-EV bet** for the pool's scoring system — the scoreline that maximizes expected points across all markets, which is almost allways not the most likely score because of how the scoring system works.

It also prices a high-value "crazy bet" each match:

- **Comeback wins** — estimated with a **Monte Carlo simulation** I wrote in Apps Script (Type script), since a comeback depends on the sequence of goals, not just the final score.
- **Hattricks** — derived from anytime-goalscorer odds, converted to player-level rates and run through Poisson.

## Calibration

Over 80 tracked matches I logged predicted EV vs. actual points. and for an avarage match the model would benefit on 0.59+ points above the EV, which was 0.12 standard deviations off, basiclly nothing, showing the accuracy of the model.

for he final, my dad was worried I might lose, so I ran a **2-million-simulation Monte Carlo** in PY of the final to put my probability of winning the league at **99.85% before kickoff** to calm my dad down.

## Tech

Google Sheets (engine) · Google Apps Script (Monte Carlo, odds fetching) · Python (calibration + final simulation)
