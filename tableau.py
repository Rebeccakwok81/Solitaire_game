from pile import Pile
from constants import CARD_WIDTH, CARD_HEIGHT, TABLEAU_BOTTOM_ROW_Y

class TableauPile(Pile):
    def __init__(self):
        super().__init__()

    def remove_cards_from(self, card):
        if card in self.cards:
            index = self.cards.index(card)
            removed_cards = self.cards[index:]
            self.cards = self.cards[:index]
            return removed_cards
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

    def is_next_rank(self, rank1, rank2):
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return ranks.index(rank1) == ranks.index(rank2) + 1

    def get_selected_cards(self, x, y):
        for i in reversed(range(len(self.cards))):
            card_y = TABLEAU_BOTTOM_ROW_Y + i * 30
            if y >= card_y and y < card_y + CARD_HEIGHT:
                return self.cards[i:]
        return []

    def move_selected_cards(self, dx, dy):
        selected_cards = self.get_selected_cards(x, y)
        for card in selected_cards:
            card.move(dx, dy)
    