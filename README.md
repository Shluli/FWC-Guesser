# World Cup EV Model

A probabilistic expected-value engine that played a 104-match World Cup prediction pool for me and won first place and money — fetching live odds, modeling every match, and submitting the optimal bet. It won first place by a wide margin, taking the 800₪ first prize on a 100₪ investment.

## What it does

For every match, the Google Sheets engine:

1. Fetches live odds from Pinnacle sportsbook using the football-odds-api extension for Google Sheets.
2. Converts the odds into expected goals for each team, de-vigging the market first (removing the bookmaker's margin).
3. Builds a Poisson distribution over every possible final scoreline.
4. Submits the highest-EV bet for the pool's scoring system — the scoreline that maximizes expected points across all markets, which is almost always *not* the most likely score, because of how the scoring system works.

It also prices a high-value "crazy bet" each match:

* **Comeback wins** — estimated with a Monte Carlo simulation I wrote in Apps Script, since a comeback depends on the sequence of goals, not just the final score.
* **Hat-tricks** — derived from anytime-goalscorer odds, converted to player-level rates and run through Poisson.

## Results

Over 80 tracked matches I logged predicted EV against actual points scored. The model outperformed its own expectation by roughly 0.59 points per match — partly a high-scoring World Cup, partly real edges the model found in the market — validating the approach over a meaningful sample.

Before the final, my dad was worried I might lose, so I ran a 2-million-simulation Monte Carlo of the final in Python and put my probability of winning the league at 99.85% before kickoff — mostly to calm him down.

## Tech

Google Sheets (engine) · Google Apps Script (Monte Carlo, odds fetching) · Python (final simulation)
