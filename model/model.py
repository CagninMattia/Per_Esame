import copy

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        # Creo grafo
        self.grafo = nx.Graph()
        # Creo dizionario per nodi
        self.diz_vertici = {}
        # Per ricorsione
        self.costo_max = -100000000
        self.percorso_migliore = []


    def get_nazioni(self):
        return DAO.get_nazioni()

    def crea_grafo(self, nazione, anno):
        self.grafo.clear()
        # Cancello diz o liste se le ho inizializzate se uno schiacca due volte pulsante non ci sono problemi
        self.diz_vertici.clear()
        retailers = DAO.get_vertici(nazione)
        for r in retailers:
            self.diz_vertici[r.Retailer_code] = r
            self.grafo.add_node(r)
        archi = DAO.get_archi(nazione, anno)
        for a in archi:
            self.grafo.add_edge(self.diz_vertici[a[0]], self.diz_vertici[a[1]], weight=a[2])

    # Ritorno lunghezza nodi e archi
    def num_nodi(self):
        return len(self.grafo.nodes)

    def num_archi(self):
        return len(self.grafo.edges)

    # Calcola per ogni nodo il peso tot degli archi e li mette in un dizionario
    # ordinandolo in modo decrescente per un certo valore
    def volume_vendita(self):
        diz_volumi = {}
        nodi = self.grafo.nodes
        for r in nodi:
            vicini = self.grafo.neighbors(r)
            volume = 0
            for v in vicini:
                volume += self.grafo[r][v]["weight"]
            diz_volumi[r] = volume
        # Ordino in modo decrescente per un certo valore
        diz_volumi_ordinato = dict(sorted(diz_volumi.items(), key=lambda item: item[1], reverse=True))
        return diz_volumi_ordinato

    # Funzione che sfrutta la ricorsione per trovare ciclo di peso max nel grafo
    def get_ciclo_max(self, num_max):
        self.costo_max = -100000000
        self.percorso_migliore.clear()
        nodi = self.grafo.nodes
        for n in nodi:
            self.ricorsione(num_max, n, [n], [])
        return self.costo_max, self.percorso_migliore

    def ricorsione(self, num_max, n_partenza, lista_archi_tutti, lista_archi_tutti_tranne_primo):
        if len(lista_archi_tutti) == num_max+1:
            if n_partenza == lista_archi_tutti[-1]:
                if self.costo_tot(lista_archi_tutti) > self.costo_max:
                    print("dentro")
                    self.costo_max = copy.deepcopy(self.costo_tot(lista_archi_tutti))
                    self.percorso_migliore = copy.deepcopy(lista_archi_tutti)

        if len(lista_archi_tutti) > num_max:
            return

        for nodo in self.grafo.neighbors(lista_archi_tutti[-1]):
            if nodo not in lista_archi_tutti_tranne_primo:
                lista_archi_tutti.append(nodo)
                lista_archi_tutti_tranne_primo.append(nodo)
                self.ricorsione(num_max, n_partenza, lista_archi_tutti, lista_archi_tutti_tranne_primo)
                lista_archi_tutti.pop()
                lista_archi_tutti_tranne_primo.pop()

    # Lo uso nella ricorsione per calcolarmi il costo del ciclo
    def costo_tot(self, lista_archi_tutti):
        costo = 0
        for i in range(len(lista_archi_tutti)-1):
            costo += self.grafo[lista_archi_tutti[i]][lista_archi_tutti[i+1]]["weight"]
        return costo

    # Data una lista di nodi mi trovo lista di archi che collegano i nodi
    def get_ciclo_archi(self, lista):
        listabella = []
        for i in range(len(lista)-1):
            listabella.append((lista[i], lista[i+1],self.grafo[lista[i]][lista[i+1]]['weight']))
        return listabella
