# World Cup Monte Carlo Simulation

## Overview

This project is a probabilistic World Cup forecasting model that uses Monte Carlo simulation to estimate the likelihood of each team winning the tournament. It simulates full tournaments repeatedly using match-level probabilities and aggregates outcomes to produce final win probabilities.

## How the Model Works

### Match Simulation
Each match outcome is randomly sampled based on precomputed probabilities:
- Home win probability
- Draw probability
- Away win probability

These probabilities can be derived from Elo ratings or other team strength metrics.

### Group Stage Simulation
- Teams are divided into groups based on the input dataset
- Each match in the group stage is simulated once per tournament iteration
- Points are assigned using standard football rules:
  - Win: 3 points
  - Draw: 1 point
  - Loss: 0 points
- Teams are ranked by points, with Elo rating used as a tiebreaker
- Top two teams from each group advance

### Knockout Stage Simulation
- Qualified teams are randomly shuffled into a bracket
- Each match is simulated using Elo-based win probabilities
- The tournament progresses until a single champion remains

### Monte Carlo Simulation
The full tournament is simulated N times (e.g., 1,000 to 100,000 iterations). The final output is the proportion of simulations each team wins, interpreted as their championship probability.

## Output

The model produces a ranked table of teams with estimated win probabilities. For example:

Team | Win Probability
-----|----------------
Spain | 0.30
France | 0.16
Argentina | 0.13
Germany | 0.12
Brazil | 0.09

## Project Structure

simulator.py – core simulation engine  
run_forecast.py – execution script  
matches.csv – input dataset containing match probabilities and Elo ratings  
requirements.txt – dependencies  
.gitignore – ignored files configuration  
README.md – project documentation  

## Assumptions

- Match outcomes are independent conditional on probabilities
- Elo ratings approximate team strength
- Knockout bracket is randomly assigned
- No in-tournament team strength updates are applied

## Limitations

- Knockout structure is not based on the official FIFA bracket
- No dynamic updates for injuries or form
- Static probabilities per match
- No calibration from historical match data

## Future Improvements

- Implement official FIFA knockout bracket structure
- Update Elo ratings dynamically after each match
- Calibrate probabilities using historical datasets
- Add visualization dashboard (e.g., Streamlit)
- Parallelize Monte Carlo simulation for performance gains
