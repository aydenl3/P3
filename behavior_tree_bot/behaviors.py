import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, calculate_troops_for_distance(state,strongest_planet,weakest_planet))


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def spread_to_closest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False
    
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (2) Find the closest enemy planet.
    closest_planet = state.enemy_planets().pop
    for planet in state.enemy_planets():
        if state.distance(strongest_planet.ID,planet.ID) < state.distance(strongest_planet.ID,closest_planet.ID):
            closest_planet = planet
    return issue_order(state, strongest_planet.ID, closest_planet.ID, calculate_troops_for_distance(state,strongest_planet, closest_planet))

def repell_neighbors_if_stronger(state):
    for planet in state.my_planets():
        if(state.enemy_planets()):
            close_planet = state.enemy_planets().pop()
        else:
            return False
        for enemy_planet in state.enemy_planets():
            if(state.distance(planet.ID,enemy_planet.ID) < state.distance(planet.ID, close_planet.ID)):
                close_planet = enemy_planet
        if(close_planet.num_ships * 1.5 < planet.num_ships):
            return issue_order(state,planet.ID,close_planet.ID,calculate_troops_for_distance(state,planet,close_planet))

#HELPER FUNCTIONS
def calculate_troops_for_distance(state,home_planet,enemy_planet):
     troops_needed = enemy_planet.num_ships + state.distance(home_planet.ID,enemy_planet.ID) * enemy_planet.growth_rate + 1
     return troops_needed

def calculate_min_troops_for_neutral(state, home_planet, neutral_planet):
    troops_needed = neutral_planet.num_ships + 1
    return troops_needed

# Kenny Implementation Below:

# HELPER FUNCTIONS

# Sort neutral planets by the minimum number of ships needed to capture it

def get_sorted_neutral_planets(state, source_planet):
        
    def min_troops_needed(target_planet):
        # Use min troops helper function
        return calculate_min_troops_for_neutral(state, source_planet, target_planet)

    return sorted(state.neutral_planets(), key=min_troops_needed)

# Sort enemy planets by enemy strength 

def get_sorted_enemy_planets(state):
    def enemy_strength(enemy_planet):
        return enemy_planet.num_ships

    return sorted(state.enemy_planets(), key=enemy_strength)

# Attacking Neutral Planets

def spread_to_multiple_neutral_planets(state):

    # Start by sorting through all available neutral planets
    for strongest_planet in state.my_planets():
        neutral_planets = get_sorted_neutral_planets(state, strongest_planet)

        for neutral_planet in neutral_planets:
            # Seek weak planets within a range to conquer them first 
            if state.distance(strongest_planet.ID, neutral_planet.ID) <= 50: 
                # Calculate amount of ships to send ONLY if we have enough
                ships_to_send = calculate_min_troops_for_neutral(state, strongest_planet, neutral_planet) + 1
                
                if ships_to_send < strongest_planet.num_ships:
                    issue_order(state, strongest_planet.ID, neutral_planet.ID, ships_to_send)
    return True

# Attacking Enemy 

def attack_weak_enemy_planets(state):
    
    # Attack the weak enemy planets first
    
    for strongest_planet in state.my_planets():
        enemy_planets = get_sorted_enemy_planets(state)

        for enemy_planet in enemy_planets:
            # Calculate distance from our strongest planet to enemy 
            distance = state.distance(strongest_planet.ID, enemy_planet.ID)
            # Use an educated estimate for sending ships to enemy planets
            ships_to_send = enemy_planet.num_ships + (2 * distance) + 10
            # Only send ships if we have enough 
            if ships_to_send < strongest_planet.num_ships:
                issue_order(state, strongest_planet.ID, enemy_planet.ID, ships_to_send)
    return True