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

        oggetto_squadra=self._model.id_map[int(id_squadra)]
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
        self._view.update()
        # TODO

    """ Altri possibili metodi per gestire di dd_anno """""
    def fill_dropdown_year(self):
        """ Popola il dropdown con gli album presenti nel grafo """
        self._view.dd_anno.options.clear()
        self._view.dd_anno.value=None

        all_years=self._model.get_years()

        for y in all_years:
            option=ft.dropdown.Option(text=y)
            self._view.dd_anno.options.append(option)

        self._view.dd_anno.update()

        # POTREBBE ESSERE UNA RIPETIZIONE - in quanto già fatto nel view
        self._view.dd_anno.on_change=self.get_selected_year

    def get_selected_year(self,e):
        """ Handler per gestire la selezione dell'album dal dropdown """""

        year_scelto=self._view.dd_anno.value

        if year_scelto is None:
            self._view.show_alert('Selezionare un anno')
            return

        # VOGLIO LE SQUADRE DI QUELL'ANNO
        teams=self._model.get_teams_of_year(year_scelto)

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

        all_teams = self._model.get_teams_of_year(self._view.dd_anno.value)

        for t in all_teams:
            option = ft.dropdown.Option(key=t.id,
                                        text=f'{t.team_code} ({t.name})')
            self._view.dd_squadra.options.append(option)

        self._view.dd_squadra.update()
    # TODO