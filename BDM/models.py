from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import os
from operator import itemgetter


author = 'Jörn Wieber'

doc = """
shows participants pictures of snacks and asks for their willingness-to-pay
"""


class Constants(BaseConstants):
    name_in_url = 'BDM'
    players_per_group = None

    # Anzahl unterschiedlicher Snack-Bilder, basierend auf Dateien im Snackbilder-Ordner
    num_snacks = len(os.listdir('_static\\kosfeld_test'))

    # Liste der Snacks, basierend auf .bmp-Dateien im Snackbilder-Ordner
    list_snacks = []
    for snack in os.listdir('_static\\kosfeld_test'):
        if snack.endswith('.bmp'):
            snack = snack[:-4]
            list_snacks.append(snack)
        else:
            continue

    # Anzahl an Entscheidungen, die gefällt werden sollen
    num_rounds = 4




class Subsession(BaseSubsession):
    def before_session_starts(self):
        # initialisiere Teilnehmer-Snack-Liste
        # erstellt für jeden Teilnehmer eine Liste mit Index-Zahlen für die Snack-Liste
        # diese Index-Zahlen werden zufällig geordnet (random.shuffle)

        # zu Testzwecken
        count = 1


        for p in self.get_players():
            if 'num_snacks' not in p.participant.vars:
                p.participant.vars['num_snacks'] = (list(range(Constants.num_snacks)))
                random.shuffle(p.participant.vars['num_snacks'])

                # zu Testzwecken
                print("zufällige Reihenfolge für Spieler " + str(count) + " erstellt")
                count += 1
                print(p.participant.vars['num_snacks'])


        # initialisiere BDM-Dictionary
        # erstellt ein zunächst leeres Dictionary, in das nach jeder Bewertung
        # über Player.fill_BDM_dict() ein key-value-Paar eingetragen wird
        # key: Snack
        # value: willingness-to-pay

        if self.round_number == 1:          # damit Schleife nur 1x durchlaufen wird
            for p in self.get_players():
                if 'BDM' in p.participant.vars:
                    continue
                else:
                    p.participant.vars['BDM'] = {}


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def unfill_snack_list(self):
        ''' entferne erste Index-Zahl aus Teilnehmer-Snack-Liste
        '''
        self.participant.vars['num_snacks'].pop(0)


    def fill_BDM_dict(self):
        rated_snack = self.slider_value
        # key: abgefragter Snack
        # value: willingness-to-pay
        self.participant.vars['BDM'][Constants.list_snacks[self.participant.vars['num_snacks'][0]]] = self.slider_value


    def sort_WTPs(self):
        '''Summe der potenzierten Differenzen der WTPs minimal halten
        '''
        # konvertiere BDM-dictionary in Liste von Tupel-Paaren: [(snack, WTP), (snack, WTP),...]
        sorted_BDM_tuples = sorted(self.participant.vars['BDM'].items(), key=itemgetter(1))
        # drehe Liste um, damit absteigend nach WTPs geordnet ist
        sorted_BDM_tuples.reverse()
        print('-----------------------sorted_BDM_tuples-------------------------------')
        print(sorted_BDM_tuples)
        BDM_length = len(sorted_BDM_tuples)

        # initialisiere Liste mit den geringsten WTP-Differenzen (wird in nachfolgender Schleife gefüllt)
        closest_WTPs = []

        for index, element in enumerate(sorted_BDM_tuples):
        # ermittelt Differenz zwischen höchster WTP und allen anderen WTPs,
        # geht dann weiter zur zweit-höchsten WTP und ermittelt deren Differenz zu allen niedrigeren WTPs
        # usw.
            if index != BDM_length-1:       # wenn nicht letztes Element der Liste
                i = index + 1
                while i < BDM_length:
                    WTP_difference = round(float(element[1])-float(sorted_BDM_tuples[i][1]), 1)
                    # wenn closest_WTP-Liste noch nicht voll ODER die gerade ermittelte WTP-Differenz niedriger als das Maximum der bereits vorhandenen WTP-Differenzen
                    if len(closest_WTPs) < Constants.num_rounds or max(closest_WTPs, key=itemgetter(2))[2] > WTP_difference:
                        next_element = sorted_BDM_tuples[i][0]
                        i += 1
                        # füge Triple (Snack1, Snack2, WTP-Differenz zwischen Snack1 und Snack2) zu closest_WTP-Liste hinzu
                        closest_WTPs.append((element[0], next_element, WTP_difference))

                        # wenn closest_WTP-Liste voll: entferne größte WTP-Differenz
                        if len(closest_WTPs) > Constants.num_rounds:
                            closest_WTPs.remove(max(closest_WTPs, key=itemgetter(2)))


        # speichere closest_WTP-Liste global in Teilnehmer-Variablen
        self.participant.vars['closest_WTPs'] = closest_WTPs

        print("-----------------------closest WTPs-------------------------------")
        print(self.participant.vars['closest_WTPs'])



    #### DATA-fields:
    # was der Teilnehmer mit dem Schieberegler wählt
    slider_value = models.CharField(widget=widgets.SliderInput())
    # welchen Snack der Teilnehmer gerade bewertet
    rated_snack = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
