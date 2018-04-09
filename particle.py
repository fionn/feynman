#!/usr/bin/env python3

from collections import namedtuple
from abc import ABC, abstractmethod

class Particle(ABC):

    Position = namedtuple("Position", ["t", "x", "y", "z"])
    Momentum = namedtuple("Momentum", ["t", "x", "y", "z"])

    def __init__(self):
        self.name = None
        self.symbol = None
        self.charge = None
        self.spin = None
        self.mass = None
        self.baryon = None
        self.lepton = None
        # The default is for particles to be their own antiparticle
        self.antiparticle = self.__class__
        #self.parity = None
        #self.c_parity = None

    def __repr__(self):
        return self.__class__.__name__

    @abstractmethod
    def _instantiated(self):
        # This prevents base classes from accidental
        # initialisation
        pass

    # Not sure what to do here, or if we care.
    #@abstractmethod
    def position(self, frame):
        pass

    #@abstractmethod
    def momentum(self, frame):
        pass

class Antiparticle(Particle):

    # TODO: some particle names & symbols can be fixed here

    def _antiparticle(self):
        self.charge *= -1
        self.lepton *= -1
        self.baryon *= -1
        self.antiparticle = self.__class__.__bases__[0]

class GaugeBoson(Particle):

    def __init__(self):
        super().__init__()
        self.spin = 1
        self.baryon = 0
        self.lepton = 0

class Photon(GaugeBoson):

    def __init__(self):
        super().__init__()
        self.name = "photon"
        self.symbol = "γ"
        self.charge = 0
        self.mass = 0
        self.parity = -1
        self.c_parity = - 1

    def _instantiated(self):
        pass

class Z(GaugeBoson):

    def __init__(self):
        super().__init__()
        self.name = "Z"
        self.symbol = "Z^0"
        self.charge = 0
        self.mass = 91.19 # GeV

    def _instantiated(self):
        pass

class WPlus(GaugeBoson):

    def __init__(self):
        super().__init__()
        self.name = "W^+"
        self.symbol = self.name
        self.charge = 1
        self.mass = 80.39
        self.antiparticle = WMinus

    def _instantiated(self):
        pass

class WMinus(GaugeBoson):

    def __init__(self):
        super().__init__()
        self.name = "W^-"
        self.symbol = self.name
        self.charge = -1
        self.mass = 80.39
        self.antiparticle = WPlus

    def _instantiated(self):
        pass

class Fermion(Particle):

    def __init__(self):
        super().__init__()
        self.spin = 0.5

class Lepton(Fermion):

    def __init__(self):
        super().__init__()
        self.baryon = 0
        self.lepton = 1

    @abstractmethod
    def neutrino(self):
        pass

class Electron(Lepton):

    def __init__(self):
        super().__init__()
        self.name = "electron"
        self.symbol = "e^-"
        self.charge = -1
        self.mass = 0.51
        self.antiparticle = Positron

    @property
    def neutrino(self):
        return ElectronNeutrino

    def _instantiated(self):
        pass

class Positron(Electron, Antiparticle):

    def __init__(self):
        super().__init__()
        self.name = "positron"
        self.symbol = "e^+"
        self._antiparticle()

    def _instantiated(self):
        pass

class Muon(Lepton):

    def __init__(self):
        super().__init__()
        self.name = "muon"
        self.symbol = "µ^-"
        self.charge = -1
        self.mass = 0.51
        self.antiparticle = AntiMuon

    @property
    def neutrino(self):
        return MuonNeutrino

    def _instantiated(self):
        pass

class AntiMuon(Muon, Antiparticle):

    def __init__(self):
        super().__init__()
        self.name = "antimuon"
        self.symbol = "µ^+"
        self._antiparticle()

    def _instantiated(self):
        pass

class Neutrino(Lepton):

    def __init__(self, flavour):
        super().__init__()
        self.name = flavour.name + " neutrino"
        self.symbol = "ν_" + flavour.symbol[0]
        self.lepton = flavour.lepton
        self.masss = 0
        self.charge = 0

    @property
    def neutrino(self):
        # Neutrinos don't have neutrinos
        raise AttributeError

class ElectronNeutrino(Neutrino):

    def __init__(self):
        super().__init__(Electron())
        self.antiparticle = ElectronAntiNeutrino

    def _instantiated(self):
        pass

class ElectronAntiNeutrino(Neutrino, Antiparticle):

    def __init__(self):
        super().__init__(Electron())
        self.name = "electron antinutrino"
        # TODO: overbar
        self.symbol = "bar " + self.symbol
        self._antiparticle()

    def _instantiated(self):
        pass

class MuonNeutrino(Neutrino):

    def __init__(self):
        super().__init__(Muon())
        self.antiparticle = MuonAntiNeutrino

    def _instantiated(self):
        pass

class MuonAntiNeutrino(Neutrino, Antiparticle):

    def __init__(self):
        super().__init__(Muon())
        self.name = "muon antinutrino"
        # TODO: overbar
        self.symbol = "bar " + self.symbol
        self._antiparticle()

    def _instantiated(self):
        pass

class Factory:

    _boson_map = {"photon": Photon,
                  "Z": Z,
                  "W^+": WPlus,
                  "W^-": WMinus,
                 }

    _fermion_map = {"electron": Electron,
                    "positron": Positron,
                    "muon": Muon,
                    "antimuon": AntiMuon,
                    "electron neutrino": ElectronNeutrino,
                    "electron antineutrino": ElectronAntiNeutrino,
                    "muon neutrino": MuonNeutrino,
                    "muon antineutrino": MuonAntiNeutrino,
                   }

    _particle_map = {**_boson_map, **_fermion_map}
    particle_instances = {key: value() for key, value in _particle_map.items()}

    @staticmethod
    def create(name):
        try:
            return Factory._particle_map[name]
        except KeyError:
            raise NotImplementedError("{}s don't exist yet".format(name))

if __name__ == "__main__":

    e = Electron()
    print(isinstance(e.antiparticle(), Positron))

