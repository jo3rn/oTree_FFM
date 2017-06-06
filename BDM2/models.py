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
        if self.round_number == 1:
            for p in self.get_players():
                # zufälliger Snack, der am Ende ausbezahlt werden könnte
                p.participant.vars['random_snack'] = random.choice(Constants.list_snacks)
                print(p.participant.vars['random_snack'])

                # Preis für den zufälligen Snack
                p.participant.vars['random_price'] = random.randrange(0, 50)/10
                print(p.participant.vars['random_price'])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def unfill_snack_list(self):
        ''' entferne erste Index-Zahl aus Teilnehmer-Snack-Liste
        '''
        self.participant.vars['num_snacks_Step4'].pop(0)



    #### DATA-fields:
    # was der Teilnehmer mit dem Schieberegler wählt
    slider_value = models.CharField(widget=widgets.SliderInput())
    # welchen Snack der Teilnehmer gerade bewertet
    rated_snack = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # zufälliger Snack, den der Teilnehmer "gewinnen" kann
    won_snack = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # Preis des Snacks, sofern kleiner-gleich der Zahlungsbereitschaft
    won_price = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
