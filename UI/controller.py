import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        """
        Funzione che si attiva quando viene premuto il pulsante "umidità media" e stampa
        l'umidità media per ciascuna località, nel mese specificato
        """
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        umidita_media = self._model.get_umidita_media(self._mese)
        self._view.lst_result.controls.clear()
        if not umidita_media:
            self._view.lst_result.controls.append(ft.Text("Nessun dato disponibile"))
        else:
            self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese selezionato è:"))
            for situazione in umidita_media:
                self._view.lst_result.controls.append(ft.Text(f"{situazione[0]}: {situazione[1]}"))
            self._view.update_page()

    def handle_sequenza(self, e):
        """
        Funzione che tramite un algoritmo ricorsivo calcola la sequenza delle città da visitare
        nei primi 15 giorni del mese selezionato, tale da minimizzare il costo complessivo sapendo che
        il tecnico compie analisi tecniche della durata di un giorno in ciascuna città e che le anlaisi
        hanno un costo per ogni giornata determinato dalla somma di un fattore costante (di valore 100)
        ogniqualvolta il tecnico si sposta da una città all'altra in due giorni consecutivi, e un fattore
        variabile pari al valore numerico dell'umidità della città nel giorno considerato.
        Inoltre vanno rispettati i seguenti vincoli:
        - In nessuna città si possono effettuare più di 6 giornate anche non consecutive.
        - Scelta una città, il tecnico non si può spstare prima di aver trascorso 3 giorni consecutivi in essa.
        """
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        sequenza_ottima, costo_minimo = self._model.get_sequenza_ottima(self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {costo_minimo} ed è:"))
        for situazione in sequenza_ottima:
            self._view.lst_result.controls.append(ft.Text(f"{situazione.localita}-{situazione.data} Umidità: {situazione.umidita}"))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)
