from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

class BDM(Page):
    form_model = models.Player
    form_fields = ['slider_value', 'rated_snack']



    def vars_for_template(self):
        return {
            'image_path': 'kosfeld_test/' + str(Constants.list_snacks[self.participant.vars['num_snacks'][0]]) + '.bmp',
            'snack'     : str(Constants.list_snacks[self.participant.vars['num_snacks'][0]]),
            'left'      : len(Constants.list_snacks)-len(self.participant.vars['num_snacks'])
        }



    def before_next_page(self):
        #zu Testzwecken
        print("before_next_page")


        self.player.fill_BDM_dict()
        self.player.unfill_snack_list()






class Results(Page):
    pass


page_sequence = [
    Instructions,
    BDM
]
