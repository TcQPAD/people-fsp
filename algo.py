

'''
    Class that holds the algorithm to move to the exit
    of the map
'''
class Algorithm :

    def __init__(self, peopleNumber, map, display=False):

        self.map = map

    start(self) :

        self.result = self.simulate()
        return self.result

    
    '''
        Simulates the movement of 
        2^peopleNumber persons to the upper left corner
        of the map.
    '''
    simulate(self) :    