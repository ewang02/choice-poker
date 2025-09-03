from deck import Deck
from hand_eval import compare_hands
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()  # Hide the main tkinter window

# Error popup for invalid user input to not clutter console
def show_error_popup(message):
    messagebox.showerror("Error", message)

class GameState:

    def __init__(self, players):
        self.deck = Deck() 
        self.round_num = 1
        self.pot = 0
        self.players = players
        self.highest_bettor = None
        self.strongest_wins = True
        self.discard_history = {players[0]: [], players[1]: []} # dictionary mapping to each players' discarded cards to be shown
        self.bets = {players[0]: 0, players[1]: 0} # dictionary mapping to each players' bets

    def initial_deal(self):
        # Make sure players have enough chips to play
        for player in self.players:
            if player.chips <= 0:
                show_error_popup(f"{player.name} has insufficient funds for a new game.")
                quit()

        print("-------------------------------")
        print(f"        ROUND {self.round_num}")
        print("-------------------------------\n")
        print(f"Player order: {self.players[0].name} (${self.players[0].chips}), {self.players[1].name} (${self.players[1].chips})\n")

        # Record logs
        self.output_log(f"ROUND {self.round_num}\n") # log output ------------------------------------
        self.output_log(f"    Player order: {self.players[0].name} (${self.players[0].chips}), {self.players[1].name} (${self.players[1].chips})\n") # log output ------------------------------------

        # Give each player 5 cards
        for player in self.players:
            for i in range(5):
                player.hand.append(self.deck.draw_card())
            player.hand.sort(key=lambda x: x.value)

            self.output_log(f"    {player.name} initial hand: {player.log_hand()}\n") # log output ------------------------------------

    def discard_phase(self):
        print("-------------------------------")
        print("        DISCARD PHASE")
        print("-------------------------------\n")

        # Call each players' discard function; gets input on which cards to discard and
        # modifies the game state inside that function
        for player in self.players:
            player.discard(self)

        # Function to reveal a player's discarded cards
        def reveal_discards(player):
            discard_string = ""
            for card in self.discard_history[player]:
                discard_string += str(card) + "   "
            if len(self.discard_history[player]) == 0:
                discard_string = "None"

            print(f"{player.name} discarded: {discard_string}\n")
            self.output_log(f"    {player.name} discarded: {discard_string}\n") # log output ------------------------------------
        
        reveal_discards(self.players[0])
        reveal_discards(self.players[1])
        self.output_log(f"    {self.players[0].name} new hand: {self.players[0].log_hand()}\n") # log output ------------------------------------
        self.output_log(f"    {self.players[1].name} new hand: {self.players[1].log_hand()}\n") # log output ------------------------------------
    
    def betting_phase(self):
        print("-------------------------------")
        print("        BETTING PHASE")
        print("-------------------------------\n")

        # Set loop variables to continue the betting loop until bets are done
        finished = False
        betting_round = 0

        # Returns the bet of the player whose turn it is
        def betting_turn(bettor, opponent, last_bet):
            valid_bet = False
            current_bet = 0

            # If player does not have enough chips to call, must go all in
            min_call = 0
            if bettor.chips <= self.bets[opponent]:
                min_call = bettor.chips
            else:
                min_call = max(self.bets.values())

            print(f"{bettor.name} turn to bet --- Minimum call: {min_call} --- Balance: ${bettor.chips}\n")
            while not valid_bet:
                current_bet = bettor.bet(self, betting_round, last_bet)
                
                # Can't bet more than player has
                if current_bet > bettor.chips:
                    show_error_popup("Insufficient chips. Please enter a new bet.")
                    continue

                # Cannot bet 0 on the first round
                if betting_round == 0 and current_bet == 0:
                    show_error_popup("Must bet on the first round.")
                    continue
                # Betting 0 ends turn and goes to showdown if current bet is less than opponent's
                elif current_bet == 0:
                    valid_bet = True
                    if self.bets[bettor] < self.bets[opponent]:
                        self.highest_bettor = opponent
                    break
                # New bets must be greater than previous bets
                elif current_bet <= self.bets[bettor]:
                    show_error_popup("You must bet higher than your current bet amount.")
                    continue
                # Must bet at least the minimum call amount
                elif current_bet < min_call:
                    show_error_popup(f"You must bet at least {min_call} chips.")
                    continue
                # Updates new bet and pot
                else:
                    self.bets[bettor] = current_bet
                    self.pot = sum(self.bets.values())
                    valid_bet = True
                    break

            self.output_log(f"    {bettor.name} bet: {current_bet}\n") # log output -----------------------------------
            print(f"    {bettor.name} bet: {current_bet}\n")
            return current_bet
                
        # Loops until player with lower bet 'folds' or until both players stop betting
        first_bet, second_bet = 0, 0
        while not finished:
            first_bet = betting_turn(self.players[0], self.players[1], second_bet)
            
            if self.highest_bettor is not None:
                break

            second_bet = betting_turn(self.players[1], self.players[0], first_bet)
            if first_bet == 0 and second_bet == 0:
                finished = True
                break
            betting_round += 1

        # Deducts the bets from the players' balances
        for player in self.players:
            player.decrement_chips(self.bets[player])

        print("Total pot: " + str(self.pot) + "\n")
        self.output_log(f"    Total pot: {self.pot}\n") # log output -----------------------------------

        # Checks to see which player bet more; in case of tie, player who bet first chooses
        if self.bets[self.players[0]] > self.bets[self.players[1]]:
            self.output_log(f"    {self.players[0].name} wins betting.\n") # log output -----------------------------------
            self.players[0].pick_ranking(self)
        elif self.bets[self.players[0]] < self.bets[self.players[1]]:
            self.output_log(f"    {self.players[1].name} wins betting.\n") # log output -----------------------------------
            self.players[1].pick_ranking(self)
        else:
            self.output_log(f"    Tied bets. {self.players[0].name} chooses.\n") # log output -----------------------------------
            print(f"Bets were tied. {self.players[0].name} chooses.")
            print("")
            self.players[0].pick_ranking(self)
                    
    def showdown_phase(self):
        print("-------------------------------")
        print("           SHOWDOWN")
        print("-------------------------------\n")
        # Displays everyone's hand
        for player in self.players:
            print(player.view_hand() + "\n")

        # Compares hands and determines winner based on win condition
        winner = None
        if self.strongest_wins:
            winner = compare_hands(self.players[0].hand, self.players[1].hand, 0)
        else:
            winner = compare_hands(self.players[0].hand, self.players[1].hand, 1)
        
        # In case of tie, players refunded their bets. If the winning player bet
        # less than the other, they can only win the same amount they bet from the other player
        if winner == 0:
            print("\nTie. Players are refunded their bets.\n")

            self.output_log("    Tie. Players are refunded their bets.\n") # log output -----------------------------------

            self.players[0].increment_chips(self.bets[self.players[0]])
            self.players[1].increment_chips(self.bets[self.players[1]])

            self.output_log("    New balances:\n") # log output -----------------------------------
            for player in self.players:
                self.output_log(f"        {player.name}: {player.chips} (+ 0)\n") # log output -----------------------------------

        elif winner == self.players[0].hand:
            print(f"\n{self.players[0].name} wins\n")

            self.output_log(f"    {self.players[0].name} wins\n") # log output -----------------------------------
            self.output_log("    New balances:\n") # log output -----------------------------------

            if self.bets[self.players[0]] < self.bets[self.players[1]]:
                self.players[0].increment_chips(2 * self.bets[self.players[0]])
                self.players[1].increment_chips(self.bets[self.players[1]] - self.bets[self.players[0]])

                self.output_log(f"        {self.players[0].name}: {self.players[0].chips} (+ {self.bets[self.players[0]]})\n") # log output -----------------------------------
                self.output_log(f"        {self.players[1].name}: {self.players[1].chips} (- {self.bets[self.players[0]]})\n") # log output -----------------------------------
            else:
                self.players[0].increment_chips(self.bets[self.players[0]] + self.bets[self.players[1]])

                self.output_log(f"        {self.players[0].name}: {self.players[0].chips} (+ {self.bets[self.players[1]]})\n") # log output -----------------------------------
                self.output_log(f"        {self.players[1].name}: {self.players[1].chips} (- {self.bets[self.players[1]]})\n") # log output -----------------------------------
        else:
            print(f"\n{self.players[1].name} wins\n")

            self.output_log(f"    {self.players[1].name} wins\n") # log output -----------------------------------
            self.output_log("    New balances:\n") # log output -----------------------------------

            if self.bets[self.players[1]] < self.bets[self.players[0]]:
                self.players[1].increment_chips(2 * self.bets[self.players[1]])
                self.players[0].increment_chips(self.bets[self.players[0]] - self.bets[self.players[1]])

                self.output_log(f"        {self.players[0].name}: {self.players[0].chips} (- {self.bets[self.players[1]]})\n") # log output -----------------------------------
                self.output_log(f"        {self.players[1].name}: {self.players[1].chips} (+ {self.bets[self.players[1]]})\n") # log output -----------------------------------
            else:
                self.players[1].increment_chips(self.bets[self.players[1]] + self.bets[self.players[0]])

                self.output_log(f"        {self.players[0].name}: {self.players[0].chips} (- {self.bets[self.players[0]]})\n") # log output -----------------------------------
                self.output_log(f"        {self.players[1].name}: {self.players[1].chips} (+ {self.bets[self.players[0]]})\n") # log output -----------------------------------

        # Display the new player chip balances
        print("Player balances:")
        print(f"    {self.players[0].name}: {self.players[0].chips}")
        print(f"    {self.players[1].name}: {self.players[1].chips}\n")

        self.reset_game()

    # Run all game phases
    def run_full_game(self):
        self.initial_deal()
        self.discard_phase()
        self.betting_phase()
        self.showdown_phase()
        self.run_full_game()
        
    # Resets game with new deck and clears bets
    def reset_game(self):
        self.round_num += 1
        self.deck = Deck()
        self.pot = 0
        self.highest_bettor = None
        self.strongest_wins = True
        self.discard_history = {self.players[0]: [], self.players[1]: []}
        self.bets = {self.players[0]: 0, self.players[1]: 0}
        for player in self.players:
            player.reset()
        self.players = [self.players[1], self.players[0]]
        print("")
        print("Rotating player order")
        print("")

    def output_log(self, msg):
        with open("output.txt", "a") as f:
            f.write(f"{msg}\n")