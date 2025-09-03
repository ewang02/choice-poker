from player import Player
from game_state import show_error_popup

class HumanPlayer(Player):

    def __init__(self, name, chips=1000):
        super().__init__(name, chips)

    """ Returns bet amount """
    def bet(self, game_state, betting_round, last_bet):
        valid = False
        amount = 0

        # Checks that the bet amount is at least 0. Balance checking occurs in GameState as it is
        # lump sump betting rather than gradual raising
        while not valid:
            try:
                amount = int(input("Enter your bet amount. To stop betting, enter 0: "))
            except:
                show_error_popup("Enter a valid bet.")
                continue

            if amount < 0:
                show_error_popup("Enter a valid bet.")
            else:
                valid = True
                break
        
        return amount
    
    def discard(self, game_state):
        print(self.view_hand() + "\n")
        discard_indx = []
        valid = False
        while not valid:
            try:
                numbers = list(map(int, input("Enter the card numbers (1-5) you would like to discard separated by a space. To keep a card, enter 0: ").split()))
            except:
                show_error_popup("Enter a valid discard input.")
                continue

            if len(numbers) != 2:
                show_error_popup("Enter two distinct numbers between 0-5.")
            elif numbers[0] == 0 and numbers[1] == 0:
                valid = True
            elif numbers[0] == numbers[1] or numbers[0] not in [0, 1, 2, 3, 4, 5] or numbers[1] not in [0, 1, 2, 3, 4, 5]:
                show_error_popup("Enter two distinct numbers between 0-5.")
            else:
                valid = True
                for i in numbers:
                    if i != 0:
                        discard_indx.append(i - 1)

        for i in discard_indx:
            game_state.discard_history[self].append(self.hand[i])
            self.hand[i] = game_state.deck.draw_card()

        self.hand.sort(key=lambda x: x.value)
        print("\n" + self.view_hand() + "\n")

    def pick_ranking(self, game_state):
        valid = False
        rank = ""
        while not valid:
            rank = input(f"{self.name} was the highest bettor. Enter 'strongest' or 'weakest' to determine which type of hand wins: ")
            if rank != 'strongest' and rank != 'weakest':
                show_error_popup("Enter a valid choice.")  
            else:
                valid = True
        
        if rank == 'strongest':
            game_state.strongest_wins = True
            game_state.output_log(f"    Strongest hand will win.\n") # log output -----------------------------------
            print("\nThe strongest hand will win\n")
        else:
            game_state.strongest_wins = False
            game_state.output_log(f"    Weakest hand will win.\n") # log output -----------------------------------
            print("\nThe weakest hand will win\n")