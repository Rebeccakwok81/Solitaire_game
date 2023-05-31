import pygame
from pygame.locals import *
from constants import *
from game import Game
from talonpile import TalonPile
from pile import Pile
from tableau import TableauPile
import sys

class SolitaireUI:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.talonpile = TalonPile()
        self.tableau_piles = TableauPile()
        self.window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.card_images = self.load_card_images()
        self.selected_pile = None

    def load_card_images(self):
        CARDS_PATH = f"Playing Cards Asset\Cards\Modern"
        card_images = {}
        card_width, card_height = 115, 175

        for suit in (SUITS):
            for rank in (RANKS):
                card_name = f"{rank}{suit}"
                if rank == '10':
                    filename = f"{rank}{suit}.png"
                else:
                    filename = f"{rank}{suit}.png"
                # filepath = os.path.join(CARDS_PATH, filename)
                filepath = f"{CARDS_PATH}\{filename}"
            
                try:
                    image = pygame.image.load(filepath)
                    image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
                    card_images[card_name] = image
                except pygame.error:
                    print(f"Error loading image: {filepath}")

        # load the back image, going with 03
        back_image_path = f"Playing Cards Asset\Backs\Card-Back-03.png"
        try:
            back_image = pygame.image.load(back_image_path)
            back_image = pygame.transform.scale(back_image, (CARD_WIDTH, CARD_HEIGHT))
            card_images['back.png'] = back_image
        except pygame.error:
            print(f"Error loading back image: {back_image_path}")

        # load empty image for foundation pile and talon pile
        empty_holder = f"Playing Cards Asset\empty_holder.png"
        try:
            e_image = pygame.image.load(empty_holder)
            e_image = pygame.transform.scale(e_image, (CARD_WIDTH, CARD_HEIGHT))
            card_images['empty_holder.png'] = e_image
        except pygame.error:
            print(f"Error loading back image: {empty_holder}")

        return card_images

    def draw(self):
        self.window_surface.fill(BACKGROUND_COLOR)  # green background
    
    # draw empty holder images for foundation pile and talon pile
        empty_holder_image = self.card_images['empty_holder.png']

        foundation_pile_positions = [(TABLEAU_LEFT_MARGIN + (i + 3) * TABLEAU_COLUMN_WIDTH, FOUNDATION_TOP_ROW_Y) for i in range(4)]
        for position in foundation_pile_positions:
            self.window_surface.blit(empty_holder_image, position)

        talon_pile_position = (TABLEAU_LEFT_MARGIN + TABLEAU_COLUMN_WIDTH, FOUNDATION_TOP_ROW_Y)
        self.window_surface.blit(empty_holder_image, talon_pile_position)

    # draw tableau piles
        for i, pile in enumerate(self.game.tableau):
            self.draw_pile_cards(pile, (TABLEAU_LEFT_MARGIN + i*TABLEAU_COLUMN_WIDTH, TABLEAU_BOTTOM_ROW_Y))

    # draw foundation, talon, and stockpile cards
        for i, pile in enumerate(self.game.foundation):
            self.draw_pile_cards(pile, (TABLEAU_LEFT_MARGIN + (i+3)*TABLEAU_COLUMN_WIDTH, FOUNDATION_TOP_ROW_Y))

        self.draw_pile_cards(self.game.talonpile, (TABLEAU_LEFT_MARGIN + TABLEAU_COLUMN_WIDTH, FOUNDATION_TOP_ROW_Y))
        self.draw_pile_cards(self.game.stockpile, (TABLEAU_LEFT_MARGIN, FOUNDATION_TOP_ROW_Y), face_up=False)

        pygame.display.flip()

    def draw_pile_cards(self, pile, position, face_up=False):
        x, y = position
        deck_x = x + CARD_WIDTH // 2
        deck_y = FOUNDATION_TOP_ROW_Y + CARD_HEIGHT // 2

        if pile == self.game.stockpile:
            if not face_up:
                back_image = self.card_images['back.png']
                back_rect = back_image.get_rect(center=(deck_x, deck_y))
                self.window_surface.blit(back_image, back_rect)
            else:
                return
        else:
            for i, card in enumerate(pile.cards):
                if pile == self.game.stockpile and not face_up and i != len(pile.cards) - 1:
                    continue

                if card.face_up == face_up:
                    image = self.card_images[f'{card.rank}{card.suit}']
                else:
                    image = self.card_images['back.png']
                
                card_x = x
                
                if pile == self.game.talonpile:
                    card_y = y
                else:
                    card_y = y + i * 15

                self.window_surface.blit(image, (card_x, card_y))

    def handle_click(self, position):
        x, y = position

        for i, pile in enumerate(self.game.tableau):
            pile_x = TABLEAU_LEFT_MARGIN + i * TABLEAU_COLUMN_WIDTH
            pile_y = TABLEAU_BOTTOM_ROW_Y

            # check if the click occurred within the bounding box of the tableau pile
            if pile_x <= x < pile_x + CARD_WIDTH and pile_y <= y < pile_y + len(pile.cards) * 30:
                # if a tableau pile was clicked
                if self.selected_pile is None:
                    # select the clicked pile as the selected pile
                    self.selected_pile = pile
                    self.selected_cards = pile.get_selected_cards(position)
                else:
                    # move the selected cards from the selected pile to the clicked pile
                    if pile.is_valid_move(self.selected_pile.peek_top_card()):
                        pile.add_cards(self.selected_cards)
                        self.selected_pile.remove_selected_cards()
                    else:
                        print("Invalid move. Cannot move cards to this pile.")
                
                break
        else:
            # handle the click-and-drag movement of cards
            if self.selected_pile is not None:
                dx = position[0] - self.click_position[0]
                dy = position[1] - self.click_position[1]
                self.selected_pile.move_selected_cards(dx, dy)

        # set the coordinates for the deck and the size of a card
        stockpile_x = TABLEAU_LEFT_MARGIN + TABLEAU_COLUMN_WIDTH // 2 - CARD_WIDTH // 2
        stockpile_y = FOUNDATION_TOP_ROW_Y

        # define the bounding box for the deck
        deck_left = stockpile_x
        deck_right = stockpile_x + CARD_WIDTH
        deck_top = stockpile_y
        deck_bottom = stockpile_y + CARD_HEIGHT

        # check if the click occurred within the bounding box of the deck
        if deck_left <= x <= deck_right and deck_top <= y <= deck_bottom:
            # The deck was clicked
            if not self.game.stockpile.is_empty():
                # move the top card from the stockpile to the talonpile (waste pile)
                card = self.game.stockpile.deal_card()
                card.flip()
                self.game.talonpile.add_card(card)
                print("Deck clicked, card moved to waste pile.")  # debug message
            else:
                print("Deck clicked but it's empty.")  # debug message
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            self.draw()
            pygame.display.flip()

