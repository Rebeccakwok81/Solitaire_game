# does not provide method for moving cards from waste pile to tableau
# does not provide ability to move entire stack of cards within tableau
# does not provide ability o f flipping over face-down cards in the tableau
# does not provide error checking, in terms of invalid moves

class Game:
    def __init__(self):
        self.deck = Deck()
        self.stock_pile = StockPile()
        self.waste_pile = WastePile()
        self.foundation_piles = [FoundationPile(suit) for suit in Card.SUITS]
        self.tableau_piles = [TableauPile() for _ in range(7)]

        # Deal initial cards to tableau
        for i in range(7):
            for j in range(i):
                self.tableau_piles[i].face_down_cards.append(self.deck.deal())
            self.tableau_piles[i].add_card(self.deck.deal().flip())

        # Put the rest of the cards in the stock pile
        while not self.deck.is_empty():
            self.stock_pile.add_card(self.deck.deal())

    def draw_from_stock(self):
        if self.stock_pile.is_empty():
            # Refill the stock pile from the waste pile
            while not self.waste_pile.is_empty():
                card = self.waste_pile.remove_card()
                card.flip()
                self.stock_pile.add_card(card)
        else:
            card = self.stock_pile.remove_card()
            card.flip()
            self.waste_pile.add_card(card)

    def move_to_foundation(self, source_pile):
        if isinstance(source_pile, (WastePile, TableauPile)):
            card = source_pile.top_card()
            for foundation_pile in self.foundation_piles:
                if foundation_pile.is_valid(card):
                    foundation_pile.add_card(source_pile.remove_card())
                    return True
        return False

    def move_in_tableau(self, source_pile, target_pile, num_cards):
        if isinstance(source_pile, TableauPile) and source_pile is not target_pile:
            if target_pile.is_valid(source_pile.cards[-num_cards]):
                target_pile.cards.extend(source_pile.cards[-num_cards:])
                source_pile.cards = source_pile.cards[:-num_cards]
                return True
        return False

    def is_won(self):
        return all(len(pile.cards) == 13 for pile in self.foundation_piles)
