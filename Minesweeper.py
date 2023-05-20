import pygame
import random

# Initialize Pygame
pygame.init()

# Set game level based on user input
level = int(input('Enter: 1 (easy), 2 (medium), 3 (hard)'))

# Define game sizes based on level
game_sizes = {1: (10, 10), 2: (15, 15), 3: (20, 20)}
game_width, game_height = game_sizes.get(level, (10, 10))

# Calculate the number of mines based on game size
mine_number = int(game_height * game_width * 0.1)

# Define the size of each board block
size = (40, 40)

# Define borders and screen dimensions
border = 16
top_border = 100
screen_width = size[0] * game_width + border * 2
screen_height = size[1] * game_height + border + top_border

# Create the game screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Create a clock to control the frame rate
timer = pygame.time.Clock()

# Set the caption of the game window
pygame.display.set_caption("Minesweeper")


# Load and scale the images used in the game
images = {
    "empty": pygame.image.load("img/0.png"),
    "flag": pygame.image.load("img/flag.png"),
    "block": pygame.image.load("img/block.png"),
    "block1": pygame.image.load("img/1.png"),
    "block2": pygame.image.load("img/2.png"),
    "block3": pygame.image.load("img/3.png"),
    "block4": pygame.image.load("img/4.png"),
    "block5": pygame.image.load("img/6.png"),
    "block6": pygame.image.load("img/5.png"),
    "block7": pygame.image.load("img/7.png"),
    "block8": pygame.image.load("img/8.png"),
    "mine": pygame.image.load("img/unclicked-bomb.png"),
    "mineclicked": pygame.image.load("img/clicked_bomb.png"),
    "non_mine": pygame.image.load("img/wrong-flag.png")
}

# Scale the images to match the grid block size
for image_name in images:
    image = images[image_name]
    image = image.convert()
    image = pygame.transform.scale(image, (int(screen_width / game_height), int(screen_width / game_width)))
    images[image_name] = image


blocks = []
mines = []

class Block:
    def __init__(self, x_block, y_block, type):
        # Positions of the block
        self.x_block, self.y_block = x_block, y_block
        # Bool to check if the block is clicked
        self.click = False
        # Bool to check if the block is a mine
        self.mine = False
        # Bool to check if the block is a non-mine that was flagged
        self.notmine = False
        # Bool to check if the block is flagged
        self.flag = False
        # Create rectObject to handle drawing and collisions
        self.rect = pygame.Rect(border + self.x_block * size[0], top_border + self.y_block * size[1], size[0], size[1])
        self.status = type

    def draw(self):
        # Draw the block based on its status and click state
        if self.notmine:
            screen.blit(images["non_mine"], self.rect)
        else:
            if self.click:
                if self.status == -1:
                    # Draw mine or mine clicked image
                    if self.mine:
                        screen.blit(images["mineclicked"], self.rect)
                    else:
                        screen.blit(images["mine"], self.rect)
                else:
                    # Draw empty block or numbered block
                    screen.blit(images.get("empty" if self.status == 0 else "block" + str(self.status)), self.rect)
            else:
                # Draw flag or block image
                if self.flag:
                    screen.blit(images["flag"], self.rect)
                else:
                    screen.blit(images["block"], self.rect)

    def openBlock(self):
        # Mark the block as clicked
        self.click = True

        if self.status == 0:
            # Open neighboring blocks recursively if the current block is empty
            for x in range(-1, 2):
                if self.x_block + x >= 0 and self.x_block + x < game_width:
                    for y in range(-1, 2):
                        if self.y_block + y >= 0 and self.y_block + y < game_height:
                            if not blocks[self.y_block + y][self.x_block + x].click:
                                blocks[self.y_block + y][self.x_block + x].openBlock()
        elif self.status == -1:
            # Open all mines if the current block is a mine
            for m in mines:
                if not blocks[m[1]][m[0]].click:
                    blocks[m[1]][m[0]].openBlock()

    def recreate(self):
        # Recalculate the status of the block based on neighboring mines
        if self.status != -1:
            for x in range(-1, 2):
                if self.x_block + x >= 0 and self.x_block + x < game_width:
                    for y in range(-1, 2):
                        if self.y_block + y >= 0 and self.y_block + y < game_height:
                            if blocks[self.y_block + y][self.x_block + x].status == -1:
                                self.status += 1

# Render text on the screen
def render_text(text, font_size, num=0):
    screen_text = pygame.font.SysFont("Montserrat", font_size, True).render(text, True, (0, 0, 0))
    place = screen_text.get_rect()
    place.center = (game_width * size[0] / 2 + border, game_height * size[1] / 2 + top_border + num)
    screen.blit(screen_text, place)

def game():
    global blocks
    global mines
    gameState = "Running"
    mineLeft = mine_number  # Number of remaining mines

    t = 0  # Time counter

    # Generate mine positions
    mines = [[random.randrange(0, game_width),
              random.randrange(0, game_height)]]

    for c in range(mine_number - 1):
        pos = [random.randrange(0, game_width),
               random.randrange(0, game_height)]
        same = True
        while same:
            for i in range(len(mines)):
                if pos == mines[i]:
                    pos = [random.randrange(0, game_width), random.randrange(0, game_height)]
                    break
                if i == len(mines) - 1:
                    same = False
        mines.append(pos)

    # Create a board
    for j in range(game_height):
        line = []
        for i in range(game_width):
            if [i, j] in mines:
                line.append(Block(i, j, -1))  # Create a mine block
            else:
                line.append(Block(i, j, 0))  # Create an empty block
        blocks.append(line)

    # Update the board
    for block in blocks:
        for i in block:
            i.recreate()

    while gameState != "Exit":
        screen.fill((230, 230, 230))  # Clear the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "Exit"  # Exit the game when the window is closed

            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    gameState = "Exit"  # Restart the game when 'R' is pressed
                    game()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for row in blocks:
                        for block in row:
                            if block.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    block.openBlock()  # Open the block on left click
                                    if block.flag:
                                        mineLeft += 1  # Toggle flag off
                                        block.flag = False
                                    if block.status == -1:  # Game over if a mine is clicked
                                        gameState = "Game Over"
                                        block.mineClicked = True
                                elif event.button == 3:
                                    if not block.click:
                                        if block.flag:
                                            block.flag = False  # Toggle flag off
                                            mineLeft += 1
                                        else:
                                            block.flag = True  # Toggle flag on
                                            if mineLeft > 0:
                                                mineLeft -= 1

        # Winning condition check
        win = True
        for row in blocks:
            for block in row:
                block.draw()
                if block.status != -1 and not block.click:
                    win = False
        if win and gameState != "Exit":
            gameState = "Win"

        # Draw the game state
        if gameState != "Game Over" and gameState != "Win":
            t += 1
        elif gameState == "Game Over":
            render_text("Game Over!", 50)
            render_text("Press R to restart", 40, 50)
            for row in blocks:
                for block in row:
                    if block.flag and block.status != -1:
                        block.mineFalse = True
        else:
            render_text("Win Win", 50)
            render_text("Press R to restart", 35, 50)
        # Draw time
        screen.blit(pygame.font.SysFont("Montserrat", 75).render(str(t // 15), True, (0, 0, 0)), (border, border))
        # Draw mine left
        screen.blit(pygame.font.SysFont("Montserrat", 75).render(str(mineLeft), True, (0, 0, 0)), (screen_width - border - 50, border))
        pygame.display.update()  # Update the screen
        timer.tick(20)  # Limit the frame rate



game()
pygame.quit()
quit()
