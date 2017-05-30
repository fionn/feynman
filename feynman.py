#!/usr/bin/env python3

from itertools import combinations_with_replacement as combine
import random
from particles import Particle, particles_list

PARTICLES = particles_list()


def vertex_conservation(particles):
    # return list of things which should be invariant across this vertex
    
    lepton_number = sum([p.lepton for p in particles])
    charge = sum([p.charge for p in particles])

    return [charge, lepton_number]


def vertex_outputs(p_in, constraints, n_out):
    # get the outputs from a vertex subject to
    #   * no trivial verts: output != input
    #	* keep invariants invariant
    #   * return n_out particles, if possible

    pairs = combine(PARTICLES, n_out)
    allowed_pairs = []

    for p in pairs:
        if ((vertex_conservation(p) == constraints) and 
            (set(p_names(p)) != set(p_names(p_in)))):
           
             allowed_pairs.append(p)

    return allowed_pairs if len(allowed_pairs) > 0 else None


def make_diagram(p_in, n_vertices, structure):
    # make diagram given input particles,
    # the number of vertices expected &
    # the number of particles we want out at each vertex (randomly chosen)

    p_out = [p_in]

    p = p_in
    for i, n in enumerate(structure):
        
        constraint = vertex_conservation(p)
        allowed_pairs = vertex_outputs(p, constraint, n)
        p = random.choice(allowed_pairs) 
        p_out.append(p)

    return p_out 


def p_names(particles):
    # return a list of names

    return [p.name for p in particles]


if __name__ == "__main__":

    particles = ["electron", "positron"]
    particles = tuple([Particle(p) for p in particles])    


    vertices = 2 # no. of vertices
    structure = [1, 2] # no of particles output from each vertex

    diagram = make_diagram(particles, vertices, structure)
    for i, v in enumerate(diagram):
        print('Vertex {}:'.format(i))
        print(p_names(v))

