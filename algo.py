'''
    Class that holds the algorithm to move to the exit
    of the map
'''
class Algorithm :

    def __init__(self, map, display=False):

        self.map = map

    start(self) :

        self.result = self.simulate()
        return self.result

    simulate(self) : 