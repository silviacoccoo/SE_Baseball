import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G=nx.Graph()

        self.id_map={}
        self._lista_teams=[]

        self._best_path=[]
        self._best_score=0

    @staticmethod
    # Se sottolinea in giallo, trasformalo in static method
    def get_years():
        return DAO.get_years()

    def get_teams_of_year(self,year):
        self._lista_teams=DAO.get_teams_by_year(year)
        # MAPPING TRA CHIAVE TEAM E OGGETTO TEAM
        self.id_map = {}
        for team in self._lista_teams:
            self.id_map[team.id] = team
        return self._lista_teams # LISTA DI OGGETTI

    def build_graph(self,year):

        self.G.clear()

        self.get_teams_of_year(year)

        salari_map=DAO.get_teams_salaries(year)

        # MODO 1: CON LA FUNZIONE COMPLETE_GRAPH
        self.G = nx.complete_graph(self._lista_teams)

        for u, v in self.G.edges():
            peso = salari_map.get(u.id, 0) + salari_map.get(v.id, 0)
            self.G[u][v]['weight'] = peso

        # MODO 2: CON IL CICLO

        # self.G.add_nodes_from(self._lista_teams)

        """
        for i in range(len(self._lista_teams)):
            for j in range(i+1,len(self._lista_teams)):
                t1=self._lista_teams[i]
                t2=self._lista_teams[j]

                peso=salari_map.get(t1.id,0)+salari_map.get(t2.id, 0)
                self.G.add_edge(t1,t2,weight=peso)
        """

    def get_neighbors_team(self,team):
        vicini_nodi=self.G.neighbors(team)
        risultato=[]
        for v in vicini_nodi:
            peso=self.G[team][v]['weight']
            risultato.append((v,peso))

        risultato.sort(key=lambda x: x[1], reverse=True) # x[1] indica di ordinare in base al peso che si trova in posizione 1 della tupla
        return risultato

    # PUNTO 2 RICORSIONE
    def get_best_solution(self,nodo_partenza):
        """Prepara i dati e lancia la ricorsione"""
        # RESET
        self._best_path=[]
        self._best_score = 0

        # RECUPERO DATI NECESSARI
        parziale=[nodo_partenza]

        self.ricorsione(parziale,float('inf'))
        return self._best_path,self._best_score

    def ricorsione(self,parziale,ultimo_peso):
        # Calcolo il peso attuale del percorso parziale
        peso_corrente=self.calcola_peso_percorso(parziale)

        # Caso terminale
        if peso_corrente > self._best_score:
            self._best_score=peso_corrente
            self._best_path=list(parziale)

        # Caso ricorsivo
        ultimo_nodo=parziale[-1]
        vicini_possibili=[]

        for vicino in self.G.neighbors(ultimo_nodo):
            peso_arco=self.G[ultimo_nodo][vicino]['weight']

            # VINCOLI
            # Non devo aver visitato il nodo
            if vicino not in parziale:
                # Il peso deve essere strettamente decrescente
                if peso_arco<ultimo_peso:
                    vicini_possibili.append((vicino, peso_arco))
        # Ordino per peso decrescente
        vicini_possibili.sort(key=lambda x: x[1], reverse=True)

        K=3
        vicini_migliori=vicini_possibili[:K]

        for v,p in vicini_migliori:
            parziale.append(v)
            self.ricorsione(parziale,p)
            parziale.pop()

    def calcola_peso_percorso(self, lista_nodi):
        if len(lista_nodi)<2:
            return 0
        peso_tot=0
        for i in range(len(lista_nodi)-1):
            u=lista_nodi[i]
            v=lista_nodi[i+1]
            peso_tot+=self.G[u][v]['weight']
        return peso_tot



