from pile import Pile

class TableauPile(Pile):
    def remove_cards_from(self, card):
        if card in self.cards:
            index = self.cards.index(card)
            return self.cards[index:]
        else:
            return None

    def is_valid_move(self, card):
        if self.is_empty() and card.rank == 'K':
            return True
        elif not self.is_empty():
            top_card = self.peek_top_card()
            return top_card.is_face_up() and not card.is_same_color(top_card) and self.is_next_rank(top_card.rank, card.rank)
        else:
            return False

    @staticmethod
    def is_next_rank(rank1, rank2):
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return ranks.index(rank1) == ranks.index(rank2) + 1
