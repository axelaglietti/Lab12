import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._orderedRet = None
        self._connessioni = None
        self._allCountries = None
        self._grafo = nx.Graph()
        self._bestPath = []
        self._pesoMax = 0

    def getAllCountries(self):
        self._allCountries = DAO.getCountries()

    def buildGraph(self, nazione, anno):
        self._grafo.clear()
        self._retailers = DAO.getRetailers(nazione)
        self._grafo.add_nodes_from(self._retailers)
        for v0 in self._retailers:
            for v1 in self._retailers:
                if v0 != v1:
                    peso = DAO.getConnessione(anno, v0, v1)
                    if int(peso) > 0:
                        self._grafo.add_edge(v0, v1, weight=int(peso))
        """self._connessioni = DAO.getConnessioni(anno)
        for c in self._connessioni:
            self._grafo.add_edge(c.v0, c.v1, weight=c.peso)"""

    def calcolaVolumeVendita(self):
        for r in self._retailers:
            volumeVendita = 0
            for n in self._grafo.neighbors(r):
                volumeVendita += self._grafo[r][n]["weight"]
            if r.volumeVendita == 0:
                r.volumeVendita = volumeVendita
        self._orderedRet = sorted(self._retailers, key=lambda x: x.volumeVendita, reverse=True)

    def calcolaPercorso(self, lungh):
        self._bestPath = []
        self._pesoMax = 0
        for n in self._grafo.nodes:
            self.ricorsione([n], lungh)
        return self._bestPath, self._pesoMax

    def ricorsione(self, parziale, lungh):
        if len(parziale) == lungh+1:
            return
        if len(parziale) > 2:
            peso = self.calcolaPeso(parziale)
            if peso > self._pesoMax and parziale[0] == parziale[-1]:    # FARE CONTROLLO CHE SUI VICINI CI SIA L'ULTIMO
                self._pesoMax = peso
                print(parziale)
                self._bestPath = copy.deepcopy(parziale)
                return
        for n in self._grafo.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self.ricorsione(parziale, lungh)
                parziale.pop()

    def calcolaPeso(self, parziale):
        pesoTot = 0
        for v0 in parziale:
            for v1 in parziale:
                if self._grafo.has_edge(v0, v1):
                    pesoTot += self._grafo[v0][v1]["weight"]
        return pesoTot
