import numpy as np
import pandas as pd


class WorldCupSimulator:

    def __init__(self, matches_df):
        self.matches = matches_df
        self.default_elo = float(
            pd.concat([
                self.matches["home_elo"],
                self.matches["away_elo"]
            ]).dropna().mean()
        )

    # -----------------------
    # Simulate one match
    # -----------------------
    def simulate_match(self, row):

        outcome = np.random.choice(
            ["home", "draw", "away"],
            p=[
                row["p_home_win"],
                row["p_draw"],
                row["p_away_win"]
            ]
        )

        return outcome

    # -----------------------
    # Simulate one group
    # -----------------------
    def simulate_group(self, group_df):

        teams = set(group_df["home_team"]).union(
            set(group_df["away_team"])
        )

        standings = {
            team: {
                "points": 0,
                "elo": 0
            }
            for team in teams
        }

        # store average elo for tiebreaks
        for _, row in group_df.iterrows():

            standings[row["home_team"]]["elo"] = row["home_elo"]
            standings[row["away_team"]]["elo"] = row["away_elo"]

        for _, row in group_df.iterrows():

            result = self.simulate_match(row)

            home = row["home_team"]
            away = row["away_team"]

            if result == "home":
                standings[home]["points"] += 3

            elif result == "away":
                standings[away]["points"] += 3

            else:
                standings[home]["points"] += 1
                standings[away]["points"] += 1

        ranking = sorted(
            standings.items(),
            key=lambda x: (
                x[1]["points"],
                x[1]["elo"]
            ),
            reverse=True
        )

        return ranking[0][0], ranking[1][0]

    # -----------------------
    # Knockout game
    # -----------------------
    def simulate_knockout_match(self, team1, team2):

        elo1 = team1["elo"]
        elo2 = team2["elo"]

        expected1 = 1 / (1 + 10 ** ((elo2 - elo1) / 400))

        winner = np.random.choice(
            [team1["name"], team2["name"]],
            p=[expected1, 1 - expected1]
        )

        return winner

    # -----------------------
    # Get Elo lookup
    # -----------------------
    def build_elo_lookup(self):

        elo = {}

        for _, row in self.matches.iterrows():

            if pd.notna(row["home_elo"]):
                elo[row["home_team"]] = row["home_elo"]

            if pd.notna(row["away_elo"]):
                elo[row["away_team"]] = row["away_elo"]

        return elo

    # -----------------------
    # Resolve team Elo
    # -----------------------
    def get_team_elo(self, team_name, elo_lookup):

        elo = elo_lookup.get(team_name)

        if pd.isna(elo):
            return self.default_elo

        return elo

    # -----------------------
    # Simulate entire tournament
    # -----------------------
    def simulate_tournament(self):

        elo_lookup = self.build_elo_lookup()

        groups = {}

        for group_name, group_df in self.matches.groupby("group"):

            winner, runner_up = self.simulate_group(group_df)

            groups[group_name] = {
                "winner": winner,
                "runner_up": runner_up
            }

        # ------------------------------------------------
        # Placeholder knockout bracket
        #
        # You MUST replace this with FIFA's official
        # 2026 Round of 32 bracket.
        # ------------------------------------------------

        qualified = []

        for g in sorted(groups.keys()):

            qualified.append(groups[g]["winner"])
            qualified.append(groups[g]["runner_up"])

        # random bracket for now

        np.random.shuffle(qualified)

        current_round = qualified

        while len(current_round) > 1:

            next_round = []

            for i in range(0, len(current_round) - 1, 2):

                team1 = current_round[i]
                team2 = current_round[i + 1]

                winner = self.simulate_knockout_match(
                    {
                        "name": team1,
                        "elo": self.get_team_elo(team1, elo_lookup)
                    },
                    {
                        "name": team2,
                        "elo": self.get_team_elo(team2, elo_lookup)
                    }
                )

                next_round.append(winner)

            if len(current_round) % 2 == 1:

                next_round.append(current_round[-1])

            current_round = next_round

        champion = current_round[0]

        return champion

    # -----------------------
    # Monte Carlo
    # -----------------------
    def run_simulations(self, n=1000):

        winners = {}

        for _ in range(n):

            champion = self.simulate_tournament()

            winners[champion] = winners.get(champion, 0) + 1

        results = pd.DataFrame(
            [
                [team, count / n]
                for team, count in winners.items()
            ],
            columns=["team", "win_probability"]
        )

        return results.sort_values(
            "win_probability",
            ascending=False
        )