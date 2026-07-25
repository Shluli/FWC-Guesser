"""
World Cup Final — Title Probability Monte Carlo
================================================

Before the final I had a huge lead, but there was still one way I could lose, if Mbappe would lose the golden ball race I lose 63 points, and if Spain wins the world
cup, my rival gets 63 points as we both bet on those pre turnament... for me to lose there was one cenerio, Messi passes mbappe for the boot and still looses the final.
So I ran a 2 million matches simulation using Pinnacles odds for messi to either score or assist in the final to see exactly what my odds were. The model put it at 99.85%.

Model:
  - Each team's goals ~ Poisson(team_xG) over regulation.
  - If tied after 90', extra time adds Poisson(team_xG / 3) (30 min = 1/3 of a match).
  - If still tied, a penalty shootout is a 50/50 coin flip (shootout goals do NOT
    count toward the Golden Boot).
  - Goals/assists are attributed to the star player by his share of team output,
    derived from his individual xG/xA vs the team xG.

Dagger scenarios counted (any of these + Argentina losing => I lose the league):
  - Messi scores 3+  (passes Mbappe's 10 outright)
  - Messi scores exactly 2 AND assists 1+ (ties on goals, wins the assist tiebreaker)
"""

import random
import math

random.seed(42)
SIMS = 2_000_000

# --- Inputs (from de-vigged market odds) ---
ARG_XG = 2.23      # Argentina expected goals (regulation)
SPA_XG = 1.34      # Spain expected goals (regulation)

MESSI_XG = 0.55    # Messi individual xG
MESSI_XA = 0.29    # Messi individual xA
OYA_XG   = 0.55    # Oyarzabal xG (checked for completeness; on 5 goals he can't catch Mbappe)
OYA_XA   = 0.29

# Star player's share of team output
messi_goal_share   = MESSI_XG / ARG_XG
messi_assist_share = MESSI_XA / ARG_XG
oya_goal_share     = OYA_XG / SPA_XG
oya_assist_share   = OYA_XA / SPA_XG


def poisson(lam):
    """Draw a Poisson sample via Knuth's algorithm."""
    L = math.exp(-lam)
    k, p = 0, 1.0
    while True:
        k += 1
        p *= random.random()
        if p <= L:
            return k - 1


def attribute(goals, goal_share, assist_share):
    """Given a team's goal count, attribute goals scored and assisted to the star.
    Each goal is either scored by the star (goal_share), or — among the rest —
    possibly assisted by him."""
    scored = assisted = 0
    for _ in range(goals):
        if random.random() < goal_share:
            scored += 1
        elif random.random() < assist_share / (1 - goal_share):
            assisted += 1
    return scored, assisted


def simulate():
    messi_hat_lost = messi_ba_lost = messi_passes_lost = 0
    oya_six = oya_five_three = 0
    arg_wins = spa_wins = 0

    for _ in range(SIMS):
        arg, spa = poisson(ARG_XG), poisson(SPA_XG)
        m_sc, m_as = attribute(arg, messi_goal_share, messi_assist_share)
        o_sc, o_as = attribute(spa, oya_goal_share, oya_assist_share)

        # Extra time if level after 90
        if arg == spa:
            ae, se = poisson(ARG_XG / 3), poisson(SPA_XG / 3)
            m2, ma2 = attribute(ae, messi_goal_share, messi_assist_share)
            o2, oa2 = attribute(se, oya_goal_share, oya_assist_share)
            arg += ae; spa += se
            m_sc += m2; m_as += ma2
            o_sc += o2; o_as += oa2

        # Decide winner (shootout = 50/50)
        if arg > spa:
            arg_won = True
        elif spa > arg:
            arg_won = False
        else:
            arg_won = random.random() < 0.5

        arg_wins += arg_won
        spa_wins += not arg_won
        argentina_lost = not arg_won

        # Boot-dagger conditions (both pass Mbappe's 10)
        hat = m_sc >= 3
        brace_assist = (m_sc == 2 and m_as >= 1)
        if hat and argentina_lost:
            messi_hat_lost += 1
        if brace_assist and argentina_lost:
            messi_ba_lost += 1
        if (hat or brace_assist) and argentina_lost:
            messi_passes_lost += 1

        # Oyarzabal (for completeness — needs 6 goals to reach 11)
        if o_sc >= 6:
            oya_six += 1
        if o_sc >= 5 and o_as >= 3:
            oya_five_three += 1

    pct = lambda x: x / SIMS * 100
    print(f"Simulations: {SIMS:,}   (ARG xG {ARG_XG}, SPA xG {SPA_XG})")
    print(f"Argentina wins cup: {pct(arg_wins):.2f}%")
    print(f"Spain wins cup:     {pct(spa_wins):.2f}%\n")
    print("Boot dagger (star passes Mbappe AND Argentina loses):")
    print(f"  Messi 3+ AND lost:          {pct(messi_hat_lost):.4f}%")
    print(f"  Messi 2 + assist AND lost:  {pct(messi_ba_lost):.4f}%")
    print(f"  COMBINED (I lose league):   {pct(messi_passes_lost):.4f}%\n")
    print(f"Oyarzabal 6+ goals:           {pct(oya_six):.5f}%")
    print(f"Oyarzabal 5 goals + 3 assists:{pct(oya_five_three):.5f}%\n")
    print(f">>> PROBABILITY OF WINNING THE LEAGUE: {100 - pct(messi_passes_lost):.4f}% <<<")


if __name__ == "__main__":
    simulate()
