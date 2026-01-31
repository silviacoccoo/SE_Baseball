import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    # PRIMO BOTTONE --> CREA IL GRAFO
    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        year = self._view.dd_anno.value
        if year is None:
            self._view.show_alert('Selezionare un anno!')
            return

        self._model.build_graph(int(year))

        self._view.update()
        # TODO

    # SECONDO BOTTONE --> DETTAGLI SQUADRE
    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        id_squadra=self._view.dd_squadra.value
        if id_squadra is None:
            self._view.show_alert('Selezionare una squadra!')
            return

        oggetto_squadra=self._model.id_map[id_squadra]

        if not self._model.G.has_node(oggetto_squadra):
            self._view.show_alert('La squadra non fa parte del grafo!')
            return

        vicini=self._model.get_neighbors_team(oggetto_squadra)

        self._view.txt_risultato.controls.clear()
        for v,p in vicini:
            self._view.txt_risultato.controls.append(
                ft.Text(f'{v.team_code} ({v.name}) - peso {p}')
            )
        self._view.update()
        # TODO

    # TERZO BOTTONE --> CALCOLO DEL PERCORSO
    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        id_squadra = self._view.dd_squadra.value
        if id_squadra is None:
            self._view.show_alert('Selezionare una squadra!')
            return

        try:
            nodo_partenza = self._model.id_map[int(id_squadra)]
        except KeyError:
            self._view.show_alert('Squadra non trovata!')
            return

        if not self._model.G.has_node(nodo_partenza):
            self._view.show_alert('La squadra selezionata non è nel grafo corrente')
            return

        best_path, best_score=self._model.get_best_solution(nodo_partenza)

        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(
            ft.Text(f'Percorso ottimo trovato con peso totale: {best_score}')
        )

        self._view.txt_risultato.controls.append(
            ft.Text(f'Lunghezza del percorso: {len(best_path)} nodi')
        )

        # Stampo la lista dei nodi
        percorso_str = ""
        for i, nodo in enumerate(best_path):
            percorso_str += f"{nodo.team_code}"
            if i < len(best_path) - 1:
                # Aggiungo una freccia e il peso dell'arco per chiarezza
                peso = self._model.G[nodo][best_path[i + 1]]['weight']
                percorso_str += f" --({peso})--> "

        self._view.txt_risultato.controls.append(ft.Text(percorso_str))

        self._view.update()
        # TODO

    """ Altri possibili metodi per gestire di dd_anno """""
    def fill_dropdown_year(self):
        """ Popola il dropdown con gli album presenti nel grafo """
        self._view.dd_anno.options.clear()
        self._view.dd_anno.value=None

        all_years=self._model.get_years() # LISTA DI INTERI

        for y in all_years:
            option=ft.dropdown.Option(text=y)
            self._view.dd_anno.options.append(option)

        self._view.dd_anno.update()

        # POTREBBE ESSERE UNA RIPETIZIONE - in quanto già fatto nel view
        #self._view.dd_anno.on_change=self.get_selected_year

    def get_selected_year(self,e):
        """ Handler per gestire la selezione dell'album dal dropdown """""

        year_scelto=self._view.dd_anno.value

        if year_scelto is None:
            self._view.show_alert('Selezionare un anno')
            return

        # VOGLIO LE SQUADRE DI QUELL'ANNO
        teams=self._model.get_teams_of_year(int(year_scelto))

        # Una volta selezionato stampare numero squadre ed elenco rispettive sigle
        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(
            ft.Text(f'Numero squadre: {len(teams)}')
        )
        for t in teams:
            self._view.txt_out_squadre.controls.append(
                ft.Text(f'{t.team_code} {t.name}')
            )

        self.fill_dropdown_team(year_scelto)

        self._view.update()

    def fill_dropdown_team(self, year):
        """ Popola il dropdown con gli album presenti nel grafo """
        self._view.dd_squadra.options.clear()
        self._view.dd_squadra.value = None

        all_teams = self._model.get_teams_of_year(int(self._view.dd_anno.value))

        for t in all_teams:
            option = ft.dropdown.Option(key=t.id,
                                        text=f'{t.team_code} ({t.name})')
            self._view.dd_squadra.options.append(option)

        self._view.dd_squadra.update()
    # TODO