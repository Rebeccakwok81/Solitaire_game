class Pile:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self):
        return self.cards.pop()

    def top_card(self):
        return self.cards[-1] if self.cards else None

    def is_empty(self):
        return len(self.cards) == 0


class StockPile(Pile):
    pass  # nothing yet, to be implemented


class WastePile(Pile):
    pass  # nothing yet, to be implemented


class FoundationPile(Pile):
    def __init__(self, suit):
        super().__init__()
        self.suit = suit

    def is_valid(self, card):
        return card.suit == self.suit and (self.is_empty() and card.rank == 'Ace' or
                                            self.top_card().rank == Card.RANKS[Card.RANKS.index(card.rank) - 1])


class TableauPile(Pile):
    def __init__(self):
        super().__init__()
        self.face_down_cards = []

    def is_valid(self, card):
        return (self.is_empty() and card.rank == 'King') or (
            self.top_card().rank == Card.RANKS[Card.RANKS.index(card.rank) + 1] and
            Card.SUITS.index(self.top_card().suit) % 2 != Card.SUITS.index(card.suit) % 2)
