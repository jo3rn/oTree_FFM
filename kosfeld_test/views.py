from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class TestRun2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        two_snacks = random.sample(Constants.list_snacks, 2)
        snack1 = two_snacks[0]
        snack2 = two_snacks[1]

        checked_or_not = ['checked="checked"', '', '']
        random.shuffle(checked_or_not)
        dependency1 = checked_or_not[0]
        dependency2 = checked_or_not[1]

        return {# Pfad zu den Bildern der Snacks
                'image_path1': 'kosfeld_test/' + snack1 + '.JPG',
                'image_path2': 'kosfeld_test/' + snack2 + '.JPG',
                # Namen der Snacks
                'snack1': snack1,
                'snack2': snack2,
                # html-tags der radio buttons
                'image1': '<input name="decision" type="radio" id="s1" value="' + snack1 + '"' + dependency1 + '/>',
                'image2': '<input name="decision" type="radio" id="s2" value="' + snack2 + '"' + dependency2 + '/>'
                }

class Control2(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = models.Player
    form_fields = ['control_4', 'control_5', 'control_6']

class Step2(Page):
    def vars_for_template(self):
        # zufällige Reihenfolge der zwei Snacks
        # damit nicht immer der erste (=bessere) Snack default ist
        zero_one = [0, 1]
        random.shuffle(zero_one)
        snack1 = self.participant.vars["snacks_to_show"][zero_one[0]]
        snack2 = self.participant.vars["snacks_to_show"][zero_one[1]]

        ### Fallunterscheidung basierend auf der zugehörigen Treatment-Gruppierung des Teilnehmers:
        # Control-Gruppe
        if self.participant.vars['treatment'] == 'control':
            dependency1 = ''
            dependency2 = ''

        # Treatment 1
        if self.participant.vars['treatment'] == 'treatment_1':
            checked_or_not = ['checked="checked"', '']
            random.shuffle(checked_or_not)
            dependency1 = checked_or_not[0]
            dependency2 = checked_or_not[1]

        # Treatment 2
        if self.participant.vars['treatment'] == 'treatment_2':
            dependency1 = self.player.set_healthier_as_default(snack1, snack2)
            dependency2 = self.player.set_healthier_as_default(snack2, snack1)


        return {# Pfad zu den Bildern der Snacks
                'image_path1': 'kosfeld_test/' + snack1 + '.JPG',
                'image_path2': 'kosfeld_test/' + snack2 + '.JPG',
                # Namen der Snacks
                'snack1': snack1,
                'snack2': snack2,
                # html-tags der radio buttons
                'image1': '<input name="decision" type="radio" id="s1" value="' + snack1 + '"' + dependency1 + '/>',
                'image2': '<input name="decision" type="radio" id="s2" value="' + snack2 + '"' + dependency2 + '/>'
                }

    def before_next_page(self):
        # aus der Liste der anzuzeigenden Snacks die 2 entfernen, die gerade angezeigt wurden
        self.player.delete_two_snacks()

    # Radio Buttons aus Player-Class von models.py
    form_model = models.Player
    form_fields = ['offer_1', 'offer_2', 'decision']



class Results(Page):
    def is_displayed(self):
        # zeige Results-Seite nur nach der letzten Runde an
        return self.round_number == Constants.num_rounds


page_sequence = [
    TestRun2,
    TestRun2,
    TestRun2,
    Control2,
    Step2,
    Results
]
