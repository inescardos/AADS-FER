import pygame
import sys
from bisect import bisect_left, bisect_right
from structures.suffix_array import SuffixArray, find_longest_common_substring

BACKGROUND_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 149, 237)
BUTTON_HOVER_COLOR = (65, 105, 225)
TEXT_COLOR = (0, 0, 0)
RESULT_COLOR = (255, 0, 0)
HIGHLIGHT_COLOR = (173, 216, 230)
INSTRUCTION_COLOR = (169, 169, 169)
BALL_COLOR = (50, 205, 50)

pygame.font.init()
TITLE_FONT = pygame.font.Font(None, 72)
BUTTON_FONT = pygame.font.Font(None, 48)
INPUT_FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 28)


def render_text(surface, text, x, y, font, color=TEXT_COLOR):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def is_mouse_over(rect):
    return rect.collidepoint(pygame.mouse.get_pos())

def main_menu(screen):
    WIDTH, HEIGHT = screen.get_size()
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)

        # Title
        title_text = TITLE_FONT.render("Suffix Array", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Buttons
        buttons = ["Visualize and Search Operations", "Find Longest Common Substring"]
        button_rects = []

        for i, text in enumerate(buttons):
            button_width, button_height = 600, 60
            button_x = (WIDTH - button_width) // 2
            button_y = HEIGHT // 2 + i * (button_height + 20)
            rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button_rects.append(rect)

            color = BUTTON_HOVER_COLOR if is_mouse_over(rect) else BUTTON_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=10)

            text_surface = BUTTON_FONT.render(text, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if is_mouse_over(button_rects[0]):
                        visualize_and_search(screen)
                    elif is_mouse_over(button_rects[1]):
                        visualize_find_longest_common_substring(screen)



def visualize_and_search(screen):
    WIDTH, HEIGHT = screen.get_size()

    input_text = ""            
    search_pattern = ""      
    search_mode = False        
    results = []
    current_search_label = "" 
    suffix_array_obj = None

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Process input
                    if input_text:
                        suffix_array_obj = SuffixArray(input_text)
                        current_search_label = "Suffix array built."
                        results = []  # Clear previous results
                elif event.key == pygame.K_BACKSPACE:
                    if search_mode:
                        search_pattern = search_pattern[:-1]
                    else:
                        input_text = input_text[:-1]
                elif event.key == pygame.K_TAB:  # Switch between input and search
                    search_mode = not search_mode
                    current_search_label = "Search mode activated." if search_mode else "Input mode activated."
                elif event.key == pygame.K_s:  # Prefix search
                    if suffix_array_obj and search_pattern:
                        results = suffix_array_obj.suffices_start_with(search_pattern)
                        current_search_label = f"Search for suffixes starting with '{search_pattern}'"
                elif event.key == pygame.K_p:  # Pattern search
                    if suffix_array_obj and search_pattern:
                        results = suffix_array_obj.suffices_pattern_search(search_pattern)
                        current_search_label = f"Pattern search for '{search_pattern}'"
                elif event.key == pygame.K_o:  # Count occurrences of the pattern
                    if suffix_array_obj and search_pattern:
                        count = suffix_array_obj.count_substring_occurrences(search_pattern)
                        results = []  # Clear results since this is a count-only action
                        current_search_label = f"Number of occurrences of '{search_pattern}': {count}"
                else:
                    if search_mode:
                        search_pattern += event.unicode
                    else:
                        input_text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    back_button_rect = pygame.Rect(10, 10, 120, 40)
                    if back_button_rect.collidepoint(event.pos):
                        return 

        # Draw Input Box
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, pygame.Rect(50, 50, WIDTH - 100, 50), 2)
        render_text(screen, f"Input Text: {input_text}", 60, 60, INPUT_FONT)

        # Draw Search Box
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, pygame.Rect(50, 120, WIDTH - 100, 50), 2)
        render_text(screen, f"Search Pattern: {search_pattern}", 60, 130, INPUT_FONT)

        # Draw Suffix Array
        if suffix_array_obj:
            render_text(screen, "i  | Suffix Array |    Suffix", 50, 200, INPUT_FONT)
            pygame.draw.line(screen, TEXT_COLOR, (50, 230), (WIDTH - 50, 230), 2)

            for i, suffix in enumerate(suffix_array_obj.get_suffixes()):
                render_text(screen, f"{i}", 60, 240 + i * 30, SMALL_FONT)
                render_text(screen, f"{suffix_array_obj.suffix_array[i]}", 120, 240 + i * 30, SMALL_FONT)
                render_text(screen, f"{suffix}", 200, 240 + i * 30, SMALL_FONT)

        # Draw Search Results
        render_text(screen, "Search Results:", 600, 200, INPUT_FONT)
        if results:
            for i, suffix in enumerate(results):
                render_text(screen, suffix, 600, 240 + i * 30, SMALL_FONT, RESULT_COLOR)
        else:
            render_text(screen, current_search_label, 600, 240, SMALL_FONT, RESULT_COLOR)

        # Draw Back Button
        back_button_rect = pygame.Rect(10, 10, 120, 40)
        pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)
        render_text(screen, "Back", back_button_rect.x + 30, back_button_rect.y + 10, INPUT_FONT)

        # Dynamic Ball Indicator
        ball_y = 75 if not search_mode else 145
        pygame.draw.circle(screen, BALL_COLOR, (40, ball_y), 10)

        instructions = [
            "Instructions:",
            "1. Enter the text and press ENTER to build the suffix array.",
            "2. Press TAB to switch to search mode.",
            "3. In search mode, type your search pattern.",
            "4. Press 'P' for pattern search.",
            "5. Press 'O' to count occurrences of the pattern.",
            "6. Use BACKSPACE to edit text in the focused box.",
        ]

        y_position = HEIGHT - len(instructions) * 25 - 10
        for instruction in instructions:
            render_text(screen, instruction, 50, y_position, SMALL_FONT, INSTRUCTION_COLOR)
            y_position += 25

        pygame.display.flip()


def visualize_find_longest_common_substring(screen):
    WIDTH, HEIGHT = screen.get_size()

    input1 = ""
    input2 = ""
    result = ""
    focused_box = 1
    BALL_COLOR = (50, 205, 50)
    INSTRUCTION_COLOR = (169, 169, 169)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    if input1 and input2:
                        result = find_longest_common_substring(input1, input2)
                elif event.key == pygame.K_BACKSPACE: 
                    if focused_box == 1:
                        input1 = input1[:-1]
                    elif focused_box == 2:
                        input2 = input2[:-1]
                elif event.key == pygame.K_TAB:  # Toggle focus between input boxes
                    focused_box = 2 if focused_box == 1 else 1
                else:
                    if focused_box == 1:
                        input1 += event.unicode
                    elif focused_box == 2:
                        input2 += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    back_button_rect = pygame.Rect(10, 10, 120, 40)
                    if back_button_rect.collidepoint(event.pos):
                        return 

        # Input Boxes
        box1_y = 50
        box2_y = 120
        ball_x = 30
        ball_y = box1_y + 25 if focused_box == 1 else box2_y + 25

        pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), 10)

        # Draw the input boxes
        pygame.draw.rect(screen, TEXT_COLOR, pygame.Rect(50, box1_y, WIDTH - 100, 50), 2)
        render_text(screen, f"String 1: {input1}", 60, box1_y + 10, INPUT_FONT)

        pygame.draw.rect(screen, TEXT_COLOR, pygame.Rect(50, box2_y, WIDTH - 100, 50), 2)
        render_text(screen, f"String 2: {input2}", 60, box2_y + 10, INPUT_FONT)

        # Result Box
        render_text(screen, "Longest Common Substring:", 50, 200, INPUT_FONT)
        render_text(screen, result, 50, 240, SMALL_FONT, RESULT_COLOR)

        # Draw Back Button
        back_button_rect = pygame.Rect(10, 10, 120, 40)  # Positioned on the left with space below
        pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)
        render_text(screen, "Back", back_button_rect.x + 30, back_button_rect.y + 10, INPUT_FONT)

        instructions = [
            "Instructions:",
            "1. Enter the first string in the top input box.",
            "2. Press TAB to switch to the second input box.",
            "3. Enter the second string in the bottom input box.",
            "4. Press ENTER to calculate the Longest Common Substring.",
            "5. The result will appear below the input boxes.",
            "6. Use BACKSPACE to edit the text in the focused input box.",
        ]

        y_position = HEIGHT - len(instructions) * 25 - 10
        for instruction in instructions:
            render_text(screen, instruction, 50, y_position, SMALL_FONT, INSTRUCTION_COLOR)
            y_position += 25

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))
    main_menu(screen)
