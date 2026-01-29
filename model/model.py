import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        # self.G=nx.complete_graph()
        self._nodes=[]
        self._edges=[]

        self.id_map={}
        self._lista_teams=[]
        self._lista_num_teams=[]

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
        return self._lista_teams

    def load_teams_connessi(self):
        pass

    def build_graph(self):
        pass

