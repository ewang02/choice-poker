from game_state import GameState
from human_player import HumanPlayer
from random_bot import RandomBot
from heuristic_bot import HeuristicBot
from player import Player
from deck import Deck
from hand_eval import hand_type, compare_hands

def run_test_game():
    # Step 1: Setup players
    p1 = HumanPlayer("Edward", 2000)
    p2 = HeuristicBot("Yumeko", 2000)
    players = [p1, p2]

    # Step 2: Create and run the game state
    game = GameState(players)
    game.run_full_game()  # You likely wrote this as a full sequence controller

def pair_type(hand):
    return hand_type(hand)[1] - 2

def winning_hands():
    p1 = Player("Edward")
    p2 = Player("Yumeko")
    strongest_win = True
    players = [p1, p2]
    win_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pair_wins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(100000):
        deck = Deck()
        for player in players:
            new_hand = []
            for i in range(5):
                new_hand.append(deck.draw_card())
            player.hand = new_hand
        
        if strongest_win:
            winning_hand = compare_hands(p1.hand, p2.hand, 0)
        else:
            winning_hand = compare_hands(p1.hand, p2.hand, 1)
        
        if winning_hand == p1.hand:
            match hand_type(p1.hand)[0]:
                case 10:
                    win_array[0] += 1
                case 20:
                    win_array[1] += 1
                    pair_wins[pair_type(p1.hand)] += 1
                case 30:
                    win_array[2] += 1
                case 40:
                    win_array[3] += 1
                case 50:
                    win_array[4] += 1
                case 60:
                    win_array[5] += 1
                case 70:
                    win_array[6] += 1
                case 80:
                    win_array[7] += 1
                case 90:
                    win_array[8] += 1
                case 100:
                    win_array[9] += 1
        elif winning_hand == p2.hand:
            match hand_type(p2.hand)[0]:
                case 10:
                    win_array[0] += 1
                case 20:
                    win_array[1] += 1
                    
                    pair_wins[pair_type(p2.hand)] += 1

                case 30:
                    win_array[2] += 1
                case 40:
                    win_array[3] += 1
                case 50:
                    win_array[4] += 1
                case 60:
                    win_array[5] += 1
                case 70:
                    win_array[6] += 1
                case 80:
                    win_array[7] += 1
                case 90:
                    win_array[8] += 1
                case 100:
                    win_array[9] += 1

    with open("data.txt", "a") as f:
        f.write("Total win distribution:\n")
        f.write(f"  High Card: {win_array[0]} {win_array[0] / 100}%\n")
        f.write(f"  Pair: {win_array[1]} {win_array[1] / 100}%\n")
        f.write(f"  Two Pair: {win_array[2]} {win_array[2] / 100}%\n")
        f.write(f"  Three of a Kind: {win_array[3]} {win_array[3] / 100}%\n")
        f.write(f"  Straight: {win_array[4]} {win_array[4] / 100}%\n")
        f.write(f"  Flush: {win_array[5]} {win_array[5] / 100}%\n")
        f.write(f"  Full House: {win_array[6]} {win_array[6] / 100}%\n")
        f.write(f"  Four of a Kind: {win_array[7]} {win_array[7] / 100}%\n")
        f.write(f"  Straight Flush: {win_array[8]} {win_array[8] / 100}%\n")
        f.write(f"  Royal Flush: {win_array[9]} {win_array[9] / 100}%\n")
        f.write(f"Pair win distribution:\n")
        f.write(f"  2:{pair_wins[0]} {pair_wins[0] / win_array[1] * 100}%\n")
        f.write(f"  3:{pair_wins[1]} {pair_wins[1] / win_array[1] * 100}%\n")
        f.write(f"  4:{pair_wins[2]} {pair_wins[2] / win_array[1] * 100}%\n")
        f.write(f"  5:{pair_wins[3]} {pair_wins[3] / win_array[1] * 100}%\n")
        f.write(f"  6:{pair_wins[4]} {pair_wins[4] / win_array[1] * 100}%\n")
        f.write(f"  7:{pair_wins[5]} {pair_wins[5] / win_array[1] * 100}%\n")
        f.write(f"  8:{pair_wins[6]} {pair_wins[6] / win_array[1] * 100}%\n")
        f.write(f"  9:{pair_wins[7]} {pair_wins[7] / win_array[1] * 100}%\n")
        f.write(f"  10:{pair_wins[8]} {pair_wins[8] / win_array[1] * 100}%\n")
        f.write(f"  J:{pair_wins[9]} {pair_wins[9] / win_array[1] * 100}%\n")
        f.write(f"  Q:{pair_wins[10]} {pair_wins[10] / win_array[1] * 100}%\n")
        f.write(f"  K:{pair_wins[11]} {pair_wins[11] / win_array[1] * 100}%\n")
        f.write(f"  A:{pair_wins[12]} {pair_wins[12] / win_array[1] * 100}%\n")

    """
    with open("data.txt", "a") as f:
        f.write(f"{msg}\n")
    """

if __name__ == "__main__":
    run_test_game()