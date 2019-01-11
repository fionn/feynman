#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Type

class Particle(ABC):

    def __init__(self) -> None:
        self.name: str = None   # type: ignore
        self.symbol: str = None # type: ignore
        self.charge: int = None # type: ignore
        self.spin: float = None # type: ignore
        self.mass: float = None # type: ignore
        self.baryon: int = None # type: ignore
        self.lepton: int = None # type: ignore
        self.tex = None
        # The default is for particles to be their own antiparticle
        self.antiparticle = self.__class__
        #self.parity = None
        #self.c_parity = None

    def __repr__(self) -> str:
        return self.__class__.__name__

    @staticmethod
    def overbar(string: str) -> str:
        overline = "\u0305"
        return overline.join(string) + overline

class Antiparticle(Particle):

    # TODO: some particle names & symbols can be fixed here

    def _antiparticle(self) -> None:
        self.charge *= -1
        self.lepton *= -1
        self.baryon *= -1
        self.antiparticle = self.__class__.__bases__[0]

class GaugeBoson(Particle):

    def __init__(self) -> None:
        super().__init__()
        self.spin = 1
        self.baryon = 0
        self.lepton = 0

class Photon(GaugeBoson):

    def __init__(self) -> None:
        super().__init__()
        self.name = "photon"
        self.symbol = "γ"
        self.charge = 0
        self.mass = 0
        #self.parity = -1
        #self.c_parity = - 1

class Z(GaugeBoson):

    def __init__(self) -> None:
        super().__init__()
        self.name = "Z"
        self.symbol = "Z^0"
        self.charge = 0
        self.mass = 91.19 # GeV

class WPlus(GaugeBoson):

    def __init__(self) -> None:
        super().__init__()
        self.name = "W^+"
        self.symbol = self.name
        self.charge = 1
        self.mass = 80.39
        self.antiparticle = WMinus

class WMinus(GaugeBoson):

    def __init__(self) -> None:
        super().__init__()
        self.name = "W^-"
        self.symbol = self.name
        self.charge = -1
        self.mass = 80.39
        self.antiparticle = WPlus

class Fermion(Particle):

    def __init__(self) -> None:
        super().__init__()
        self.spin = 0.5

class Lepton(Fermion):

    def __init__(self) -> None:
        super().__init__()
        self.baryon = 0
        self.lepton = 1

    @abstractmethod
    def neutrino(self) -> Type[Neutrino]:
        pass

class Neutrino(Lepton):

    def __init__(self, flavour: Lepton) -> None:
        super().__init__()
        self.name = flavour.name + " neutrino"
        self.symbol = "ν_" + flavour.symbol[0]
        self.lepton = flavour.lepton
        self.masss = 0
        self.charge = 0

    @property
    def neutrino(self) -> Type[Neutrino]:
        """Get the lepton's neutrino"""

class Electron(Lepton):

    def __init__(self) -> None:
        super().__init__()
        self.name = "electron"
        self.symbol = "e^-"
        self.charge = -1
        self.mass = 0.51
        self.antiparticle = Positron

    @property
    def neutrino(self) -> Type[Neutrino]:
        return ElectronNeutrino

class Positron(Electron, Antiparticle):

    def __init__(self) -> None:
        super().__init__()
        self.name = "positron"
        self.symbol = "e^+"
        self._antiparticle()

class Muon(Lepton):

    def __init__(self) -> None:
        super().__init__()
        self.name = "muon"
        self.symbol = "µ^-"
        self.charge = -1
        self.mass = 0.51
        self.antiparticle = AntiMuon

    @property
    def neutrino(self) -> Type[Neutrino]:
        return MuonNeutrino

class AntiMuon(Muon, Antiparticle):

    def __init__(self) -> None:
        super().__init__()
        self.name = "antimuon"
        self.symbol = "µ^+"
        self._antiparticle()

class ElectronNeutrino(Neutrino):

    def __init__(self) -> None:
        super().__init__(Electron())
        self.antiparticle = ElectronAntiNeutrino

class ElectronAntiNeutrino(Neutrino, Antiparticle):

    def __init__(self) -> None:
        super().__init__(Electron())
        self.name = "electron antinutrino"
        self.symbol = self.overbar(self.symbol)
        self._antiparticle()

class MuonNeutrino(Neutrino):

    def __init__(self) -> None:
        super().__init__(Muon())
        self.antiparticle = MuonAntiNeutrino

class MuonAntiNeutrino(Neutrino, Antiparticle):

    def __init__(self) -> None:
        super().__init__(Muon())
        self.name = "muon antinutrino"
        self.symbol = self.overbar(self.symbol)
        self._antiparticle()

BOSONS = [Photon, Z, WPlus, WMinus]
LEPTONS = [Electron, Positron,
           Muon, AntiMuon,
           ElectronNeutrino, ElectronAntiNeutrino,
           MuonNeutrino, MuonAntiNeutrino]
PARTICLES = BOSONS + LEPTONS # type: ignore

