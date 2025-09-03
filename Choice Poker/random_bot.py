from player import Player
import random

class RandomBot(Player):

    def __init__(self, name, chips=1000):
        super().__init__(name, chips)

    def bet(self, game_state, betting_round, last_bet):
        opponent = None
        for player in game_state.players:
            if player != self:
                opponent = player
        opponent_bet = game_state.bets[opponent]

        # Go all-in if low chips
        if self.chips <= 50:
            return self.chips
        
        # If bot starts the betting, bet 50 chips or less
        if betting_round == 0 and max(game_state.bets.values()) == 0:
            if self.chips >= 50:
                return 50
            else:
                return self.chips
        # If opponent starts the betting in round 1, raise by 20 or all in if not enough chips
        elif betting_round == 0 and opponent_bet != 0:
            if self.chips >= opponent_bet + 20:
                return opponent_bet + 20
            else:
                return min(self.chips, opponent_bet)
        else:
            if last_bet == 0:
                if game_state.bets[self] > opponent_bet:
                    return 0

            # 25% of folding outside of round 1
            if random.randrange(1, 100) > 75:
                return 0
            else:
                raise_amt = random.randrange(10, 50, 10)
                
                # If can afford to raise by raise_amt, then raise
                if self.chips >= opponent_bet + raise_amt:
                    return opponent_bet + raise_amt
                # If cannot afford to raise, then 50/50 all in or fold
                else:
                    if random.randrange(1, 100) <= 50:
                        return 0
                    else:
                        return self.chips
        

    
    def discard(self, game_state):
        # Equal chance of discarding either 0, 1, or 2 cards, all of which have an equal chance of being discarded
        choice = random.choice([0, 1, 2])
        if choice == 0:
            return 0
        elif choice == 1:
            discard_card = random.choice([0, 1, 2, 3, 4])
            game_state.discard_history[self].append(self.hand[discard_card])
            self.hand[discard_card] = game_state.deck.draw_card()
        elif choice == 2:
            discard_card = random.sample([0, 1, 2, 3, 4], 2)
            for i in discard_card:
                game_state.discard_history[self].append(self.hand[i])
                self.hand[i] = game_state.deck.draw_card()
                  
        self.hand.sort(key=lambda x: x.value)

    def pick_ranking(self, game_state):
        print(f"{self.name} was the highest bettor. Choosing win condition...")

        # 50/50 chance of choosing strongest or weakest
        choice = random.choice(['strongest', 'weakest'])
        if choice == 'strongest':
            game_state.strongest_wins = True
            game_state.output_log(f"    Strongest hand will win.\n") # log output -----------------------------------
            print("The strongest hand will win")
            print("")
        else:
            game_state.strongest_wins = False
            game_state.output_log(f"    Weakest hand will win.\n") # log output -----------------------------------
            print("The weakest hand will win")
            print("")
