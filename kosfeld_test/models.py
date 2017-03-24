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
    # TO DO: Liste erweitern mit allen Snacks
    snacks = [  'Actilife Wildberry',
                'After Eight',
                'Bärli-Biber',
                'Balisto Müsli']


class Subsession(BaseSubsession):
    def before_session_starts(self):
        # Liste mit so vielen Zahlen, wie Bilder von Snacks
        # TO DO: Anzahl an tatsächliche Snack-Bilder anpassen
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

    f1 = models.CharField(widget=widgets.RadioSelect())

    def check_radio_input(self):

        # check, ob noch keine Präferenzen-Liste für diesen Teilnehmer existiert
        if 'preferences' in self.participant.vars:
            pass
        else:
            self.participant.vars['preferences'] = []

        # der angeklickte Snack wird Variable "more_val"uable,
        # der andere Snack "less_val"uable
        if self.f1 == self.session.vars['snack1']:
            more_val = self.f1
            less_val = self.session.vars['snack2']
        else:
            more_val = self.f1
            less_val = self.session.vars['snack1']

        # wenn präferierter Snack bereits in Präferenzen-Liste:
        # gehe sicher, dass er vor dem anderen Snack steht
        if more_val in self.participant.vars['preferences']:
            if less_val not in self.participant.vars['preferences']:
                self.participant.vars['preferences'].append(less_val)
            else:
                # finde Position (Index) der Snacks in Präferenzen-Liste
                index_more = self.participant.vars['preferences'].index(more_val)
                index_less = self.participant.vars['preferences'].index(less_val)

                if index_more > index_less:
                    self.participant.vars['preferences'].remove(more_val)
                    self.participant.vars['preferences'].insert(index_less, more_val)
                else:
                    return

        # wenn präferierter Snack noch nicht in Präferenzen-Liste:
        #
        else:
            if less_val not in self.participant.vars['preferences']:
                self.participant.vars['preferences'] += [more_val, less_val]
            else:
                index_less = self.participant.vars['preferences'].index(less_val)
                self.participant.vars['preferences'].insert(index_less, more_val)

        #nur zu Testzwecken
        print(self.participant.vars['preferences'])
