from pile import Pile

class TalonPile(Pile):
    def __init__(self):
        super().__init__()

    def move_to_tableau(self, tableau_pile):
        if not self.is_empty():
            top_card = self.peek_top_card()
            if tableau_pile.is_valid_move(top_card):
                tableau_pile.add_card(self.remove_card())

