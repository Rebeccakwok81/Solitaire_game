class Card:
    SUITS = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
    RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')

    def __init__(self, suit, rank, face_up=False):
        self.suit = suit
        self.rank = rank
        self.face_up = face_up

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def flip(self):
        self.face_up = not self.face_up

    def is_face_up(self):
        return self.face_up
