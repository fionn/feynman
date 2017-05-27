class Particle():
    # particle class

    def __init__(self, particle=None):
        # particles are defined as a tuple of
        #   * name, charge, lepton number, statistic

        self.particle_definitions = [
            ('electron', -1, 1, 'fermion'),        
            ('positron', 1, -1, 'fermion'),        
            ('photon', 0, 0, 'boson'),        
            ('neutrino', 0, 1, 'fermion')]
    
        if particle != None: 
            self.name = particle
            i = [p[0] for p in self.particle_definitions].index(self.name) 

            self.charge = self.particle_definitions[i][1]
            self.lepton = self.particle_definitions[i][2]
            self.statistics = self.particle_definitions[i][3]


def particles_list():
    # helper function to instantiate a list of all particles

    P = Particle()
    particle_list = []
    for p in P.particle_definitions:

        Pi = Particle(p[0])

        particle_list.append(Pi)

    return particle_list

