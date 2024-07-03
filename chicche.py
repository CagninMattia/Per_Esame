"""Stampare:
i. Sull’area di testo con id txtResGrafo il numero di vertici ed archi 
ii. Sull’area di testo con id txtArchi, i tre archi di peso maggiore (seguendo la convenzione 
prodotto1, prodotto2, peso). Tra i vertici di questi tre archi, stampare i prodotti che sono 
presenti in più di uno dei tre archi. 
Esempio: se i tre archi sono A <-> C, A<->B, C<->D, i prodotti da stampare sono A, C."""
"""Parte di controller:
    for a in archi:
        self._view.txtOut.controls.append(ft.Text(f"Arco da {a[0]} a {a[1]} di peso {a[2]}"))
    self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono:"))
    for c in common_products:
        self._view.txtOut.controls.append(ft.Text(f"- {c}"))
"""
def get_nodi_da_stampare(self):
    # Get all edges with weights
    all_edges = list(self.grafo.edges(data=True))
    # Sort edges by weight in descending order
    all_edges_sorted = sorted(all_edges, key=lambda x: x[2]['weight'], reverse=True)
    # Get the top 3 edges
    top_edges = all_edges_sorted[:3]

    # Print top 3 edges to txtArchi
    archi = []
    for edge in top_edges:
        prod1 = edge[0].Product_number
        prod2 = edge[1].Product_number
        weight = edge[2]['weight']
        archi.append([prod1, prod2, weight])

    # Find common products
    # Inizializza la lista dei prodotti
    products = []

    # Itera su ogni arco in top_edges
    for edge in top_edges:
        # Aggiungi il Product_number del primo nodo dell'arco alla lista dei prodotti
        products.append(edge[0].Product_number)
        # Aggiungi il Product_number del secondo nodo dell'arco alla lista dei prodotti
        products.append(edge[1].Product_number)

    # Crea un dizionario per contare le occorrenze di ciascun prodotto
    product_counts = {}

    # Itera su ogni prodotto nella lista dei prodotti
    for product in products:
        if product in product_counts:
            product_counts[product] += 1
        else:
            product_counts[product] = 1

    # Inizializza la lista dei prodotti comuni
    common_products = []

    # Itera su ogni prodotto e il suo conteggio nel dizionario product_counts
    for product, count in product_counts.items():
        # Se il prodotto appare più di una volta, aggiungilo alla lista dei prodotti comuni
        if count > 1:
            common_products.append(product)

    # Print common products
    print("Common products in top 3 edges:", common_products)

    # Assume txtArchi is an area of text widget where the results need to be displayed
    # Here, just returning the value for demonstration
    return archi, common_products




""" Calcolo distanza coordinate due punti, qui avevo salvato in un dizionario le 
    chiave: nodo e come valore una lista contenete lat e lng"""

from geopy import distance
def dist(self, a1, a2):
    lat1 = self.diz_archi[a1][0]
    lon1 = self.diz_archi[a1][1]
    lat2 = self.diz_archi[a2][0]
    lon2 = self.diz_archi[a2][1]
    d = distance.geodesic((lat1, lon1), (lat2, lon2)).km
    return d

"""
Trovo nodi visitabili attraverso DFS 
"""
import networkx as nx
def get_nodi_visitabili(self, stato):
    st = None
    for s in self.lista_stati:
        if s.StateNme == stato:
            st = s
    albero = nx.dfs_tree(self.grafo, st)
    visitabili = list(albero.nodes)
    visitabili.remove(st)  # Rimuovi lo stato stesso dalla lista
    return visitabili

"""
Si definisca come “volume di vendita” di un retailer la somma dei pesi di tutti gli archi ad esso incidenti. Si 
visualizzi l’intero elenco di retailer, ordinati per valore decrescente. In questo elenco visualizzare il nome del 
retailer ed il valore del volume di vendita corrispondente
"""
def get_retailers_ordinati(self):
    # 1. Calcolare il volume di vendita per ogni retailer
    volumi_vendita = {}

    # Itera su ogni nodo del grafo
    for node in self.grafo.nodes:
        volumi_vendita[node] = 0  # Inizializza il volume di vendita a 0

    # Itera su ogni arco del grafo
    for edge in self.grafo.edges(data=True):
        retailer1, retailer2, data = edge
        weight = data['weight']
        # Aggiungi il peso dell'arco al volume di vendita di ciascun retailer
        volumi_vendita[retailer1] += weight
        volumi_vendita[retailer2] += weight

    # 2. Creare un elenco di retailer con i loro volumi di vendita
    elenco_retailer = []

    # Itera su ogni nodo e volume di vendita nel dizionario
    for retailer, volume in volumi_vendita.items():
        # Aggiungi una tupla con il retailer e il volume di vendita all'elenco
        elenco_retailer.append((retailer, volume))

    # 3. Ordinare l'elenco in ordine decrescente per volume di vendita
    elenco = sorted(elenco_retailer, key=lambda x: x[1], reverse=True)

    return elenco
