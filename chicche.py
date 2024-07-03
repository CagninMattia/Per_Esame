from collections import Counter

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
    products = []
    for edge in top_edges:
        products.extend([edge[0].Product_number, edge[1].Product_number])

    product_counts = Counter(products)
    common_products = [product for product, count in product_counts.items() if count > 1]

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
def get_nodi_visitabili(self, stato):
    st = None
    for s in self.lista_stati:
        if s.StateNme == stato:
            st = s
    albero = nx.dfs_tree(self.grafo, st)
    visitabili = list(albero.nodes)
    visitabili.remove(st)  # Rimuovi lo stato stesso dalla lista
    return visitabili


