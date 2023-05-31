# constants for card dimensions
CARD_WIDTH = 115
CARD_HEIGHT = 175

# constants for window dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750

# constants for colors
BACKGROUND_COLOR = (0, 100, 0)  # Green background

# constants for tableau pile positions
TABLEAU_LEFT_MARGIN = 100
TABLEAU_BOTTOM_ROW_Y = 300
TABLEAU_COLUMN_WIDTH = (1200 - 2*100) // 7

# constants for foundation pile positions
FOUNDATION_LEFT_MARGIN = TABLEAU_LEFT_MARGIN + 3 * (WINDOW_WIDTH - 2 * TABLEAU_LEFT_MARGIN) // 7
FOUNDATION_TOP_ROW_Y = 50

# constant for talon pile position
TALONPILE_POSITION = (TABLEAU_LEFT_MARGIN + (WINDOW_WIDTH - 2 * TABLEAU_LEFT_MARGIN) // 7, FOUNDATION_TOP_ROW_Y)

# constant for stockpile position
STOCKPILE_POSITION = (TABLEAU_LEFT_MARGIN, FOUNDATION_TOP_ROW_Y)

# constants for number of piles
NUM_TABLEAU_PILES = 7
NUM_FOUNDATION_PILES = 4

#constants suits and ranks
SUITS = ['h', 'd', 'c', 's']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUIT_SYMBOLS = {
    'h': '\u2665',
    'd': '\u2666',
    'c': '\u2663',
    's': '\u2660'
}
MAX_CARDS = 13