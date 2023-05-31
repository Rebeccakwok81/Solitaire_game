from pile import Pile
from constants import CARD_WIDTH, CARD_HEIGHT

class Stockpile(Pile):
    def __init__(self):
        super().__init__()
        self.talon_pile = []

    def deal_card(self):
        if not self.is_empty():
            return self.cards.pop()
        else:
            raise ValueError("Stockpile is empty, cannot deal a card.")

    def move_to_talon(self):
        if not self.is_empty():
            card = self.remove_card()
            card.flip()
            self.talon_pile.append(card)

    def reset_stockpile(self):
        while self.talon_pile:
            card = self.talon_pile.pop()
            card.flip()
            self.cards.append(card)

    def get_top_talon_card(self):
        if self.talon_pile:
            return self.talon_pile[-1]
        else:
            return None
