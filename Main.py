import math
from itertools import combinations

# Complex version of the simple balancer
# This version includes role assignment
# Balance using Rank Value, Role Rank Variance, Team rank variance, On role count difference

# Define players_data with their ranks and preferred roles
# Rank 1: Iron, Rank 2: Bronze, Rank 3: Silver, Rank 4: Gold, Rank 5: Platinum,
# Rank 6: Emerald, Rank 7: Diamond, Rank 8: Master, Rank 9: Grandmaster, Rank 10: Challenger
players_data = [
    {"name": "SirMightyBacon", "rank": 8, "role": "Mid"},
    {"name": "Z3Sleeper", "rank": 8, "role": "Top"},
    {"name": "Meyst", "rank": 5, "role": "Fill"},
    {"name": "Wazzaii", "rank": 3, "role": "Adc"},
    {"name": "Classiq", "rank": 7, "role": "Fill"},
    {"name": "Silvia", "rank": 3, "role": "Top"},
    {"name": "KingNeptun3", "rank": 3, "role": "Top"},
    {"name": "Shrektangle", "rank": 9, "role": "Fill"},
    {"name": "Kyupo", "rank": 2, "role": "Support"},
    {"name": "Settupss", "rank": 7, "role": "Support"},
    {"name": "Evelynn Toes", "rank": 6, "role": "Jungle"},
    {"name": "Tiny Cena", "rank": 3, "role": "Support"},
    {"name": "Ramza", "rank": 8, "role": "Fill"},
    {"name": "Zotto", "rank": 9, "role": "Jungle"},
    {"name": "Gourish", "rank": 9, "role": "Fill"},
    {"name": "Wallaby", "rank": 6, "role": "Mid"},
    {"name": "Flames", "rank": 5, "role": "Support"}
]

# Define current players
players = [
    "SirMightyBacon", "Z3Sleeper", "Meyst", "KingNeptun3", "Gourish",
    "Kyupo", "Wallaby", "Shrektangle", "Ramza", "Settupss"
]

current_players_data = []


def get_player_by_name(name):
    return next((player for player in players_data if player['name'] == name), None)


def get_players_data():
    global current_players_data
    current_players_data = [get_player_by_name(player) for player in players]
    if None in current_players_data:
        print(f"Player {players[current_players_data.index(None)]} not found in players_data.")
        current_players_data = [player for player in current_players_data if player is not None]


# Calculate the rank value for a player
def calculate_rank_value(rank):
    base_value = 1  # Base value for the lowest rank
    max_value = 100  # Maximum cap for the highest rank
    steepness = 0.8  # Adjust this value to control how fast the curve flattens
    midpoint = 5  # Midpoint rank where the curve starts to flatten

    # Using a sigmoid function for smooth diminishing growth
    return base_value + (max_value - base_value) / (1 + math.exp(-steepness * (rank - midpoint)))


# This function calculates the total rank value for a team
def calculate_team_rank_value(team):
    return sum(calculate_rank_value(player['rank']) for player in team)


def assign_roles(team):
    roles = ['Top', 'Jungle', 'Mid', 'Adc', 'Support']
    assigned_roles = {role: None for role in roles}
    unassigned_players = []

    # First, assign players to their preferred roles if available
    for player in team:
        if player['role'] in roles and assigned_roles[player['role']] is None:
            assigned_roles[player['role']] = player
        else:
            unassigned_players.append(player)

    # Then, assign remaining players to open roles or as Fill
    for player in unassigned_players:
        if player['role'] == 'Fill':
            # Assign to first available role
            for role in roles:
                if assigned_roles[role] is None:
                    assigned_roles[role] = player
                    break
        else:
            # Try to find an open role
            for role in roles:
                if assigned_roles[role] is None:
                    assigned_roles[role] = player
                    break

    return assigned_roles


# Calculates how many players are in their preferred role (or Fill)
def calculate_on_role_factor(team_roles):
    on_role_count = sum(1 for role, player in team_roles.items() if player['role'] == role or player['role'] == 'Fill')
    return on_role_count / len(team_roles)


# Calculates the rank variance for a team (how spread out the ranks are)
def calculate_team_rank_variance(team):
    ranks = [player['rank'] for player in team]
    avg_rank = sum(ranks) / len(ranks)
    rank_variance = sum((rank - avg_rank) ** 2 for rank in ranks) / len(ranks)
    return rank_variance


# Calculate the role-specific rank variance between the two teams
def calculate_role_rank_variance(team1_roles, team2_roles):
    return sum(abs(calculate_rank_value(team1_roles[role]['rank']) - calculate_rank_value(team2_roles[role]['rank']))
               for role in team1_roles.keys())


# Balance teams based on rank value, team rank variance role, and team composition
def balance_teams(current_players, previous_teams):
    best_combination = None
    min_score = float('inf')

    for team1 in combinations(current_players, 5):
        team2 = [p for p in current_players if p not in team1]

        # Skip if this combination has been used before
        if (tuple(sorted(p['name'] for p in team1)), tuple(sorted(p['name'] for p in team2))) in previous_teams:
            continue

        # Assign roles to both teams
        team1_roles = assign_roles(team1)
        team2_roles = assign_roles(team2)

        # Calculate rank value difference
        team1_rank_value = calculate_team_rank_value(team1)
        team2_rank_value = calculate_team_rank_value(team2)
        teams_rank_value = abs(team1_rank_value - team2_rank_value)

        # Calculate team rank variance
        team1_rank_variance = calculate_team_rank_variance(team1)
        team2_rank_variance = calculate_team_rank_variance(team2)
        teams_rank_variance = abs(team1_rank_variance - team2_rank_variance)

        # Calculate role-specific rank differences
        role_rank_variance = calculate_role_rank_variance(team1_roles, team2_roles)

        # Calculate on-role count difference
        team1_on_role = calculate_on_role_factor(team1_roles)
        team2_on_role = calculate_on_role_factor(team2_roles)
        on_role_diff = abs(team1_on_role - team2_on_role)

        # Calculate the overall balance score (lower is better)
        balance_score = (teams_rank_value * 0.4 +
                         role_rank_variance * 0.2 +
                         teams_rank_variance * 0.2 +
                         on_role_diff * 0.2)

        if balance_score < min_score:
            min_score = balance_score
            best_combination = (team1, team2, team1_roles, team2_roles, min_score)

    return best_combination


def print_team(roles, team_number):
    print(f"Team {team_number}:")
    total_rank_value = 0
    for role, player in roles.items():
        rank_value = calculate_rank_value(player['rank'])
        total_rank_value += rank_value
        print(
            f"  {role}: {player['name']} (Rank: {player['rank']}, Preferred: {player['role']})") # Value: {rank_value:.2f}
    print(f"  Total Rank Value: {total_rank_value:.2f}")


def main():
    get_players_data()
    previous_teams = set()
    while True:
        # Get a new team combination that hasn't been used before
        result = balance_teams(current_players_data, previous_teams)
        if not result:
            print("No more unique combinations available.")
            break

        team1, team2, team1_roles, team2_roles, min_score = result
        print_team(team1_roles, 1)
        print_team(team2_roles, 2)
        #print(f"  Balance Score: {min_score:.2f}")
        # Add current teams to previous_teams set
        previous_teams.add((tuple(sorted(p['name'] for p in team1)), tuple(sorted(p['name'] for p in team2))))

        print("Press Enter to generate next most balanced teams or 'Q' to quit.")
        user_input = input()
        if user_input.lower() == 'q':
            break


if __name__ == "__main__":
    main()
