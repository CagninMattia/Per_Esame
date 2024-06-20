import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    # Se devo riempire una dropdown list
    def fillDD(self):
        nazioni = self._model.get_nazioni()
        for c in nazioni:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))
            # Con data= rimane oggetto
            # Con key= si trasforma in stringa
            # Con text= Scriviamo quello che vogliamo vedere all'interno della DD

    # Serie di comandi per gestire la pressione del pulsante
    def handle_graph(self, e):
        anno = self._view.ddyear.value
        nazione = self._view.ddcountry.value
        if anno is not None and nazione is not None:
            try:
                anno = int(anno)
            except ValueError:
                self._view.txtOut3.controls.clear()
                self._view.create_alert("Inserisci un numero intero. ")
                self._view.update_page()
                return
            self._view.txt_result.controls.clear()
            self._view.update_page()
            self._model.crea_grafo(nazione, anno)
            num_nodi = self._model.num_nodi()
            num_archi = self._model.num_archi()
            self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {num_nodi}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero archi: {num_archi}"))
            self._view.btn_volume.disabled = False
            self._view.txtN.disabled = False
            self._view.btn_path.disabled = False
            self._view.update_page()
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare tutti e due i campi. "))
            self._view.update_page()

    def handle_volume(self, e):
        diz = self._model.volume_vendita()
        for retailer, volume in diz.items():
            self._view.txtOut2.controls.append(ft.Text(f"{retailer} --> {volume}"))
        self._view.update_page()

    # Dato un numero ti trova ciclo di costo massimo di lunghezza data dal numero
    def handle_path(self, e):
        numero = self._view.txtN.value
        self._view.txtOut3.controls.clear()
        self._view.update_page()
        # Controllo per intero
        try:
            numero = int(numero)
        except ValueError:
            self._view.txtOut3.controls.clear()
            self._view.create_alert("Inserisci un numero intero. ")
            self._view.update_page()
            return
        costo, ciclo_lista = self._model.get_ciclo_max(numero)
        lista_archi = self._model.get_ciclo_archi(ciclo_lista)
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {costo}"))
        for n in lista_archi:
            self._view.txtOut3.controls.append(ft.Text(f"{n[0]} --> {n[1]} Peso: {n[2]}"))
        self._view.update_page()




