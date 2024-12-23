import copy

#Exercise 1 - Spacemon Competition

'''
This exercise is a battle simulator for two teams of Spacemons. Each Spacemon has three powers represented as a tuple -- 
a planet type, energy, and attack power. The planets have a special table that shows how effective one planet is against another (mult_table). 
The battle happens one-on-one, with a Spacemon from team 1 fighting a Spacemon from team 2. 
They take turns attacking each other until one of them runs out of energy. 
The winner of the fight moves on to battle the next Spacemon from the other team. 
The battle keeps going until one team has no Spacemons left. If team 1 defeats all of team 2's Spacemons, 
the function returns True; otherwise, it returns False. 
The energy levels of the winning Spacemons are updated after each battle, and the winning Spacemon does not regenerate energy.
'''

def exercise1(roster1, roster2):

    # This table shows how strong each planet is against others
    mult_table = {
        'Mercury': {'Mercury': 1, 'Venus': 2, 'Earth': 1, 'Mars': 0.5},
        'Venus': {'Mercury': 0.5, 'Venus': 1, 'Earth': 2, 'Mars': 1},
        'Earth': {'Mercury': 1, 'Venus': 0.5, 'Earth': 1, 'Mars': 2},
        'Mars': {'Mercury': 2, 'Venus': 1, 'Earth': 0.5, 'Mars': 1},
    }
    
    # Start with the first Spacemon from both teams
    index1, index2 = 0, 0
    
    # Keep battling while both teams still have Spacemons left
    while index1 < len(roster1) and index2 < len(roster2):

        # Get the current Spacemons from each team
        smon1 = roster1[index1]
        smon2 = roster2[index2]
        
        # Break down the details of each Spacemon
        planet1, energy1, power1 = smon1  # Team 1's Spacemon
        planet2, energy2, power2 = smon2  # Team 2's Spacemon
        
        # These two Spacemons fight until one runs out of energy
        while energy1 > 0 and energy2 > 0:
            # Team 1's Spacemon attacks first
            energy2 -= mult_table[planet1][planet2] * power1
            if energy2 <= 0:  # If Team 2's Spacemon runs out of energy, stop the fight
                break
            # Team 2's Spacemon attacks next
            energy1 -= mult_table[planet2][planet1] * power2
        
        # Check who won the fight
        if energy1 > 0:

            # Team 1's Spacemon wins, so move to the next Spacemon in Team 2
            index2 += 1

            # Update Team 1's Spacemon with its remaining energy
            roster1[index1] = (planet1, energy1, power1)

        else:
            # Team 2's Spacemon wins, so move to the next Spacemon in Team 1
            index1 += 1

            # Update Team 2's Spacemon with its remaining energy
            roster2[index2] = (planet2, energy2, power2)
    
    # If Team 2 has no Spacemons left, Team 1 wins, return True. Otherwise, return False
    return index2 == len(roster2)



# Exercise 2 - Five Letter Unscramble

'''
This exercise is a smart helper that figures out how many five letter words you can make with a bunch of letters. 
First, it reads a file of words (its "dictionary") and saves them all in a list. Then, it checks each 
word in the dictionary to see if it can be built using only the letters you have, making sure you have 
enough of each letter to match the word. If a word works, it adds it to a list of "good matches." 
Finally, it counts how many words are in the list of matches and gives you that number. 
It is a step-by-step process: collect words, check if they fit your letters, and return the total 
number of the ones that work.
'''
# Load the list of words from the specified file and returns them as a list.
def import_wordle_words(file_path):
   
    # Start with an empty list to hold the words from the file
    imported_words = []
    
    # Open the file at the given path so we can read it 
    with open(file_path, 'r', encoding='utf-8') as file:

        # Go through each line in the file one at a time and then split the line into individual words and add each word to our list
        for line in file:
            for word in line.split():
                imported_words.append(word)
    
    # Send back the full list of words we found
    return imported_words


# Find all words in the Wordle list that can be formed using characters from the input string
def find_matching_words(wordle_words, input_string): 
    
    # Use a list to collect all the words that match the input string
    matching_words = [
        word  # This is the word we're checking
        for word in wordle_words  # Look at each word in the list of Wordle words

        # Check if the input string has enough of each letter to spell the word
        if all(input_string.count(char) >= word.count(char) for char in word)
    ]
    
    # Send back the list of words that can be made from the input string
    return matching_words


 # Count the number of Wordle words that can be formed from the input string
def exercise2(s, wordle_file='wordle.txt'):
   
    # Read all the Wordle words from the file so we have them in a list and then find the words we can make from the input string and count how many there are
    wordle_words = import_wordle_words(wordle_file)
    
    return len(find_matching_words(wordle_words, s))





# Exercise 3 - Wordle Set

'''
This function helps find how many words from a Wordle list match specific rules you give it. The rules are:

Green: Some letters must be in specific positions (like "A" in spot 1).
Yellow: Some letters must be in the word but not in certain spots.
Gray: Some letters aren't allowed in the word at all.
The function reads the Wordle words from a file and checks each word against these rules. 
If a word follows all the rules, it gets counted. 
The helper function 'matches' does the checking for each word. It ensures that:
-Green letters are in the correct positions (e.g., "A" must be in spot 1).
-Yellow letters are included in the word, but they are not in any of the positions where they are not allowed.
-Gray letters are completely excluded from the word.
After checking all the words, the function counts how many meet these conditions and returns the total.
'''

def exercise3(green, yellow, gray):
    
    # Open the Wordle file and read all the words into a list
    with open('wordle.txt', 'r') as file:
        words = file.read().splitlines()

    def matches(word):
        # Check that green letters are in the correct positions
        for pos, char in green.items():
            if word[pos] != char:
                return False

        # Check that yellow letters are in the word but not in their invalid positions
        for char, invalid_positions in yellow.items():
            if char not in word or any(word[pos] == char for pos in invalid_positions):
                return False

        # Make sure gray letters are not in the word at all
        if any(char in word for char in gray):
            return False

        # If it passes all checks, it's a match
        return True

    # Go through the list of words and count how many match the rules
    return sum(1 for word in words if matches(word))


# Exercise 4 - 2D Most Rewarding Shortest Path

'''
This function finds the shortest path on a grid, starting from 'A' and ending at 'B', 
while collecting as many rewards ('R') as possible along the way. The grid has obstacles ('X') you cannot cross, 
open spaces ('O') you can move through, and rewards ('R') you can collect. 
It uses a helper function to explore all possible paths by trying every valid move = right, down, left, and up. 
As it explores, it keeps track of the total steps and rewards collected. 
It picks the shortest path, and if paths have the same length, it chooses the one with the highest rewards. 
If there is no path between 'A' and 'B', it returns None.

ChatGPT4o (2024) was asked to help map out the explore_path function, that left me a little confused and helped
with the float('inf') solution - accessed on 05/12/2024

'''

# Find the shortest path from 'A' to 'B' with the highest reward
def exercise4(env):
    
    # Get the number of rows and columns in the grid
    rows = len(env)
    columns = len(env[0])

    # Locate the positions of 'A' (start) and 'B' (end)
    start = None
    end = None
    for r in range(rows):
        for c in range(columns):
            if env[r][c] == 'A':  # Found the start
                start = (r, c)
            elif env[r][c] == 'B':  # Found the destination
                end = (r, c)

    # Recursive helper function to explore paths on the grid
    def explore_path(row, column, visited, path_length, reward_collected):
       
        # If we reach 'B', return the path length and rewards
        if (row, column) == end:
            return path_length, reward_collected

        # Mark the current cell as visited to avoid revisiting
        visited.add((row, column))
        min_length = float('inf')  # Start with a very large path length
        max_reward = -1  # Start with no rewards

        # Check all four directions: right, down, left, up
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, column + dc  # Calculate the new row and column

            # Make sure the new cell is valid: within bounds and not visited
            if 0 <= nr < rows and 0 <= nc < columns and (nr, nc) not in visited:
                # Only move to open spaces, rewards, or the destination
                if env[nr][nc] in ('O', 'R', 'B'):

                    # Collect a reward if the cell is 'R'
                    new_reward = reward_collected + (1 if env[nr][nc] == 'R' else 0)

                    # Recursively explore the next cell
                    length, reward = explore_path(nr, nc, visited, path_length + 1, new_reward)

                    # Update the best path if it's shorter or has more rewards
                    if length < min_length or (length == min_length and reward > max_reward):
                        min_length, max_reward = length, reward

        # Unmark the current cell before backtracking
        visited.remove((row, column))
        return min_length, max_reward

    # If 'A' and 'B' are found, start the exploration
    if start and end:
        return explore_path(start[0], start[1], set(), 0, 0)
    else:
        return None  # Return None if 'A' or 'B' is missing



# Exercise 5 - Social Network Analysis

'''
This challenge helps find tightly connected groups of friends (called cliques) in a social network. 
A clique is a group where everyone is directly connected to each other, and a maximal clique is the biggest 
group you can form without adding more actors who aren't already connected to everyone in the group. 
The function first looks for all maximal cliques in the network using a clever recursive process. 
Then, it checks how many of these cliques each actor (or node) belongs to. Lastly, it gives you a list where each 
actor’s number shows how many cliques they are part of. (See below code for more information and references)
'''


# Check if a group of nodes forms a clique (everyone is connected). Finds all maximal cliques in the network using the Bron-Kerbosch algorithm
def is_clique(net, nodes):
   
    for i in nodes:
        for j in nodes:
            if i != j and net[i][j] == 0:  # If two nodes aren't connected
                return False
    return True

# Find all maximal cliques in the network using a simplified Bron-Kerbosch algorithm
def find_cliques(net, curr_clique, to_add, to_skip, cliques):
    
    # If no more nodes to add or skip, this is a maximal clique
    if not to_add and not to_skip:
        cliques.append(curr_clique)
        return

    # Try adding each node in to_add to the clique
    for node in list(to_add):
        # Add the node to the current clique
        new_clique = curr_clique + [node]

        # Find neighbors of this node that can join the clique
        add_next = [n for n in to_add if net[node][n] == 1]
        skip_next = [n for n in to_skip if net[node][n] == 1]

        # Recursively find larger cliques
        find_cliques(net, new_clique, add_next, skip_next, cliques)

        # Move node from to_add to to_skip
        to_add.remove(node)
        to_skip.append(node)

 # Count how many cliques each actor (node) belongs to in the network
def exercise5(net):
    
    n = len(net)  # Number of actors (nodes)
    cliques = []  # List to store all maximal cliques

    # Find all maximal cliques and count how many cliques each node belongs to
    find_cliques(net, [], list(range(n)), [], cliques)
    counts = [0] * n
    for node in range(n):
        for c in cliques:
            if node in c:
                counts[node] += 1

    return counts

'''

ChatGPT4o (2024) was asked to assist with fleshing out the idea for exercise 5, and to explain and provide sources for further reading in regards to the Bron-Kerbosch algorithm on 08/12/2024

This implementation of exercise5 uses the Bron-Kerbosch algorithm (Bron, C., & Kerbosch, J. (1973). Algorithm 457: Finding all cliques of an undirected graph. 
Communications of the ACM, 16(9), 575–577, https://dl.acm.org/doi/10.1145/362342.362367) 
to find all maximal cliques in a social network represented by an adjacency matrix.

The Bron-Kerbosch algorithm: 

Finds groups (cliques) where everyone is connected. Normally, it uses three sets to manage nodes: 
one for the current group, one for possible future members, and one for excluded nodes. 

For this problem, I simplified it by:
-Using clear, shorter names:
-curr_clique (current group being built)
-to_add (possible members that can still join)
-to_skip (excluded nodes that can't join)
-Using the network table (adjacency matrix) to check if two actors are connected.
-Filtering neighbors directly with Python lists for simplicity.
-When no more nodes can join (to_add and to_skip are empty), the group is saved as a maximal clique.
-In the end, count how many groups each actor belongs to
These changes make the algorithm simpler and easier to understand while solving the specific task
'''


