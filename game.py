from constants import NUM_TABLEAU_PILES, NUM_FOUNDATION_PILES
from deck import Deck
from tableau import TableauPile
from foundation import FoundationPile
from stockpile import Stockpile
from talonpile import TalonPile

class Game:
    def __init__(self):
        self.deck = Deck()
        self.waste = []
        self.deck.shuffle()
        self.tableau = [TableauPile() for _ in range(NUM_TABLEAU_PILES)]
        self.foundation = [FoundationPile() for _ in range(NUM_FOUNDATION_PILES)]
        self.stockpile = Stockpile()
        self.talonpile = TalonPile()

        for i in range(NUM_TABLEAU_PILES):
            for j in range(i):
                self.tableau[i].add_card(self.deck.deal_card())
            card = self.deck.deal_card()
            card.flip()
            self.tableau[i].add_card(card)

        while not self.deck.is_empty():
            self.stockpile.add_card(self.deck.deal_card())

    def move_card(self, source, destination):
        if isinstance(source, Stockpile) and isinstance(destination, TableauPile):
            card = source.get_top_talon_card()
            if destination.is_valid_move(card):
                source.remove_card()
                card.flip()
                destination.add_card(card)
        elif isinstance(source, Stockpile) and isinstance(destination, FoundationPile):
            card = source.get_top_talon_card()
            if destination.is_valid_move(card):
                source.remove_card()
                card.flip()
                destination.add_card(card)
        elif isinstance(source, TableauPile) and isinstance(destination, FoundationPile):
            card = source.peek_top_card()
            if destination.is_valid_move(card):
                source.remove_card()
                destination.add_card(card)
        elif isinstance(source, TableauPile) and isinstance(destination, TableauPile):
            card = source.peek_top_card()
            if destination.is_valid_move(card):
                source.remove_card()
                destination.add_card(card)
        elif isinstance(source, TalonPile) and isinstance(destination, TableauPile):
            card = source.peek_top_card()
            if destination.is_valid_move(card):
                destination.add_card(source.remove_card())

    def is_won(self):
        return all(pile.is_full() for pile in self.foundation)
    
    def is_lost(self):
        return (
            self.stockpile.is_empty() and
            all(pile.is_empty() for pile in self.tableau) and
            all(pile.is_empty() for pile in self.talonpile)
        )
