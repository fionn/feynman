#!/usr/bin/env python3

from itertools import combinations_with_replacement as combine
import random
import particle

PARTICLE_MAP = particle.Factory.particle_map

# TODO: This is hard to reason about. Let's rewrite and have something  like a
#       Vertex class that contains conservation laws, etc.
#       It's also broken -- sorry.

def vertex_conservation(particles):
    """returns a list of values invariant across this vertex"""
    lepton_number = sum([p.lepton for p in particles])
    charge = sum([p.charge for p in particles])
    return [charge, lepton_number]

def vertex_outputs(p_in, constraints, n_out):
    """
    get the outputs from a vertex subject to:
    * no trivial verts: output != input
    * keep invariants invariant
    * return n_out particles, if possible
    """
    pairs = combine(PARTICLE_MAP.values(), n_out)
    allowed_pairs = []

    for particle in pairs:
        print(particle)
        if ((vertex_conservation(p) == constraints) and
            (set(p_names(p)) != set(p_names(p_in)))):
             allowed_pairs.append(p)

    if len(allowed_pairs) > 0:
        return allowed_pairs

def make_diagram(p_in, n_vertices, structure):
    """
    make diagram given input particles,
    the number of vertices expected &
    the number of particles we want out at each vertex (randomly chosen)
    """
    p_out = [p_in]
    p = p_in
    for i, n in enumerate(structure):
        constraint = vertex_conservation(p)
        allowed_pairs = vertex_outputs(p, constraint, n)
        p = random.choice(allowed_pairs)
        p_out.append(p)

    return p_out

def class_list():
    """Misleading, this returns all particle classes"""
    particle_list = []
    for attr in dir(particle):
        x = getattr(particle, attr)
        if isinstance(x, type):
            particle_list.append(x)
    return particle_list

if __name__ == "__main__":
    particles = (particle.Electron(), particle.Positron())
    print(particles)

    vertices = 2 # no. of vertices
    structure = [1, 2] # no of particles output from each vertex

    diagram = make_diagram(particles, vertices, structure)
    #for i, v in enumerate(diagram):
    #    print('Vertex {}:'.format(i))
    #    print(p_names(v))
