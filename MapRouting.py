from Algorithms import *

class CityPathProblem(Problem):

    """
    State: a city name (string), e.g., "Toronto"
    Action: (next_city, distance_km)
    next_states returns (action, next_state) where:
      - action is the distance (int) so students see "cost" as the action label
      - next_state is the neighbor city (string)
    """

    def __init__(self, graph, start_city, goal_city):
        super().__init__(start_city)
        self.graph = graph
        self.goal_city = goal_city

    def is_goal(self, state):
        return state == self.goal_city

    def next_states(self, state):
        neighbors = self.graph.get(state, {})
        # action = distance, next_state = neighbor city
        return [(distance, neighbor) for neighbor, distance in neighbors.items()]

graph = {
"Toronto":{"Vaughan":25,"Mississauga":29,"Markham":33,"Brampton":35,"Oakville":40},
"Hamilton":{"Burlington":15,"Oakville":45,"Cambridge":55,"Mississauga":55,"Guelph":60},
"Mississauga":{"Brampton":20,"Oakville":22,"Toronto":29,"Milton":33,"Burlington":35},
"Brampton":{"Mississauga":20,"Vaughan":24,"Milton":33,"Toronto":35,"Oakville":42},
"Vaughan":{"Markham":22,"Brampton":24,"Toronto":25,"Mississauga":48,"Oakville":55},
"Markham":{"Vaughan":22,"Toronto":33,"Oshawa":55,"Brampton":55,"Mississauga":70},
"Oshawa":{"Markham":55,"Toronto":60,"Vaughan":80,"Brampton":97,"Mississauga":95},
"Barrie":{"Vaughan":90,"Brampton":95,"Markham":100,"Toronto":105,"Oshawa":150},
"Oakville":{"Burlington":20,"Mississauga":22,"Milton":25,"Toronto":40,"Brampton":42},
"Burlington":{"Hamilton":15,"Oakville":20,"Mississauga":35,"Milton":35,"Toronto":55},
"Milton":{"Oakville":25,"Mississauga":33,"Brampton":33,"Burlington":35,"Guelph":35},
"Guelph":{"Cambridge":24,"Kitchener":26,"Waterloo":27,"Milton":35,"Hamilton":60},
"Kitchener":{"Waterloo":5,"Cambridge":22,"Guelph":26,"Milton":55,"Hamilton":75},
"Waterloo":{"Kitchener":5,"Cambridge":25,"Guelph":27,"Milton":60,"Hamilton":80},
"Cambridge":{"Kitchener":22,"Guelph":24,"Waterloo":25,"Milton":50,"Hamilton":55}
}



p = CityPathProblem(graph, start_city="Oshawa", goal_city="Guelph")

print("\nBFS")
bfs(p)

print("\nDFS")
dfs(p)

print("\nIDDFS")
iddfs(p)