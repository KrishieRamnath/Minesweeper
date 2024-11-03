import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    # ... existing code ...

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """ Returns the set of all cells in self.cells known to be mines. """
        if self.count == len(self.cells):
            return self.cells
        return set()

    def known_safes(self):
        """ Returns the set of all cells in self.cells known to be safe. """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """ Updates internal knowledge representation given the fact that a cell is known to be a mine. """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """ Updates internal knowledge representation given the fact that a cell is known to be safe. """
        if cell in self.cells:
            self.cells.remove(cell)



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        # 1. Mark the cell as a move made and as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # 2. Create a list of neighboring cells that are not known to be safe or mines
        neighbors = set()
        i, j = cell
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if (di, dj) != (0, 0):
                    neighbor = (i + di, j + dj)
                    if 0 <= neighbor[0] < self.height and 0 <= neighbor[1] < self.width:
                        if neighbor not in self.safes and neighbor not in self.mines:
                            neighbors.add(neighbor)

        # 3. Add the new sentence to the AI's knowledge base
        new_sentence = Sentence(neighbors, count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # 4. Mark additional cells as safe or mines if possible
        self.update_knowledge()

        # 5. Combine sentences to draw new inferences
        self.infer_new_sentences()

    def update_knowledge(self):
        """
        Mark cells as safe or as mines based on the current knowledge.
        """
        for sentence in self.knowledge.copy():
            if sentence.known_mines():
                for cell in sentence.known_mines():
                    self.mark_mine(cell)
            if sentence.known_safes():
                for cell in sentence.known_safes():
                    self.mark_safe(cell)

        # Remove empty sentences (fully inferred)
        self.knowledge = [s for s in self.knowledge if s.cells]

    def infer_new_sentences(self):
        """
        Look for sentences in knowledge that are subsets of others and create new inferences.
        """
        for sentence1 in self.knowledge.copy():
            for sentence2 in self.knowledge.copy():
                if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                    inferred_cells = sentence2.cells - sentence1.cells
                    inferred_count = sentence2.count - sentence1.count
                    inferred_sentence = Sentence(inferred_cells, inferred_count)

                    if inferred_sentence not in self.knowledge:
                        self.knowledge.append(inferred_sentence)



    def make_safe_move(self):
    
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None



    def make_random_move(self):
        all_cells = {(i, j) for i in range(self.height) for j in range(self.width)}
        possible_moves = all_cells - self.moves_made - self.mines
        if possible_moves:
            return random.choice(list(possible_moves))
        return None


