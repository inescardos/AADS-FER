import pygame
import sys
import time
from structures.prefix_trie import PrefixTrie

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
NODE_RADIUS = 20
FONT_SIZE = 18
NODE_SPACING_X = 50
NODE_SPACING_Y = 80


WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
DARKER_BLUE = (70, 130, 180)  
BABY_YELLOW = (255, 255, 153)  
LIGHT_GREEN = (144, 238, 144)  
BLACK = (0,0,0)
RED = (255,119, 121)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Trie Visualization")
font = pygame.font.Font(None, FONT_SIZE)

class VisualTrieNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.children = {}
        self.is_end = False

class VisualTrie:
    def __init__(self):
        self.root = VisualTrieNode(WINDOW_WIDTH // 2, 50)
        self.total_width = WINDOW_WIDTH
        self.highlighted_nodes = []  # Nodes to highlight for search

    def insert(self, word):
        word = word[::-1]
        for i in range(len(word)):
            suffix = word[i:]
            current = self.root
            for char in suffix:
                if char not in current.children:
                    current.children[char] = VisualTrieNode(0, 0)
                current = current.children[char]
            current.is_end = True

    def reset(self):
        self.__init__()

    def count_substring_occurrences(self, pattern):
        pattern = pattern[::-1] 
        total_count = 0
        node = self.root

        for depth, char in enumerate(pattern):
            if char in node.children:
                node = node.children[char]
            else:
                return 0

        def count_end_nodes(current_node):
            nonlocal total_count
            if current_node.is_end:
                total_count += 1
            for child in current_node.children.values():
                count_end_nodes(child)

        count_end_nodes(node)
        return total_count

    def find_pattern(self, pattern):
        self.highlighted_nodes = []  # Clear previous highlights
        pattern = pattern[::-1]

        def _search_from_node(node, pattern, depth=0):
            if depth == len(pattern):
                return True

            char = pattern[depth]
            if char not in node.children:
                return False

            self.highlighted_nodes.append(node.children[char])  # Highlight the current matching node
            return _search_from_node(node.children[char], pattern, depth + 1)

        def _traverse_and_match(node, pattern):
            if _search_from_node(node, pattern):
                return True

            for child in node.children.values():
                if _traverse_and_match(child, pattern):
                    return True

            return False

        if _traverse_and_match(self.root, pattern):
            return True
        else:
            return False

    def find_longest_common_substring(self, word):
        self.highlighted_nodes = []
        word = word[::-1] 
        longest_common_substring = ""
        current_substring = []

        def search(node, index):
            nonlocal longest_common_substring
            if index == len(word):
                return

            char = word[index]
            if char in node.children:
                current_substring.append(char)
                self.highlighted_nodes.append(node.children[char])
                search(node.children[char], index + 1)

                if len(current_substring) > len(longest_common_substring):
                    longest_common_substring = "".join(current_substring)

                current_substring.pop()

        for i in range(len(word)):
            search(self.root, i)

        return longest_common_substring[::-1]

    def assign_positions(self):
        def compute_positions(node, left_bound, right_bound, depth):
            mid_x = (left_bound + right_bound) // 2
            node.x = mid_x
            node.y = depth * NODE_SPACING_Y

            # Divide the horizontal space equally among children
            num_children = len(node.children)
            if num_children > 0:
                child_width = (right_bound - left_bound) // num_children
                for i, (char, child) in enumerate(node.children.items()):
                    child_left = left_bound + i * child_width
                    child_right = child_left + child_width
                    compute_positions(child, child_left, child_right, depth + 1)

        compute_positions(self.root, 0, self.total_width, 1)

    def draw(self, screen):
        """Draw the tree on the screen."""
        def draw_node(node, parent=None, parent_char=None):
            # Highlight node if it is part of the search path
            color = BABY_YELLOW if node in self.highlighted_nodes else (DARKER_BLUE if node.is_end else LIGHT_BLUE)
            pygame.draw.circle(screen, color, (node.x, node.y), NODE_RADIUS)
            if parent:
                pygame.draw.line(screen, LIGHT_BLUE, (parent.x, parent.y), (node.x, node.y), 2)
                text = font.render(parent_char, True, BLACK)
                text_rect = text.get_rect(center=((parent.x + node.x) // 2, (parent.y + node.y) // 2))
                screen.blit(text, text_rect)

            # Draw children recursively
            for char, child in node.children.items():
                draw_node(child, node, char)

        self.assign_positions()  # Ensure positions are updated
        draw_node(self.root)

def main():
    running = True
    clock = pygame.time.Clock()
    visual_trie = VisualTrie()

    user_input = ""
    mode = "insert"  # Modes: "insert", "search", "longest_common_substring", "reset", "count_occurrences"
    search_result = None
    lcs_result = ""
    occurrences_result = 0

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if mode == "insert":
                        visual_trie.insert(user_input)
                    elif mode == "search":
                        search_result = visual_trie.find_pattern(user_input)
                    elif mode == "longest_common_substring":
                        lcs_result = visual_trie.find_longest_common_substring(user_input)
                    elif mode == "count_occurrences":
                        occurrences_result = visual_trie.count_substring_occurrences(user_input)
                    user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 10 <= x <= 110 and 10 <= y <= 40:
                    mode = "insert"
                elif 120 <= x <= 220 and 10 <= y <= 40:
                    mode = "search"
                elif 230 <= x <= 430 and 10 <= y <= 40:
                    mode = "longest_common_substring"
                elif 440 <= x <= 540 and 10 <= y <= 40:
                    mode = "count_occurrences"
                elif 550 <= x <= 650 and 10 <= y <= 40:
                    visual_trie.reset()
                    user_input = ""
                    search_result = None
                    lcs_result = ""
                    occurrences_result = 0

        # Draw buttons
        pygame.draw.rect(screen, LIGHT_GREEN if mode == "insert" else LIGHT_BLUE, (10, 10, 100, 30))
        screen.blit(font.render("Insert", True, BLACK), (20, 15))

        pygame.draw.rect(screen, LIGHT_GREEN if mode == "search" else LIGHT_BLUE, (120, 10, 100, 30))
        screen.blit(font.render("Search", True, BLACK), (130, 15))

        pygame.draw.rect(screen, LIGHT_GREEN if mode == "longest_common_substring" else LIGHT_BLUE, (230, 10, 200, 30))
        screen.blit(font.render("Longest Common Substring", True, BLACK), (240, 15))

        pygame.draw.rect(screen, LIGHT_GREEN if mode == "count_occurrences" else LIGHT_BLUE, (440, 10, 100, 30))
        screen.blit(font.render("Count", True, BLACK), (450, 15))

        pygame.draw.rect(screen, LIGHT_GREEN if mode == "reset" else LIGHT_BLUE, (550, 10, 100, 30))
        screen.blit(font.render("Reset", True, BLACK), (560, 15))

        # Draw user input
        input_text = font.render(user_input, True, BLACK)
        screen.blit(input_text, (10, 50))

        # Draw search result
        if mode == "search" and search_result is not None:
            result_text = font.render(f"Found: {search_result}", True, DARKER_BLUE if search_result else RED)
            screen.blit(result_text, (10, 80))

        # Draw longest common substring result
        if mode == "longest_common_substring" and lcs_result:
            lcs_text = font.render(f"LCS: {lcs_result}", True, DARKER_BLUE)
            screen.blit(lcs_text, (10, 110))

        # Draw occurrences result
        if mode == "count_occurrences" and occurrences_result is not None:
            occurrences_text = font.render(f"Occurrences: {occurrences_result}", True, DARKER_BLUE)
            screen.blit(occurrences_text, (10, 140))

        # Draw the Trie
        visual_trie.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
