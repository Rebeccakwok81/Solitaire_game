from constants import SUIT_SYMBOLS, RANKS

class Card:
    def __init__(self, rank, suit, face_up=True):
        self.rank = rank
        self.suit = suit
        self.face_up = face_up

    def get_image_filename(self):
        return f'{self.rank}{self.suit}.png'

    def flip(self):
        self.face_up = not self.face_up

    def is_face_up(self):
        return self.face_up

    def is_same_color(self, other_card):
        if other_card:
            red_suits = [HEARTS, DIAMONDS]
            black_suits = [SPADES, CLUBS]
            return (self.suit in red_suits and other_card.suit in red_suits) or \
                   (self.suit in black_suits and other_card.suit in black_suits)
        return False

