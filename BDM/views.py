from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

class BDM(Page):
    def vars_for_template(self):
        return {
            'image_path': 'kosfeld_test/' + str(Constants.list_snacks[self.participant.vars['num_snacks'][0]]) + '.JPG',
            'snack'     : str(Constants.list_snacks[self.participant.vars['num_snacks'][0]]),
            'left'      : len(Constants.list_snacks)-len(self.participant.vars['num_snacks'])
        }

    def before_next_page(self):
        self.player.fill_BDM_dict()
        self.player.unfill_snack_list()

    form_model = models.Player
    form_fields = ['slider_value', 'rated_snack']


class End(Page):
    def is_displayed(self):
        # zeige End-Seite nur nach der letzten Runde an
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.sort_WTPs()


page_sequence = [
    Instructions,
    BDM,
    End
]
