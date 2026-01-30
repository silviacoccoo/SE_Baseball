import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G=nx.Graph()

        self.id_map={}
        self._lista_teams=[]

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
        # self.G.add_nodes_from(self._lista_teams)

        # AGGIUNTA ARCHI
        salari_map=DAO.get_teams_salaries(year)

        self.G = nx.complete_graph(self._lista_teams)

        for u, v in self.G.edges():
            peso = salari_map.get(u.id, 0) + salari_map.get(v.id, 0)
            self.G[u][v]['weight'] = peso

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

        risultato.sort(key=lambda x: x[1], reverse=True)
        return risultato

