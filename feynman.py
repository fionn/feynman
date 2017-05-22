#!/usr/bin/env python3

from itertools import combinations_with_replacement as combine
import random

class Particle():

    def __init__(self, particle):
        self.name = particle
        self.charge = self._charge(particle)
        self.lepton = self._lepton(particle)
        self.statistics = self._statistics(particle)

    def _charge(self, particle):
        charge_dict = {'electron': -1, 'positron': 1, 'photon': 0}
        return charge_dict[particle]


    def _lepton(self, particle):
        lepton_dict = {'electron': 1, 'positron': -1, 'photon': 0}
        return lepton_dict[particle]


    def _statistics(self, particle):
        stat_dict = {'electron': 'fermion',
                     'positron': 'fermion', 
                     'photon': 'boson'}
        return stat_dict[particle]


PARTICLES = (Particle('electron'), 
             Particle('positron'), 
             Particle('photon'))


def vertex_conservation(particles):
    lepton_number = sum([p.lepton for p in particles])
    charge = sum([p.charge for p in particles])

    return [charge, lepton_number]


def vertex_outputs(constraints, n_out):
    pairs = combine(PARTICLES, n_out)
    allowed_pairs = []

    for p in pairs:
        if vertex_conservation(p) == constraints:
            allowed_pairs.append(p)

    return allowed_pairs


if __name__ == "__main__":
    particles = ["electron", "positron"]
    particles = [Particle(p) for p in particles]

    vertices = 2
    p = particles
    print([j.name for j in p])
    for i in range(vertices):
        constraint = vertex_conservation(p)
        allowed_pairs = vertex_outputs(constraint, 2)
        p = random.choice(allowed_pairs)
        print([j.name for j in p])

    output = list(particles)

