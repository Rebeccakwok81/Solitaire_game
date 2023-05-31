from constants import SUITS, RANKS
from card import Card
import random

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            return None

    def is_empty(self):
        return len(self.cards) == 0
