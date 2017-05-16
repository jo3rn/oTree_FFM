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
lets participant again choose between 2 images the snack he/she prefers (without default)
"""


class Constants(BaseConstants):
    name_in_url = 'Step3'
    players_per_group = None
    num_rounds = 4
    list_snacks = []
    for snack in os.listdir('_static//kosfeld_test'):
        if snack.endswith('.JPG'):
            snack = snack[:-4]
            list_snacks.append(snack)
        else:
            continue


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def delete_two_snacks(self):
        if len(self.participant.vars["snacks_to_show_step3"]) >= 2:
            self.participant.vars["snacks_to_show_step3"].pop(0)
            self.participant.vars["snacks_to_show_step3"].pop(0)


    #### DATA-fields
    # die zwei Snacks, zwischen denen sich der Teilnehmer entscheiden muss
    offer_1 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    offer_2 = models.CharField(widget=widgets.HiddenInput(), verbose_name='')
    # der Snack, für den sich der Teilnehmer entscheidet
    decision = models.CharField()