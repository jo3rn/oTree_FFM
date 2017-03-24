from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import os


author = 'Your name here'

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

    # jeder Snack soll einmal abgefragt werden
    num_rounds = num_snacks


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


        # initialisiere BDM-Liste
        # erstellt ein zunächst leeres Dictionary, in das nach jeder Bewertung
        # über Player.fill_BDM_list() ein key-value-Paar eingetragen wird
        # key: Snack
        # value: willingness-to-pay
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
        #TODO: rated_snack field füllen (im Monitoring)
        rated_snack = self.slider_value

        # key: abgefragter Snack
        # value: willingness-to-pay
        self.participant.vars['BDM'][Constants.list_snacks[self.participant.vars['num_snacks'][0]]] = self.slider_value
        #zu Testzwecken
        print("fill_BDM_list")
        print(self.participant.vars['BDM'])


    # Slider für BDM
    slider_value = models.CharField(widget=widgets.SliderInput(attrs={'step': '0.10'}), verbose_name="Deine Bewertung:", min="0.0", max="5.0")

    rated_snack = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
