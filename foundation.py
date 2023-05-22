from pile import Pile

class FoundationPile(Pile):
    def __init__(self):
        super().__init__()
        self.max_cards = 13

    def add_card(self, card):
        if self.is_valid_move(card):
            super().add_card(card)
        else:
            raise ValueError('Invalid move')

    def is_valid_move(self, card):
        if self.is_empty() and card.rank == 'A':
            return True
        elif not self.is_empty():
            top_card = self.peek_top_card()
            return card.suit == top_card.suit and self.is_next_rank(card.rank, top_card.rank)
        else:
            return False

    @staticmethod
    def is_next_rank(rank1, rank2):
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return ranks.index(rank1) == ranks.index(rank2) + 1

    def is_full(self):
        return len(self.cards) == self.max_cards