import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []


    def fillDD(self):
        # FILL YEARS
        for i in range(2015, 2019):
            self._view.ddyear.options.append(ft.dropdown.Option(f"{i}"))
        # FILL COUNTRIES
        self._model.getAllCountries()
        for c in self._model._allCountries:
            self._view.ddcountry.options.append(ft.dropdown.Option(f"{c}"))
        self._view.update_page()

    def handle_graph(self, e):
        nazione = self._view.ddcountry.value
        anno = self._view.ddyear.value
        self._model.buildGraph(nazione, anno)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {len(self._model._grafo.nodes)}, Numero di archi: {len(self._model._grafo.edges)}"))
        self._view.update_page()

    def handle_volume(self, e):
        self._model.calcolaVolumeVendita()
        for r in self._model._orderedRet:
            if r.volumeVendita > 0:
                self._view.txtOut2.controls.append(ft.Text(f"{r.Retailer_name} --> {r.volumeVendita}"))
        self._view.update_page()

    def handle_path(self, e):
        self._view.txtOut3.controls.clear()
        lungh = self._view.txtN.value
        try:
            lunghInt = int(lungh)
        except ValueError:
            self._view.txtOut3.controls.append(ft.Text(f"Devi inserire un numero intero"))
            self._view.update_page()
            return
        if lunghInt < 2:
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append(ft.Text(f"Devi inserire un valore almeno grande 2"))
            self._view.update_page()
            return
        percorso, peso = self._model.calcolaPercorso(lunghInt)
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {peso}"))
        for i in range(0, len(percorso)-1):
            self._view.txtOut3.controls.append(f"{percorso[i]} --> {percorso[i+1]}: {self._model._grafo[percorso[i]][percorso[i+1]]["weight"]}")
        self._view.update_page()


