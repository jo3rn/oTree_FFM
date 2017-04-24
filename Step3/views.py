from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class Step3(Page):
    def vars_for_template(self):
        snack1 = self.participant.vars["snacks_to_show_step3"][0]
        snack2 = self.participant.vars["snacks_to_show_step3"][1]

        return {# Pfad zu den Bildern der Snacks
                'image_path1': 'kosfeld_test/' + snack1 + '.bmp',
                'image_path2': 'kosfeld_test/' + snack2 + '.bmp',
                # Namen der Snacks
                'snack1': snack1,
                'snack2': snack2,
                # html-tags der radio buttons
                'image1': '<input name="decision" type="radio" id="s1" value="' + snack1 + '"' + '/>',
                'image2': '<input name="decision" type="radio" id="s2" value="' + snack2 + '"' + '/>'
                }

    def before_next_page(self):
        # aus der Liste der anzuzeigenden Snacks die 2 entfernen, die gerade angezeigt wurden
        self.player.delete_two_snacks()

    # Radio Buttons aus Player-Class von models.py
    form_model = models.Player
    form_fields = ['offer_1', 'offer_2', 'decision']

    timeout_seconds = 20



class Results(Page):
    def is_displayed(self):
        # zeige Results-Seite nur nach der letzten Runde an
        return self.round_number == Constants.num_rounds


page_sequence = [
    Instructions,
    Step3,
    Results
]
