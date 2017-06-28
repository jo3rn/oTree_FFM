from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        # im Folgenden wird der zufällige Snack ausgewählt
        if self.round_number == 1:

            # Zufalls-Stufe, von der ausgewählt wird
            self.participant.vars['step'] = random.choice([1,2,3,4])
            print(self.participant.vars['step'])

            if self.participant.vars['step'] in [1, 4]:
                # zufälliger Snack, der am Ende ausbezahlt werden könnte
                self.participant.vars['random_snack'] = random.choice(Constants.list_snacks)

            if self.participant.vars['step'] == 2:
                # zufälliger Snack, der am Ende ausbezahlt wird
                self.participant.vars['random_snack'] = random.choice(self.participant.vars['step2_decisions'])

            if self.participant.vars['step'] == 3:
                # zufälliger Snack, der am Ende ausbezahlt wird
                self.participant.vars['random_snack'] = random.choice(self.participant.vars['step3_decisions'])

            # Preis für den zufälligen Snack
            self.participant.vars['random_price'] = random.randrange(0, 50)/10

            print("Step2 und 3 decisions")
            print(self.participant.vars['step2_decisions'])
            print(self.participant.vars['step3_decisions'])
            print(self.participant.vars['random_snack'])

class BDM2(Page):
    def vars_for_template(self):
        return {
            'image_path': 'kosfeld_test/' + str(Constants.list_snacks[self.participant.vars['num_snacks_Step4'][0]]) + '.JPG',
            'snack'     : str(Constants.list_snacks[self.participant.vars['num_snacks_Step4'][0]]),
            'left'      : len(Constants.list_snacks)-len(self.participant.vars['num_snacks_Step4'])
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


    def vars_for_template(self):
        # PAYOFF LOGIK
        # bestimme Stufe, die für den Payoff genommen wird
        step_payoff = self.participant.vars['step']
        minimumwage = 10
        random_snack = self.participant.vars['random_snack']

        if step_payoff == 1 or step_payoff == 4:
            payoff_with_snack = minimumwage - float(self.participant.vars['random_price'])
            payoff_without_snack = minimumwage
            if step_payoff == 1:
                participant_WTP = float(self.participant.vars['BDM'][self.participant.vars['random_snack']])
            if step_payoff == 4:
                #TO DO: Liste für Step 4 erstellen
                participant_WTP = float(self.participant.vars['WTPs_step_4'][self.participant.vars['random_snack']])

        if step_payoff == 2 or step_payoff == 3:
            payoff_with_snack = minimumwage
            payoff_without_snack = minimumwage
            participant_WTP = "-"


        return {
            'step': step_payoff,
            'random_snack': random_snack,
            'random_price': float(self.participant.vars['random_price']),
            'participant_WTP': participant_WTP,
            'payoff_with_snack': payoff_with_snack,
            'payoff_without_snack': payoff_without_snack
        }

    form_model = models.Player
    form_fields = ['rand_snack', 'rand_price', 'payout1', 'payout2']



page_sequence = [
    Instructions,
    BDM2,
    End
]
