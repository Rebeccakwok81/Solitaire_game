from card import Card

class Pile:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None

    def peek_top_card(self):
        if self.cards:
            return self.cards[-1]
        else:
            return None

    def is_empty(self):
        return len(self.cards) == 0
