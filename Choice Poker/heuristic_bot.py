from player import Player
from hand_eval import hand_type
import random
from game_state import show_error_popup

class HeuristicBot(Player):

    def __init__(self, name, chips=1000):
        super().__init__(name, chips)
    
    def bet(self, game_state, betting_round, last_bet):

        # Cannot bet anymore if current bet is equal to/exceeds amount of chips
        if game_state.bets[self] >= self.chips:
            return 0

        hand_strength = hand_type(self.hand)[0]

        # First round, bot first bet
        if betting_round == 0 and max(game_state.bets.values()) == 0:

            # If two pair or better hand, bet between 50-225
            if hand_strength >= 30:
                multiplier = random.randrange(2, 10, 1) / 2
                amount = min(50 * multiplier, self.chips)
            # If weak hand, bet between 50-125
            else:
                multiplier = random.randrange(2, 6, 1) / 2
                amount = min(50 * multiplier, self.chips)
            
        # First round, bot second bet
        elif betting_round == 0:

            # If a two pair or higher, 50/50 chance of calling or raising by between 50-150 chips
            if hand_strength >= 20:
                
                if random.random() > 0.5:
                    amount = min(last_bet, self.chips)
                else:
                    amount = min(last_bet + random.randrange(50, 150, 10), self.chips)
                
            # If a pair, fold 30% of the time if opponent bets higher than threshold; otherwise call/raise
            elif hand_strength == 20:

                # Bet only up to 40% of total chips on a pair 
                threshold = 0.4 * self.chips

                if last_bet > threshold:
                    if random.random() > 0.30:
                        amount = min(last_bet + random.randrange(0, 50, 10), self.chips)
                    else:
                        amount = 0
                else:
                    amount = min(last_bet + random.randrange(0, 50, 10), self.chips)
            
            # If a high card, fold 75% of the time if opponent bets higher than threshold; otherwise call/raise
            else:

                # Bet only up to 20% of total chips on a high card 
                threshold = 0.2 * self.chips

                if last_bet > threshold:
                    if random.random() > 0.75:
                        amount = min(last_bet + random.randrange(0, 50, 10), self.chips)
                    else:
                        amount = 0
                else:
                    amount = min(last_bet + random.randrange(0, 50, 10), self.chips)
        
        # Every round after first round
        else:

            # Keep betting if two pair hand or better
            if hand_strength >= 30:
                amount = min(last_bet + random.randrange(20, 120, 10), self.chips)
            
            # Moderate betting for pair
            elif hand_strength == 20:

                threshold = 0.6 * self.chips

                # If opponent bet higher than threshold, fold 85% of the time. Otherwise call/raise
                if last_bet > threshold:
                    if random.random() > 0.15:
                        amount = 0
                    else:
                        amount = min(last_bet + random.randrange(0, 50, 10), self.chips)
                    
                # If opponent bet under the threshold, call/raise 85% of the time
                else:
                    if random.random() > 0.85:
                        amount = 0
                    else:
                        amount = min(last_bet + random.randrange(0, 50, 10), self.chips)

            # Conservative betting for high card
            else:

                threshold = 0.15 * self.chips

                # If opponent bet higher than threshold, fold 85% of the time. Otherwise call/raise
                if last_bet > threshold:
                    if random.random() > 0.15:
                        amount = 0
                    else:
                        amount = min(last_bet + random.randrange(0, 50, 10), self.chips)
                    
                # If opponent bet under the threshold, call/raise 85% of the time
                else:
                    if random.random() > 0.85:
                        amount = 0
                    else:
                        amount = min(last_bet + random.randrange(0, 50, 10), self.chips)

        if amount == 0:
            return amount
        elif amount == game_state.bets[self] or amount > self.chips:
            return 0
        else:
            return amount
    
    def discard(self, game_state):
        hand_strength = hand_type(self.hand)
        organized_hand = hand_strength[1:]

        # No discard if hand is straight/flush or better
        if hand_strength[0] >= 50:
            return 0
        
        # Discard lowest 2 cards if high card hand
        elif hand_strength[0] == 10:
            game_state.discard_history[self].append(self.hand[0])
            game_state.discard_history[self].append(self.hand[1])

            self.hand[0] = game_state.deck.draw_card()
            self.hand[1] = game_state.deck.draw_card()
        
        # Discard lowest 2 cards that are not in the pair if a pair hand
        elif hand_strength[0] == 20:
            lowest_values = organized_hand[3:]
            
            # Lowest value cannot be part of the pair otherwise it would be 3 of a kind
            for i in range(len(self.hand)):
                if self.hand[i].value in lowest_values:
                    game_state.discard_history[self].append(self.hand[i])
                    self.hand[i] = game_state.deck.draw_card()
        
        # Discard the card not part of the two pair
        elif hand_strength[0] == 30:
            discard = organized_hand[4]
            for i in range(len(self.hand)):
                if self.hand[i].value == discard:
                    game_state.discard_history[self].append(self.hand[i])
                    self.hand[i] = game_state.deck.draw_card()

        # Discard the two cards not part of the 3 of a kind
        elif hand_strength[0] == 40:
            discard_values = organized_hand[3:]

            for i in range(len(self.hand)):
                if self.hand[i].value in discard_values:
                    game_state.discard_history[self].append(self.hand[i])
                    self.hand[i] = game_state.deck.draw_card()


    
    def pick_ranking(self, game_state):
        hand_strength = hand_type(self.hand)

        if hand_strength[0] >= 20:
            game_state.strongest_wins = True
            game_state.output_log(f"    Strongest hand will win.\n") # log output -----------------------------------
            print("\nThe strongest hand will win\n")
        else:
            game_state.strongest_wins = False
            game_state.output_log(f"    Weakest hand will win.\n") # log output -----------------------------------
            print("\nThe weakest hand will win\n")
        