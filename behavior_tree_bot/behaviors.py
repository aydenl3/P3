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

def calculate_min_troops_for_neutral(state,home_planet,neutral_planet):
    troops_needed = neutral_planet.num_ships + 1
    return troops_needed
    