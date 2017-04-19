from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class BDM2(Page):
    def vars_for_template(self):
        return {
            'image_path': 'kosfeld_test/' + str(Constants.list_snacks[self.participant.vars['num_snacks_Step4'][0]]) + '.bmp',
            'snack'     : str(Constants.list_snacks[self.participant.vars['num_snacks_Step4'][0]]),
            'left'      : len(Constants.list_snacks)-len(self.participant.vars['num_snacks_Step4'])
        }

    def before_next_page(self):
        self.player.unfill_snack_list()

    form_model = models.Player
    form_fields = ['slider_value', 'rated_snack']

class End(Page):
    def is_displayed(self):
        # zeige End-Seite nur nach der letzten Runde an
        return self.round_number == Constants.num_rounds



page_sequence = [
    Instructions,
    BDM2,
    End
]
