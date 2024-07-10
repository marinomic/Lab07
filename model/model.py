import copy
from database.meteo_dao import MeteoDao
from model.situazione import Situazione


class Model:
    def __init__(self):
        self._costo_minimo = -1
        self._sequenza_ottima = []

    def get_umidita_media(self, _mese):
        return MeteoDao.get_umidita_media_mese(_mese)

    def get_situazioni_meta_mese(self, _mese):
        return MeteoDao.get_situazioni_meta_mese(_mese)

    def get_sequenza_ottima(self, _mese):
        self._costo_minimo = -1
        self._sequenza_ottima = []
        self._ricorsione([], self.get_situazioni_meta_mese(_mese))
        return self._sequenza_ottima, self._costo_minimo

    def _ricorsione(self, parziale: list[Situazione], situazioni):
        # Caso terminale
        if len(parziale) == 15:
            costo = self._calcola_costo(parziale)
            if (self._costo_minimo == -1) or (costo < self._costo_minimo):
                self._costo_minimo = costo
                self._sequenza_ottima = copy.deepcopy(parziale)
            return parziale
        # Caso ricorsivo
        else:
            # Il giorno corrisponde alla lunghezza della lista parziale + 1
            day = len(parziale) + 1
            # 3 situazioni per giorno (Torino, Milano, Genova) corrispondono a 3 posizioni in situazioni che è stata
            # creata con la query SQL che ordina per data e quindi la query genera prima le situazione di tutte e 3 le città
            # per il primo giorno, poi per il secondo giorno e così via, vedere l'esecuzione su DBeaver. Quindi per
            # passare da un giorno al successivo iterando su situazioni bisogna utilizzare quel calcolo qua sotto
            for situazione in situazioni[(day - 1) * 3:day * 3]:
                # oppure, più intuitivo secondo me, cambi il for qua sopra così:
                # for situazione in situazioni:
                #     if situazione.data.day == day:
                if self._vincoli(parziale, situazione):
                    parziale.append(situazione)
                    self._ricorsione(parziale, situazioni)
                    parziale.pop()

    def _vincoli(self, parziale, situazione) -> bool:
        # In nessuna città si possono trascorrere più di 6 giornate (anche non consecutive)
        counter = 0
        for fermata in parziale:
            if fermata.localita == situazione.localita:
                counter += 1
        if counter >= 6:
            return False

        # Scelta una città, il tecnico non si può spostare prima di aver trascorso 3 giorni consecutivi in essa
        # se la sequenza ha 1 o 2 elementi posso solo rimettere la prima città, quindi alla seconda e la terza
        # iterazione ricorsiva sarò sicuro che la città sia la stessa della prima iterazione grazie a questo vincolo
        if 0 < len(parziale) <= 2:
            if situazione.localita != parziale[0].localita:
                return False
        # se la mia parziale ha almeno 3 elementi devo controllare che gli ultimi 3 siano tutti uguali
        elif len(parziale) > 2:
            sequenza_finale = parziale[-3:]
            prima_fermata = sequenza_finale[0].localita
            counter = 0
            for fermata in sequenza_finale:
                if fermata.localita == prima_fermata:
                    counter += 1
            if (counter < 3) and situazione.localita != sequenza_finale[-1].localita:
                return False
        # Se non si è violato nessun vincolo
        return True

    def _calcola_costo(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            # 1) costo dell'umidità
            costo += parziale[i].umidita
            # 2) costo del cambio città
            if i == 2:
                if parziale[i].localita != parziale[0].localita:
                    costo += 100
            elif i > 2:
                ultime_fermate = parziale[i - 2:i + 1]
                if (ultime_fermate[2].localita != ultime_fermate[0].localita or
                        ultime_fermate[2].localita != ultime_fermate[1].localita):
                    costo += 100
        return costo
