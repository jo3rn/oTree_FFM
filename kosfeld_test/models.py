from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import os
import operator
import itertools


author = 'Jörn Wieber'

doc = """
lets participant choose between 2 images the snack he/she prefers
"""


class Constants(BaseConstants):
    name_in_url = 'kosfeld_test'
    players_per_group = None
    num_rounds = 4
    list_snacks = []
    for snack in os.listdir('_static\\kosfeld_test'):
        if snack.endswith('.bmp'):
            snack = snack[:-4]
            list_snacks.append(snack)
        else:
            continue


class Subsession(BaseSubsession):
    def before_session_starts(self):

        # Weise einmalig Teilnehmer abwechselnd einem bestimmten Treatment zu
        if self.round_number == 1:
            treatments = itertools.cycle(['control', 'treatment_1', 'treatment_2'])
            for p in self.get_players():
                p.participant.vars['treatment'] = next(treatments)
                print(p.participant.vars['treatment'])

        # Fülle in Datenfeld, welchem Treatment der Teilnehmer zugeordnet ist
        for p in self.get_players():
            p.treatment = p.participant.vars['treatment']



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def delete_two_snacks(self):
        if len(self.participant.vars["snacks_to_show"]) >= 2:
            self.participant.vars["snacks_to_show"].pop(0)
            self.participant.vars["snacks_to_show"].pop(0)


    def set_higher_WTP_as_default(self, snack1, snack2):
        if self.participant.vars['BDM'].get(snack1) > self.participant.vars['BDM'].get(snack2):
            return 'checked="checked"'
        else:
            return ''


    #### DATA-fields
    # die zwei Snacks, zwischen denen sich der Teilnehmer entscheiden muss
    offer_1 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    offer_2 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # der Snack, für den sich der Teilnehmer entscheidet
    decision = models.CharField()
    # Treatment-Gruppe des Teilnehmers
    treatment = models.CharField()

    #decision = models.CharField(widget=widgets.RadioSelect())      {% formfield player.decision with label=label %}
