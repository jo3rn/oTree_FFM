from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Instructions(Page):
    def is_displayed(self):
        # zeige Instruktionen nur zu  Beginn an
        return self.round_number == 1

class TestRun(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        test_image = random.choice(Constants.list_snacks)
        return {
            'image_path': 'kosfeld_test/' + str(test_image) + '.JPG'
        }

class Control(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = models.Player
    form_fields = ['control_1', 'control_2', 'control_3']

# class WaitPage(WaitPage):
class WaitPage(Page):
    def is_displayed(self):
        return self.round_number == 1

    title_text = "Bitte warten..."
    body_text = "...bis alle Teilnehmer die Kontrollfragen beantwortet haben."

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
    TestRun,
    TestRun,
    TestRun,
    Control,
    WaitPage,
    BDM,
    End
]
