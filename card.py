class Card:
    def __init__(self, rank, suit, face_up=False):
        self.rank = str(rank)
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
            red_suits = ['h', 'd']
            black_suits = ['s', 'c']
            return (self.suit in red_suits and other_card.suit in red_suits) or \
                   (self.suit in black_suits and other_card.suit in black_suits)
        return False

    def __str__(self):
        return f'{self.rank} of {self.suit}' if self.face_up else 'Unknown card'


