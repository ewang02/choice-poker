def royal_flush(values, suits):
    flush = True
    for i in range(1, len(suits)):
        if suits[i] != suits[i - 1]:
            flush = False
    if flush:
        if values == [10, 11, 12, 13, 14]:
            return [100, 14, 13, 12, 11, 10]
        else:
            return [0, 0, 0, 0, 0, 0]
    else:
        return [0, 0, 0, 0, 0, 0]

def straight_flush(values, suits):
    flush = True
    for i in range(1, len(suits)):
        if suits[i] != suits[i - 1]:
            flush = False

    straight = True
    for i in range(1, len(values)):
        if values[i] != values[i - 1] + 1:
            straight = False
    if values == [2, 3, 4, 5, 14]:
        straight = True

    if straight and flush:
        return [90] + list(values)
    else:
        return [0, 0, 0, 0, 0, 0]
    
def four_of_a_kind(values, suits):
    four_kind = True
    for i in range(len(values) - 1):
        if values[i] != values[0]:
            four_kind = False

    if four_kind:
        return [80] + list(values)
    
    four_kind = True
    for i in range(1, len(values)):
        if values[i] != values[1]:
            four_kind = False
    
    if four_kind:
        return [80] + values[1:] + [values[0]]
    else:
        return [0, 0, 0, 0, 0, 0]

def full_house(values, suits):
    three_kind = True
    for i in range(len(values) - 2):
        if values[0] != values[i]:
            three_kind = False
    
    if three_kind:
        if values[3] == values[4]:
            return [70] + list(values)
        else:
            return [0, 0, 0, 0, 0, 0]
    else:
        three_kind = True
        for i in range(2, len(values)):
            if values[2] != values[i]:
                three_kind = False
        if three_kind:
            if values[0] == values[1]:
                return [70] + values[2:] + values[:2]
        return [0, 0, 0, 0, 0, 0]

def flush(values, suits):
    flush = True
    for i in range(1, len(suits)):
        if suits[i] != suits[i - 1]:
            flush = False
    
    if flush:
        return [60] + sorted(values, reverse=True)
    else:
        return [0, 0, 0, 0, 0, 0]
    
def straight(values, suits):
    straight = True
    for i in range(1, len(values)):
        if values[i] != values[i - 1] + 1:
            straight = False
    if values == [2, 3, 4, 5, 14]:
        straight = True
    
    if straight:
        return [50] + list(values)
    else:
        return [0, 0, 0, 0, 0, 0]

def three_of_a_kind(values, suits):
    three_kind = True
    for i in range(len(values) - 2):
        if values[0] != values[i]:
            three_kind = False
    
    if three_kind:
        return [40] + values[:3] + [values[4]] + [values[3]]
    
    three_kind = True
    for i in range(1, len(values) - 1):
        if values[1] != values[i]:
            three_kind = False
    
    if three_kind:
        return [40] + values[1:4] + [values[4]] + [values[0]]

    three_kind = True
    for i in range(2, len(values)):
        if values[2] != values[i]:
            three_kind = False

    if three_kind:
        return [40] + values[2:] + [values[1]] + [values[0]] 
    
    return [0, 0, 0, 0, 0, 0]

def two_pair(values, suits):
    num_pairs = 0
    pair_indices = []
    for i in range(len(values) - 1):
        count = 1
        for j in range(i + 1, len(values)):
            if values[i] == values[j]:
                pair_indices.append([i, j])
                count += 1
        if count > 2:
            return [0, 0, 0, 0, 0, 0]
        elif count == 2:
            num_pairs += 1
    if num_pairs != 2:
        return [0, 0, 0, 0, 0, 0]
    else:
        single_card = 0
        for i in range(len(values)):
            if i not in pair_indices[0] and i not in pair_indices[1]:
                single_card = values[i]
                break
        return [30] + [values[pair_indices[1][0]]] + [values[pair_indices[1][1]]] + [values[pair_indices[0][0]]] + [values[pair_indices[0][1]]] + [single_card]

def pair(values, suits):
    num_pairs = 0
    pair_indices = []
    for i in range(len(values) - 1):
        count = 1
        for j in range(i + 1, len(values)):
            if values[i] == values[j]:
                pair_indices.append(i)
                pair_indices.append(j)
                count += 1
        if count > 2:
            return [0, 0, 0, 0, 0, 0]
        elif count == 2:
            num_pairs += 1
    if num_pairs != 1:
        return [0, 0, 0, 0, 0, 0]
    else:
        single_cards = []
        for i in range(len(values)):
            if i not in pair_indices:
                single_cards.append(values[i])
        single_cards.sort(reverse=True)
        return [20] + [values[pair_indices[0]]] + [values[pair_indices[1]]] + list(single_cards)
    
def high_card(values, suits):
    return [10] + list(sorted(values, reverse=True))


# Determines type of hand; pass in hand as an array of Card objects
def hand_type(hand):

    # Get the values and suits of the cards in the hand
    values = []
    suits = []
    for card in hand:
        values.append(card.value)
        suits.append(card.suit)
    values.sort()

    strength = [0, 0, 0, 0, 0, 0]
    if royal_flush(values, suits) != [0, 0, 0, 0, 0, 0]:
        strength = royal_flush(values, suits)
    elif straight_flush(values, suits) != [0, 0, 0, 0, 0, 0]:
        strength = straight_flush(values, suits)
    elif four_of_a_kind(values, suits) != [0, 0, 0, 0, 0, 0]:
        strength = four_of_a_kind(values, suits)
    elif full_house(values, suits) != [0, 0, 0, 0, 0, 0]:
        strength = full_house(values, suits)
    elif flush(values, suits) != [0, 0, 0, 0, 0, 0]:
        strength = flush(values, suits)
    elif straight(values, suits) != [0, 0, 0, 0, 0, 0]:
        strength = straight(values, suits)
    elif three_of_a_kind(values, suits) != [0, 0, 0, 0, 0, 0]:
        strength = three_of_a_kind(values, suits)
    elif two_pair(values, suits) != [0, 0, 0, 0, 0, 0]:
        strength = two_pair(values, suits)
    elif pair(values, suits) != [0, 0, 0, 0, 0, 0]:
        strength = pair(values, suits)
    else:
        strength = high_card(values, suits)
    
    return strength

# Takes two hands and outputs the stronger one. Ranking = 0 means the strongest hand wins while ranking = 1 means the weakest hand wins
def compare_hands(hand1, hand2, ranking=0):
    hand1_strength, hand2_strength = hand_type(hand1), hand_type(hand2)
    
    for i in range(len(hand1_strength)):
        if hand1_strength[i] > hand2_strength[i]:
            if ranking == 0:
                return hand1
            else:
                return hand2
        elif hand1_strength[i] < hand2_strength[i]:
            if ranking == 0:
                return hand2
            else:
                return hand1
            
    return 0