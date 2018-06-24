#!/usr/bin/env python3

import random
from collections import namedtuple
from typing import Tuple
from itertools import combinations_with_replacement as combine
import particle

class InteractionError(RuntimeError):
    pass

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

    def _legal_vertex(self, t: tuple) -> None:
        if self._vertex_invariants(t) != self._invariants:
            raise InteractionError("{} != {} for {}"
                                   .format(self._vertex_invariants(t),
                                           self._invariants, t))
        if self._violates_landau_yang(t):
            raise InteractionError("{} violates Landau-Yang".format(t))
        # TODO: pair production/annihilation

    def _vertex_outputs(self, number_of_outputs: int = 2) -> list:
        """
        get the outputs from a vertex subject to:
        * no trivial vertices: output != input,
        * keep invariants invariant,
        * return required number of particles.
        """
        particle_instances = [x() for x in particle.PARTICLES]
        tuples = combine(particle_instances, number_of_outputs)
        allowed_tuples = []
        for t in tuples:
            try:
                self._legal_vertex(t)
                allowed_tuples.append(t)
            except InteractionError:
                pass

        if allowed_tuples:
            return allowed_tuples

        raise InteractionError("{} can't generate {} legal outputs"
                               .format([t for t in tuples], number_of_outputs))

    def make_diagram(self) -> list:
        vertex_particles = [self._particles]
        for n_out in self._structure:
            allowed_tuples = self._vertex_outputs(n_out)
            vertex_particles.append(random.choice(allowed_tuples))
            self._out = vertex_particles[-1]

        self._vertex_particles = vertex_particles # type: ignore
        return vertex_particles

    def make_tex(self):
        if not self._vertex_particles:
            self.make_diagram()
        raise NotImplementedError

if __name__ == "__main__":
    particles = (particle.Electron(), particle.Positron())
    structure = [1, 2] # number of particles output from each vertex

    interaction = Interaction(particles, structure)
    diagram = interaction.make_diagram()
    for i, vertex in enumerate(diagram):
        print('Vertex {}: {}'.format(i, [p.symbol for p in vertex]))

