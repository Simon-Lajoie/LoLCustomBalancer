from itertools import combinations

# Simple version of the balancer
# Balance using Rank Value and uses on role count difference as a tiebreaker

# Define players_data with their ranks and preferred roles
# Rank 1: Iron, Rank 2: Bronze, Rank 3: Silver, Rank 4: Gold, Rank 5: Platinum,
# Rank 6: Emerald, Rank 7: Diamond, Rank 8: Master, Rank 9: Grandmaster, Rank 10: Challenger
players_data = [
    {"name": "SirMightyBacon", "rank": 8, "role": "Mid"},
    {"name": "Z3Sleeper", "rank": 8, "role": "Top"},
    {"name": "Meyst", "rank": 5, "role": "Fill"},
    {"name": "Wazzaii", "rank": 4, "role": "Adc"},
    {"name": "Classiq", "rank": 7, "role": "Fill"},
    {"name": "Silvia", "rank": 5, "role": "Top"},
    {"name": "Kingneptun3", "rank": 3, "role": "Top"},
    {"name": "Shrektangle", "rank": 9, "role": "Fill"},
    {"name": "Kyupo", "rank": 2, "role": "Support"},
    {"name": "Settupss", "rank": 7, "role": "Support"},
    {"name": "Evelynn Toes", "rank": 6, "role": "Jungle"},
    {"name": "Tiny Cena", "rank": 3, "role": "Support"},
    {"name": "Ramza", "rank": 8, "role": "Fill"},
    {"name": "Zotto", "rank": 9, "role": "Jungle"},
    {"name": "Gourish", "rank": 9, "role": "Fill"},
    {"name": "Wallaby", "rank": 7, "role": "Mid"},
    {"name": "Flames", "rank": 5, "role": "Support"},
    {"name": "Maa San", "rank": 5, "role": "Support"},
    {"name": "Cleenslate", "rank": 4, "role": "Mid"},
    {"name": "Nasir", "rank": 8, "role": "Fill"},
    {"name": "Limi", "rank": 6, "role": "Mid"},
    {"name": "Oogli", "rank": 7, "role": "Mid"},
    {"name": "Drzoan", "rank": 7, "role": "Support"},
    {"name": "Slimelvl1", "rank": 6, "role": "Support"},
    {"name": "Rogier", "rank": 7, "role": "Support"},
    {"name": "I SETT YOU UP", "rank": 6, "role": "Top"},
    {"name": "Aimishi", "rank": 6, "role": "Jungle"},
    {"name": "Sehnbon", "rank": 5, "role": "Top"},
    {"name": "Smoking Hookah", "rank": 6, "role": "Fill"},
    {"name": "Mnesia", "rank": 5, "role": "Jungle"},
    {"name": "Aimishi", "rank": 6, "role": "Fill"},
    {"name": "Nappy", "rank": 9, "role": "Top"},
    {"name": "Untuchable", "rank": 5, "role": "Adc"},
    {"name": "Kyupo", "rank": 2, "role": "Support"},
    {"name": "Silva b", "rank": 2, "role": "Support"},
    {"name": "Feenz", "rank": 4, "role": "Adc"},
    {"name": "NotJustPlatonic", "rank": 7, "role": "Fill"},
    {"name": "Gabyumi", "rank": 3, "role": "Support"},
    {"name": "GumGumBlast", "rank": 2, "role": "Adc"},
    {"name": "Tsaritsa", "rank": 2, "role": "Support"},
    {"name": "Vroom", "rank": 6, "role": "Top"},
    {"name": "SkrtSkrt", "rank": 4, "role": "Support"}
]

# Define current players
players = [
    "SirMightyBacon", "Tsaritsa", "Wazzaii", "Settupss", "Vroom",
    "Shrektangle", "Smoking Hookah", "Ramza", "SkrtSkrt", "Wallaby"
]

current_players_data = []


def get_player_by_name(name):
    for player in players_data:
        if player['name'] == name:
            return player
    return None


def get_players_data_data():
    for player in players:
        player_to_add = get_player_by_name(player)
        if player_to_add is not None:
            current_players_data.append(player_to_add)
        else:
            print(f"Player {player} not found in players_data.")


# Calculate the total rank value for a team
def calculate_team_score(team):
    return sum(player['rank']**2 for player in team)


# Calculate the raw total rank value for a team
def calculate_team_raw_score(team):
    return sum(player['rank'] for player in team)


def count_on_roles(team):
    roles = [player['role'] for player in team]

    on_roles_count = 0
    seen_roles = set()

    for role in roles:
        if role == "Fill":
            on_roles_count += 1
        elif role not in seen_roles:
            seen_roles.add(role)
            on_roles_count += 1

    return min(on_roles_count, 5)


def balance_teams(previous_teams):
    best_combination = None
    min_rank_difference = float('inf')
    max_total_on_roles = 0

    for team1 in combinations(current_players_data, 5):
        team2 = [p for p in current_players_data if p not in team1]

        # Create sorted tuples of player names to compare combinations
        sorted_team1 = tuple(sorted(p['name'] for p in team1))
        sorted_team2 = tuple(sorted(p['name'] for p in team2))

        # Skip if this combination of teams has already been generated
        if (sorted_team1, sorted_team2) in previous_teams or (sorted_team2, sorted_team1) in previous_teams:
            continue

        # Calculate the rank difference between the two teams
        rank_difference = abs(calculate_team_score(team1) - calculate_team_score(team2))
        on_roles_team1 = count_on_roles(team1)
        on_roles_team2 = count_on_roles(team2)

        # Calculate the total on roles for the two teams
        total_on_roles = on_roles_team1 + on_roles_team2

        # Prioritize rank balance, then maximize on roles for both teams
        if rank_difference < min_rank_difference or (
                rank_difference == min_rank_difference and total_on_roles > max_total_on_roles):
            min_rank_difference = rank_difference
            max_total_on_roles = total_on_roles
            best_combination = (team1, team2)

    return best_combination


def print_team(team, team_number):
    print(f"Team {team_number}:")
    for player in team:
        print(f"  {player['name']} (Rank: {player['rank']}, Role: {player['role']})")
    print(f"  On Roles: {count_on_roles(team)}")
    print(f"  Team Score: {calculate_team_raw_score(team)}")
    print()


def main():
    previous_teams = set()
    get_players_data_data()
    while True:
        # Get a new team combination that hasn't been used before
        teams = balance_teams(previous_teams)
        if not teams:
            print("No more unique combinations available.")
            break

        team1, team2 = teams
        print_team(team1, 1)
        print_team(team2, 2)

        # Add current teams to previous_teams set
        previous_teams.add((tuple(sorted(p['name'] for p in team1)), tuple(sorted(p['name'] for p in team2))))

        print("Press any Key to generate new teams or 'Q' to quit.")
        user_input = input()
        if user_input.lower() == 'q':
            break


if __name__ == "__main__":
    main()
