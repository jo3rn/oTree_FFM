from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import os
import random


author = 'Jörn Wieber'

doc = """
again shows participants pictures of snacks and asks for their willingness-to-pay
"""


class Constants(BaseConstants):
    name_in_url = 'Step4'
    players_per_group = None

    # Anzahl unterschiedlicher Snack-Bilder, basierend auf Dateien im Snackbilder-Ordner
    num_snacks = len(os.listdir('_static//kosfeld_test'))

    # Liste der Snacks, basierend auf .jpg-Dateien im Snackbilder-Ordner
    list_snacks = []
    for snack in os.listdir('_static//kosfeld_test'):
        if snack.endswith('.JPG'):
            snack = snack[:-4]
            list_snacks.append(snack)
        else:
            continue

    # Anzahl an Entscheidungen, die in Step 4 gefällt werden sollen = Anzahl Snacks gesamt
    num_rounds = len(os.listdir('_static//kosfeld_test'))


class Subsession(BaseSubsession):
    def before_session_starts(self):
        pass




class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def unfill_snack_list(self):
        ''' entferne erste Index-Zahl aus Teilnehmer-Snack-Liste
        '''
        self.participant.vars['num_snacks_Step4'].pop(0)

    def fill_BDM_dict(self):
        # nur notwendig für mögliche spätere Auszahlung
        rated_snack = self.slider_value
        # key: abgefragter Snack
        # value: willingness-to-pay
        if self.slider_value == "":
            self.participant.vars['WTPs_step_4'][Constants.list_snacks[self.participant.vars['num_snacks_Step4'][0]]] = '0'
        else:
            self.participant.vars['WTPs_step_4'][Constants.list_snacks[self.participant.vars['num_snacks_Step4'][0]]] = self.slider_value


    #### DATA-fields:
    # was der Teilnehmer mit dem Schieberegler wählt
    slider_value = models.CharField(widget=widgets.SliderInput())
    # welchen Snack der Teilnehmer gerade bewertet
    rated_snack = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # zufälliger Snack, den der Teilnehmer "gewinnen" kann
    rand_snack = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # zufälliger Preis des Snacks
    rand_price = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # Label des PCs
    p_label = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # ausgegebener Snack, falls WTP größer gleich zufälliger Preis
    payout1 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # gesamte Geld-Auszahlung am Ende
    payout2 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # ausgegebener Snack, falls WTP größer gleich zufälliger Preis
    payout3 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # gesamte Geld-Auszahlung am Ende
    payout4 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # ausgegebener Snack, falls WTP größer gleich zufälliger Preis
    payout5 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # gesamte Geld-Auszahlung am Ende
    payout6 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # ausgegebener Snack, falls WTP größer gleich zufälliger Preis
    payout7 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # gesamte Geld-Auszahlung am Ende
    payout8 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # ausgegebener Snack, falls WTP größer gleich zufälliger Preis
    payout9 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # gesamte Geld-Auszahlung am Ende
    payout10 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
