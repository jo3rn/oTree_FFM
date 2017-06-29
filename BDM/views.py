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
        # zeige Testlauf nur zu Beginn an
        return self.round_number == 1

    def vars_for_template(self):
        # für den Testlauf wird ein Bild zufällig gewählt
        test_image = random.choice(Constants.list_snacks)
        return {
            'image_path': 'kosfeld_test/' + str(test_image) + '.JPG'
        }

class Control(Page):
    def is_displayed(self):
        # zeige Kontrollfragen nur zu Beginn an
        return self.round_number == 1

    # Eingabefelder für die Kontrollfragen
    form_model = models.Player
    form_fields = [ 'control_1', 'control_2', 'control_3', 'control_4',
                    'control_5', 'control_6', 'control_7']


# class WaitPage(WaitPage):
# WaitPage class wird nicht genommen, damit es beim letzten User nicht automatisch weiter geht.
# Der Experimentator setzt mit "advanced slowest user" das Experiment fort
class WaitPage(Page):
    def is_displayed(self):
        # zeige Warteseite nur nach Kontrollfragen (zu Beginn) an
        return self.round_number == 1

class BDM(Page):
    def vars_for_template(self):
        # image_path: Pfad zum Snack, der auf dieser Seite angezeit wird
        # snack: Name des Snacks
        # left: wieviele Snacks noch bewertet werden müssen
        return {
            'image_path': 'kosfeld_test/' + str(Constants.list_snacks[self.participant.vars['num_snacks'][0]]) + '.JPG',
            'snack'     : str(Constants.list_snacks[self.participant.vars['num_snacks'][0]]),
            'left'      : len(Constants.list_snacks)-len(self.participant.vars['num_snacks'])
        }

    def before_next_page(self):
        # schreibe Zahlungsbereitschaft in BDM-Liste
        self.player.fill_BDM_dict()
        # entferne bewerteten Snack aus der Liste der noch zu bewertenden Snacks
        self.player.unfill_snack_list()

    # Feld für den Wert des Sliders
    # Feld für den Namen des Snacks
    form_model = models.Player
    form_fields = ['slider_value', 'rated_snack']


class End(Page):
    def is_displayed(self):
        # zeige End-Seite nur nach der letzten Runde an
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'treatment'     : str(self.participant.vars['treatment'])
        }

    def before_next_page(self):
        self.player.sort_WTPs()


page_sequence = [
    Instructions,
    TestRun,
    Control,
    WaitPage,
    BDM,
    End
]
