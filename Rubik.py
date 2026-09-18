from Algorithms import *
import random

class Rubik(Problem):
    """
    Rubic state representation:
        - state is a tuple of length 54 (up, down, left, right, front, back) (u, d, l, r, f, b)
        - each face is length 9
        - colors are represented by the digits 1->6
        - allowable moves are clockwise and counter clockwise for each face

    Example:
    solved = (1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6)
             (u,u,u,u,u,u,u,u,u,d,d,d,d,d,d,d,d,d,l,l,l,l,l,l,l,l,l,r,r,r,r,r,r,r,r,r,f,f,f,f,f,f,f,f,f,b,b,b,b,b,b,b,b,b)
             (1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9)

    """
    # moves:    Dictionary that defines the name of the move based on the face that is rotated
    #           and a list with 2 tuples that correspond to the source and destination indexes
    #           that are swapped during that face rotation.  Reversing source and dest is the
    #           opposite rotation.  Upper case means clockwise and lower case means counter.
    moves = { 'U':[ ( 0, 1, 2, 3, 5, 6, 7, 8,18,19,20,27,28,29,36,37,38,45,46,47),
                    ( 6, 3, 0, 7, 1, 8, 5, 2,36,37,38,45,46,47,27,28,29,18,19,20) ],
              'D':[ ( 9,10,11,12,14,15,16,17,24,25,26,33,34,35,42,43,44,51,52,53),
                    (15,12, 9,16,10,17,14,11,51,52,53,42,43,44,24,25,26,33,34,35) ],
              'L':[ (18,19,20,21,23,24,25,26, 0, 3, 6, 9,12,15,36,39,42,47,50,53),
                    (24,21,18,25,19,26,23,20,53,50,47,36,39,42, 0, 3, 6,15,12, 9) ],
              'R':[ (27,28,29,30,32,33,34,35, 2, 5, 8,11,14,17,38,41,44,45,48,51),
                    (33,30,27,34,28,35,32,29,38,41,44,51,48,45,11,14,17, 8, 5, 2) ],
              'F':[ (36,37,38,39,41,42,43,44, 6, 7, 8, 9,10,11,20,23,26,27,30,33),
                    (42,39,36,43,37,44,41,38,26,23,20,33,30,27, 9,10,11, 6, 7, 8) ],
              'B':[ (45,46,47,48,50,51,52,53, 0, 1, 2,15,16,17,18,21,24,29,32,35),
                    (51,48,45,52,46,53,50,47,29,32,35,18,21,24, 2, 1, 0,17,16,15) ], }

    def __init__(self, start, goal):
        super().__init__(start)
        self.goal = goal

    def is_goal(self, state):
        return state == self.goal

    def next_states(self, state):
        result = []

        for face in self.moves.keys():
            result.append( (face, self.apply_move(state, face, True)) )
            result.append( (face.lower(), self.apply_move(state, face, False)) )

        return result

    def apply_move( self, state, face, clockwise ):
        destinations, sources = self.moves[face]

        new_state = list(state)

        for dest, src in zip(destinations, sources):
            if clockwise:
                new_state[dest] = state[src]
            else:
                new_state[src] = state[dest]

        return tuple(new_state)

    def test(self, state):

        result = []

        print("begin test")

        for key, val in self.moves.items():
            print( key, self.apply_move(state, key, True) )

        return result



if __name__ == "__main__":
    start = (1,1,1,1,1,1,1,1,1,
             2,2,2,2,2,2,2,2,2,
             3,3,3,3,3,3,3,3,3,
             4,4,4,4,4,4,4,4,4,
             5,5,5,5,5,5,5,5,5,
             6,6,6,6,6,6,6,6,6)
    goal = start

    cube = Rubik(start, goal)
    state = start

    choices = list(cube.moves.keys())
    old_choice = 'R'
    for i in range(7):
        while True:
            random_choice = random.choice(choices) 
            if random_choice != old_choice:
                break
        old_choice = random_choice
        state = cube.apply_move(state, random_choice, bool(random.getrandbits(1)) )

    problem = Rubik(state, goal)

    #problem.test(state)

    #print("\nDFS")
    #dfs(problem)

    #print("\nBFS")
    #bfs(problem)

    print("\nIDDFS")
    iddfs(problem)
