from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import random


class MyPage(Page):
    def vars_for_template(self):
        label = '{}'.format(self.session.vars['snack1']) + ' oder ' + '{}'.format(self.session.vars['snack2']) + '?'

        return {# Pfad zu den Bildern der Snacks
                'image_path1': 'kosfeld_test/' + self.session.vars['snack1'] + '.bmp',
                'image_path2': 'kosfeld_test/' + self.session.vars['snack2'] + '.bmp',
                # Label des Radio-Buttons
                'label': label,
                # Namen der Snacks
                'snack1': self.session.vars['snack1'],
                'snack2': self.session.vars['snack2']
                }

    def before_next_page(self):
        self.player.check_radio_input()


        # ab hier dasselbe wie before_session_starts in models.py... TODO: DRY einhalten

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

    # Radio Buttons aus Player-Class von models.py
    form_model = models.Player
    form_fields = ['f1']

    def f1_choices(self):
        # die Snack-Namen neben den Radio-Buttons
        return [self.session.vars['snack1'], self.session.vars['snack2']]




class Results(Page):
    def is_displayed(self):
        # zeige Results-Seite nur nach der letzten Runde an
        return self.round_number == Constants.num_rounds


page_sequence = [
    MyPage,
    Results
]
