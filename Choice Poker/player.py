from hand_eval import hand_type

class Player:

    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        self.discarded_cards = []
    
    def reset(self):
        self.hand = []
        self.discarded_cards = []

    def increment_chips(self, n):
        self.chips += n

    def decrement_chips(self, n):
        self.chips -= n
    

    """ Displays the cards in player's hand """
    def view_hand(self):
        hand_string = ""
        for card in self.hand:
            hand_string += str(card) + "   "
        
        strength = hand_type(self.hand)
        strength_name = ""
        match strength[0]:
            case 10:
                strength_name = "High Card"
            case 20:
                strength_name = "Pair"
            case 30:
                strength_name = "Two Pair"
            case 40:
                strength_name = "Three of a Kind"
            case 50:
                strength_name = "Straight"
            case 60:
                strength_name = "Flush"
            case 70:
                strength_name = "Full House"
            case 80:
                strength_name = "Four of a Kind"
            case 90:
                strength_name = "Straight Flush"
            case 100:
                strength_name = "Royal Flush"
            case _:
                strength_name = "Error determining strength"
        
        return f"{self.name} hand: {hand_string}|   Hand strength: {strength_name}"
    
    # Function for recording hands in the output logs
    def log_hand(self):
        hand_string = ""
        for card in self.hand:
            hand_string += str(card) + "   "
        
        strength = hand_type(self.hand)
        strength_name = ""
        match strength[0]:
            case 10:
                strength_name = "High Card"
            case 20:
                strength_name = "Pair"
            case 30:
                strength_name = "Two Pair"
            case 40:
                strength_name = "Three of a Kind"
            case 50:
                strength_name = "Straight"
            case 60:
                strength_name = "Flush"
            case 70:
                strength_name = "Full House"
            case 80:
                strength_name = "Four of a Kind"
            case 90:
                strength_name = "Straight Flush"
            case 100:
                strength_name = "Royal Flush"
            case _:
                strength_name = "Error determining strength"
        
        return f"{hand_string}|   Hand strength: {strength_name}"
            

    def bet(self, game_state, betting_round, last_bet):
        raise NotImplementedError("Not all subclasses implemented")
    
    def discard(self, game_state):
        raise NotImplementedError("Not all subclasses implemented")
    
    def pick_ranking(self, game_state):
        raise NotImplementedError("Not all subclasses implemented")
    