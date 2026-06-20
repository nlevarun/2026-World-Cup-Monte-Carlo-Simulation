import pandas as pd
from simulator import WorldCupSimulator


# Load your match probability dataset

matches = pd.read_csv("matches.csv")

# Safety check

for col in ["p_home_win", "p_draw", "p_away_win"]:

    if col not in matches.columns:
        raise ValueError(f"Missing column: {col}")

# Normalize probabilities

prob_sum = (
    matches["p_home_win"]
    + matches["p_draw"]
    + matches["p_away_win"]
)

matches["p_home_win"] /= prob_sum
matches["p_draw"] /= prob_sum
matches["p_away_win"] /= prob_sum

sim = WorldCupSimulator(matches)

results = sim.run_simulations(
    n=100
)

print("\nWORLD CUP WIN PROBABILITIES\n")
print(results.head(20))

results.to_csv(
    "world_cup_forecast.csv",
    index=False
)

print("\nSaved to world_cup_forecast.csv")