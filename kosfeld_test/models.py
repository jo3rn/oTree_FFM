from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random


author = 'Jörn Wieber'

doc = """
A player chooses between 2 images of snacks the one he/she prefers.
"""


class Constants(BaseConstants):
    name_in_url = 'kosfeld_test'
    players_per_group = None
    num_rounds = 3
    snacks = [  'actilifewildberry',
                'aftereight',
                'baerlibiber',
                'balistomuesli']


class Subsession(BaseSubsession):
    def before_session_starts(self):
        # Liste mit so vielen Zahlen, wie Bilder von Snacks
        pictures = list(range(4))
        # Wähle eine zufällige Zahl aus pictures, transkodiere sie in den Namen des Snacks
        picture1_number = random.choice(pictures)
        snack1 = Constants.snacks[picture1_number]
        self.session.vars['snack1'] = snack1
        # entferne diese Zahl aus pictures, damit nicht 2x das gleiche Bild gewählt wird
        pictures.remove(picture1_number)
        # Wähle eine zweite zufällige Zahl aus pictures, transkodiere sie in den Namen des Snacks
        picture2_number = random.choice(pictures)
        snack2 = Constants.snacks[picture2_number]
        self.session.vars['snack2'] = snack2


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # TODO: preferences liste in participant.vars
    preferences = []
    f1 = models.CharField(widget=widgets.RadioSelect())

    def check_radio_input(self):
        if self.f1 == self.session.vars['snack1']:
            a = self.f1
            b = self.session.vars['snack2']
            print(self.session.vars['snack1'])
            print(self.preferences)
        else:
            a = self.f1
            b = self.session.vars['snack1']
            print(self.session.vars['snack2'])
            print(self.preferences)

        if a in self.preferences:
            if b not in self.preferences:
                self.preferences.append(b)
            else:
                ia = self.preferences.index(a)
                ib = self.preferences.index(b)

                if ia > ib:
                    self.preferences.remove(a)
                    self.preferences.insert(ib, a)
                else:
                    return

        else:
            if b not in self.preferences:
                self.preferences += [a,b]
            else:
                ib = self.preferences.index(b)
                self.preferences.insert(ib, a)
