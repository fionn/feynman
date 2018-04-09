#!/usr/bin/env python3

import random
import abc
from collections import namedtuple
from typing import Tuple
from itertools import combinations_with_replacement as combine
import particle

PARTICLE_MAP = particle.Factory.particle_instances

class Interaction:

    def __init__(self, initial_particles: tuple, vertex_structure: list) -> None:
        self._particles = initial_particles
        self._out = initial_particles
        self._structure = vertex_structure
        self._invariants = self._vertex_invariants(particles)
        self._vertex_particles = None

    @staticmethod
    def _vertex_invariants(particles_in: tuple) -> Tuple[int, int]:
        Invariants = namedtuple("Invariants", ["charge", "lepton"])
        lepton_number = sum([p.lepton for p in particles_in])
        charge = sum([p.charge for p in particles_in])
        return Invariants(charge, lepton_number)

    def _violates_landau_yang(self, t: tuple) -> bool:
        if len(self._out) == 1 and len(t) == 2:
            if isinstance(self._out[0], particle.Z):
                if isinstance(t[0], particle.Photon) \
                   and isinstance(t[1], particle.Photon):
                    return True
        return False

    def _legal_vertex(self, t: tuple) -> bool:
        if self._vertex_invariants(t) != self._invariants:
            return False
        if self._violates_landau_yang(t):
            return False
        # TODO: pair production/annihilation
        return True

    def _vertex_outputs(self, number_of_outputs=2) -> list:
        """
        get the outputs from a vertex subject to:
        * no trivial vertices: output != input,
        * keep invariants invariant,
        * return required number of particles.
        """
        tuples = combine(PARTICLE_MAP.values(), number_of_outputs)
        allowed_tuples = []
        for t in tuples:
            if self._legal_vertex(t):
                allowed_tuples.append(t)

        if allowed_tuples:
            return allowed_tuples

        raise RuntimeError("{} can't generate {} legal outputs"
                           .format([t for t in tuples], number_of_outputs))

    def make_diagram(self) -> list:
        """
        make diagram given input particles,
        the number of vertices expected
        & the number of particles we want out at each vertex
        """
        vertex_particles = [self._particles]
        for n_out in self._structure:
            allowed_tuples = self._vertex_outputs(n_out)
            vertex_particles.append(random.choice(allowed_tuples))
            self._out = vertex_particles[-1]

        self._vertex_particles = vertex_particles
        return vertex_particles

    def make_tex(self):
        if not self._vertex_particles:
            self.make_diagram()
        raise NotImplementedError

def class_list():
    particle_list = []
    for attr in dir(particle):
        x = getattr(particle, attr)
        if isinstance(x, type):
            try:
                x()
                particle_list.append(x)
            except TypeError:
                continue
    particle_list.remove(abc.ABC)
    particle_list.remove(particle.Factory)
    return particle_list

if __name__ == "__main__":
    particles = (particle.Electron(), particle.Positron())
    structure = [1, 2] # number of particles output from each vertex

    interaction = Interaction(particles, structure)
    diagram = interaction.make_diagram()
    for i, vertex in enumerate(diagram):
        print('Vertex {}: {}'.format(i, [p.symbol for p in vertex]))

