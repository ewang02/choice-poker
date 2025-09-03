import random

class Card:

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __str__(self):
        suit_icon = ""
        if self.suit == 'club':
            suit_icon = "♣"
        elif self.suit == 'spade':
            suit_icon = "♠"
        elif self.suit == 'heart':
            suit_icon = "♡"
        elif self.suit == 'diamond':
            suit_icon = "♢"

        value_symbol = self.value
        if self.value == 11:
            value_symbol = "J"
        elif self.value == 12:
            value_symbol = "Q"
        elif self.value == 13:
            value_symbol = "K"
        elif self.value == 14:
            value_symbol = "A"
            
        return str(value_symbol) + suit_icon

class Deck:
    
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    suits = ['club', 'spade', 'heart', 'diamond']

    # Construct deck of 52 cards
    cards = []
    for val in values:
        for suit in suits:
            cards.append(Card(val, suit))

    def __init__(self):
        # Create deck of 52 cards, then shuffle into its own order
        self.order = list(Deck.cards)
        random.shuffle(self.order)

    def shuffle(self):
        random.shuffle(self.order)
    
    def draw_card(self):
        if self.order:
            return self.order.pop(0)
        else:
            print("No more cards remaining.")


