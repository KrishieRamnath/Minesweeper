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
        # Step 1: Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Step 2: Mark the cell as safe
        self.mark_safe(cell)

        # Step 3: Create a new sentence from the current cell and count of neighboring mines
        neighboring_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) != cell and 0 <= i < self.height and 0 <= j < self.width:
                    neighboring_cells.add((i, j))

        new_sentence = Sentence(neighboring_cells, count)
        self.knowledge.append(new_sentence)

        # Step 4: Mark additional cells as safe or as mines
        for sentence in self.knowledge:
            if len(sentence.cells) == sentence.count:
                for cell in sentence.cells:
                    self.mark_mine(cell)
            elif len(sentence.cells) == 0:
                continue

        # Step 5: Infer new knowledge from existing sentences
        for sentence in self.knowledge:
            for other_sentence in self.knowledge:
                if sentence != other_sentence and sentence.cells.issubset(other_sentence.cells):
                    new_cells = other_sentence.cells - sentence.cells
                    new_count = other_sentence.count - sentence.count
                    if new_count >= 0:
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence)



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


