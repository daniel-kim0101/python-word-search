import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import json
import random
import string


# creating scrollable frame class
 # ScrollableFrame generated with AI assistance (Gemini)
class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Bind the configure event of the inner frame to update the scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind("<Enter>", self.bind_mouse_wheel)
        self.canvas.bind("<Leave>", self.unbind_mouse_wheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def bind_mouse_wheel(self, event):
        """Bind the mouse wheel events when the cursor enters the canvas area."""
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        # Specific bindings for Linux scroll buttons
        self.canvas.bind_all('<Button-4>', self._on_mousewheel)
        self.canvas.bind_all('<Button-5>', self._on_mousewheel)

    def unbind_mouse_wheel(self, event):
        """Unbind the mouse wheel events when the cursor leaves the canvas area."""
        self.canvas.unbind_all('<MouseWheel>')
        self.canvas.unbind_all('<Button-4>')
        self.canvas.unbind_all('<Button-5>')


# mouse functions
def on_mouse_press(event):
    global clicked, curr_coord, final_coord
    temp = (event.x, event.y)
    if(ingame):
        if(not clicked):
            for i in range(len(board_pos)):
                for e in range(len(board_pos[i])):
                    if((temp[0] > board_pos[i][e][0] and temp[0] < board_pos[i][e][0] + 22) and (temp[1] > board_pos[i][e][1] and temp[1] < board_pos[i][e][1] + 22)):
                        curr_coord = (i, e)
                        fill(curr_coord)
                        clicked = True
        else:
            for i in range(len(board_pos)):
                for e in range(len(board_pos[i])):
                    if((temp[0] > board_pos[i][e][0] and temp[0] < board_pos[i][e][0] + 22) and (temp[1] > board_pos[i][e][1] and temp[1] < board_pos[i][e][1] + 22)):
                        gameboard.delete(tempsquare)
                        final_coord = (i, e)
                        clicked = False
                        guess = check(curr_coord, final_coord)
                        if(guess):
                            '''
                            NOTE:
                            0 = up and to the left
                            1 = up
                            2 = up and to the right
                            3 = left
                            4 = right
                            5 = down and to the left
                            6 = down
                            7 = down and to the right
                            '''
                            if(guess[1] < 0 and guess[2] < 0):
                                direction = 0
                            elif(guess[1] == 0 and guess[2] < 0):
                                direction = 1
                            elif(guess[1] > 0 and guess[2] < 0):
                                direction = 2
                            elif(guess[1] < 0 and guess[2] == 0):
                                direction = 3
                            elif(guess[1] > 0 and guess[2] == 0):
                                direction = 4
                            elif(guess[1] < 0 and guess[2] > 0):
                                direction = 5
                            elif(guess[1] == 0 and guess[2] > 0):
                                direction = 6
                            elif(guess[1] > 0 and guess[2] > 0):
                                direction = 7
                            crossout(curr_coord, final_coord, direction, tempwords.index(guess[0]))
                            found_words.append(guess[0])
                            check_completion()
                        curr_coord = ()
                        final_coord = ()


def on_mouse_drag(event):
    global ticks, curr_block, curr_line
    ticks += 1
    temp = (event.x, event.y)
    for i in range(len(board_pos)):
        for e in range(len(board_pos[i])):
            if((temp[0] > board_pos[i][e][0] and temp[0] < board_pos[i][e][0] + 22) and (temp[1] > board_pos[i][e][1] and temp[1] < board_pos[i][e][1] + 22) and curr_block != (i, e)):
                curr_block = (i, e)
                if(curr_coord == curr_block):
                    return
                if(inline(curr_coord, curr_block)):
                    guess = (0, curr_block[1] - curr_coord[1], curr_block[0] - curr_coord[0])
                    if(guess[1] < 0 and guess[2] < 0):
                        direction = 0
                    elif(guess[1] == 0 and guess[2] < 0):
                        direction = 1
                    elif(guess[1] > 0 and guess[2] < 0):
                        direction = 2
                    elif(guess[1] < 0 and guess[2] == 0):
                        direction = 3
                    elif(guess[1] > 0 and guess[2] == 0):
                        direction = 4
                    elif(guess[1] < 0 and guess[2] > 0):
                        direction = 5
                    elif(guess[1] == 0 and guess[2] > 0):
                        direction = 6
                    elif(guess[1] > 0 and guess[2] > 0):
                        direction = 7
                    tempcrossout(curr_coord, curr_block, direction)


def on_mouse_release(event):
    global clicked, curr_coord, final_coord, ticks, curr_line, tempwords
    temp = (event.x, event.y)
    if(ingame and ticks > 0):
        for i in range(len(board_pos)):
            for e in range(len(board_pos[i])):
                if((temp[0] > board_pos[i][e][0] and temp[0] < board_pos[i][e][0] + 22) and (temp[1] > board_pos[i][e][1] and temp[1] < board_pos[i][e][1] + 22)):
                    gameboard.delete(tempsquare)
                    gameboard.delete(curr_line)
                    final_coord = (i, e)
                    clicked = False
                    guess = check(curr_coord, final_coord)
                    if(guess):
                        '''
                        NOTE:
                        0 = up and to the left
                        1 = up
                        2 = up and to the right
                        3 = left
                        4 = right
                        5 = down and to the left
                        6 = down
                        7 = down and to the right
                        '''
                        if(guess[1] < 0 and guess[2] < 0):
                            direction = 0
                        elif(guess[1] == 0 and guess[2] < 0):
                            direction = 1
                        elif(guess[1] > 0 and guess[2] < 0):
                            direction = 2
                        elif(guess[1] < 0 and guess[2] == 0):
                            direction = 3
                        elif(guess[1] > 0 and guess[2] == 0):
                            direction = 4
                        elif(guess[1] < 0 and guess[2] > 0):
                            direction = 5
                        elif(guess[1] == 0 and guess[2] > 0):
                            direction = 6
                        elif(guess[1] > 0 and guess[2] > 0):
                            direction = 7
                        crossout(curr_coord, final_coord, direction, tempwords.index(guess[0]))
                        found_words.append(guess[0])
                        check_completion()
                    curr_coord = ()
                    final_coord = ()
                    ticks = 0


# variables
ingame = False
board = []
clicked = False
ticks = 0
curr_block = ()
curr_line = 0
gameboard = None
wordboard = None

# Create Tk and canvas
root = Tk()
root.title("Word Search")
root.resizable(width=False, height=False)
root.geometry('1536x841+0+0')
root.update()
width = root.winfo_width()
height = root.winfo_height()
print(str(width) + " " + str(height))
fall = Image.open("fall.png")
resized_image = fall.resize((1500, 100), Image.Resampling.LANCZOS)
fall_photo = ImageTk.PhotoImage(resized_image)
spring = Image.open("spring.png")
resized_image = spring.resize((1500, 100), Image.Resampling.LANCZOS)
spring_photo = ImageTk.PhotoImage(resized_image)
summer = Image.open("summer.png")
resized_image = summer.resize((1500, 100), Image.Resampling.LANCZOS)
summer_photo = ImageTk.PhotoImage(resized_image)
winter = Image.open("winter.png")
resized_image = winter.resize((1500, 100), Image.Resampling.LANCZOS)
winter_photo = ImageTk.PhotoImage(resized_image)
games = Image.open("games.png")
resized_image = games.resize((1500, 100), Image.Resampling.LANCZOS)
games_photo = ImageTk.PhotoImage(resized_image)
sports = Image.open("sports.png")
resized_image = sports.resize((1500, 100), Image.Resampling.LANCZOS)
sports_photo = ImageTk.PhotoImage(resized_image)
food = Image.open("food.png")
resized_image = food.resize((1500, 100), Image.Resampling.LANCZOS)
food_photo = ImageTk.PhotoImage(resized_image)
animals = Image.open("animals.png")
resized_image = animals.resize((1500, 100), Image.Resampling.LANCZOS)
animals_photo = ImageTk.PhotoImage(resized_image)
colors = Image.open("colors.png")
resized_image = colors.resize((1500, 100), Image.Resampling.LANCZOS)
colors_photo = ImageTk.PhotoImage(resized_image)


# handle button clicks
def b_click(b, num):
    if(b["text"] == "Fall"):
        create_game("Fall", fall_photo)
    elif(b["text"] == "Spring"):
        create_game("Spring", spring_photo)
    elif(b["text"] == "Summer"):
        create_game("Summer", summer_photo)
    elif(b["text"] == "Winter"):
        create_game("Winter", winter_photo)
    elif(b["text"] == "Games"):
        create_game("Games", games_photo)
    elif(b["text"] == "Sports"):
        create_game("Sports", sports_photo)
    elif(b["text"] == "Food"):
        create_game("Food", food_photo)
    elif(b["text"] == "Animals"):
        create_game("Animals", animals_photo)
    elif(b["text"] == "Colors"):
        create_game("Colors", colors_photo)


# generate random direction (listed below) for direction of word
def random_direction():
    randomdirection = random.randint(0, 7)
    deltax = 0
    deltay = 0
    '''
    0 = up and to the left
    1 = up
    2 = up and to the right
    3 = left
    4 = right
    5 = down and to the left
    6 = down
    7 = down and to the right
    '''
    if(randomdirection == 0):
        deltax -= 1
        deltay -= 1
    elif(randomdirection == 1):
        deltay -= 1
    elif(randomdirection == 2):
        deltax += 1
        deltay -= 1
    elif(randomdirection == 3):
        deltax -= 1
    elif(randomdirection == 4):
        deltax += 1
    elif(randomdirection == 5):
        deltax -= 1
        deltay += 1
    elif(randomdirection == 6):
        deltay += 1
    elif(randomdirection == 7):
        deltax += 1
        deltay += 1
    return deltax, deltay


# checks to see if there's a potential intersection in a word's path
def no_letters(length, startx, starty, deltax, deltay, board):
    for i in range(length):
        if(board[startx][starty] != '.'):
            return False
        startx += deltax
        starty += deltay
    return True


# creates random letters for board
def populate(board):
    global indices
    for i in range(len(board)):
        for e in range(len(board[i])):
            found = True
            for ind in indices:
                if((i, e) in ind):
                    found = False
            if(found):
                board[i][e] = random.choice(string.ascii_uppercase)
    return board


# checks to see if guess was correct
# note: tuple is in (y,x) due to logic of checking
def check(init, final):
    if(inline(init, final)):
        guess = ""
        dy = (final[0] - init[0])
        if(dy != 0):
            dy = int(dy / (abs(final[0] - init[0])))
        dx = (final[1] - init[1])
        if(dx != 0):
            dx = int(dx / (abs(final[1] - init[1])))
        while init != final:
            guess += board[init[0]][init[1]]
            init = (init[0] + dy, init[1] + dx)
        guess += board[init[0]][init[1]]
        if(guess in tempwords):
            return guess, dx, dy
        return ""


# ensure that guess is in a straight line
def inline(init, final):
    if(init[0] == final[0] or init[1] == final[1] or abs((final[1] - init[1]) / (final[0] - init[0])) == 1):
        return True
    return False


# cross out found word in wordlist and on board
# note that coords will be given in (y,x)
def crossout(init, final, direction, ind):
    start = board_pos[init[0]][init[1]]
    end = board_pos[final[0]][final[1]]
    '''
    0 = up and to the left
    1 = up
    2 = up and to the right
    3 = left
    4 = right
    5 = down and to the left
    6 = down
    7 = down and to the right
    '''
    if(direction == 0):
        gameboard.create_line(start[0] + 22, start[1] + 22, end[0], end[1], fill="red", width=3)
    elif(direction == 1):
        gameboard.create_line(start[0] + 11, start[1] + 22, end[0] + 11, end[1], fill="red", width=3)
    elif(direction == 2):
        gameboard.create_line(start[0], start[1] + 22, end[0] + 22, end[1], fill="red", width=3)
    elif(direction == 3):
        gameboard.create_line(start[0] + 22, start[1] + 11, end[0], end[1] + 11, fill="red", width=3)
    elif(direction == 4):
        gameboard.create_line(start[0], start[1] + 11, end[0] + 22, end[1] + 11, fill="red", width=3)
    elif(direction == 5):
        gameboard.create_line(start[0] + 22, start[1], end[0], end[1] + 22, fill="red", width=3)
    elif(direction == 6):
        gameboard.create_line(start[0] + 11, start[1], end[0] + 11, end[1] + 22, fill="red", width=3)
    elif(direction == 7):
        gameboard.create_line(start[0], start[1], end[0] + 22, end[1] + 22, fill="red", width=3)
    edges = wordboard_pos[ind]
    wordboard.create_line(edges, fill="red", width=3)
    edges = [edges[2], edges[1], edges[0], edges[3]]
    wordboard.create_line(edges, fill="red", width=3)


# cross out current guess when dragging, not for final guess
# note that coords will be given in (y,x)
def tempcrossout(init, final, direction):
    global curr_line
    if(curr_line in gameboard.find_all()):
        gameboard.delete(curr_line)
    start = board_pos[init[0]][init[1]]
    end = board_pos[final[0]][final[1]]
    '''
    0 = up and to the left
    1 = up
    2 = up and to the right
    3 = left
    4 = right
    5 = down and to the left
    6 = down
    7 = down and to the right
    '''
    if(direction == 0):
        curr_line = gameboard.create_line(start[0] + 22, start[1] + 22, end[0], end[1], fill="red", width=3)
    elif(direction == 1):
        curr_line = gameboard.create_line(start[0] + 11, start[1] + 22, end[0] + 11, end[1], fill="red", width=3)
    elif(direction == 2):
        curr_line = gameboard.create_line(start[0], start[1] + 22, end[0] + 22, end[1], fill="red", width=3)
    elif(direction == 3):
        curr_line = gameboard.create_line(start[0] + 22, start[1] + 11, end[0], end[1] + 11, fill="red", width=3)
    elif(direction == 4):
        curr_line = gameboard.create_line(start[0], start[1] + 11, end[0] + 22, end[1] + 11, fill="red", width=3)
    elif(direction == 5):
        curr_line = gameboard.create_line(start[0] + 22, start[1], end[0], end[1] + 22, fill="red", width=3)
    elif(direction == 6):
        curr_line = gameboard.create_line(start[0] + 11, start[1], end[0] + 11, end[1] + 22, fill="red", width=3)
    elif(direction == 7):
        curr_line = gameboard.create_line(start[0], start[1], end[0] + 22, end[1] + 22, fill="red", width=3)


# fills a square
def fill(coord):
    global tempsquare
    tofill = board_pos[coord[0]][coord[1]]
    tempsquare = gameboard.create_rectangle(tofill[0], tofill[1], tofill[0] + 22, tofill[1] + 22, outline="red")


# check to see if words aren't repeated
def all_unique(board):
    global tempwords
    start = []
    for words in tempwords:
        if(not words[0] in start):
            start.append(words[0])
    found_dict = {}
    for i in range(len(board)):
        for e in range(len(board[i])):
            if(board[i][e] in start):
                words = []
                words.append(search(board, i - 1, e - 1, tempwords, -1, -1, board[i][e], [(i, e)]))
                words.append(search(board, i, e - 1, tempwords, 0, -1, board[i][e], [(i, e)]))
                words.append(search(board, i + 1, e - 1, tempwords, 1, -1, board[i][e], [(i, e)]))
                words.append(search(board, i - 1, e, tempwords, -1, 0, board[i][e], [(i, e)]))
                words.append(search(board, i + 1, e, tempwords, 1, 0, board[i][e], [(i, e)]))
                words.append(search(board, i - 1, e + 1, tempwords, -1, 1, board[i][e], [(i, e)]))
                words.append(search(board, i, e + 1, tempwords, 0, 1, board[i][e], [(i, e)]))
                words.append(search(board, i + 1, e + 1, tempwords, 1, 1, board[i][e], [(i, e)]))
                for word in words:
                    if(word):
                        if(word[0] in found_dict.keys()):
                            found = False
                            for key in found_dict.keys():
                                if(set(word[1]).issubset(set(found_dict[key]))):
                                    found = True
                            if(not found):
                                print('restart')
                                print(found_dict)
                                return False
                        found_dict[word[0]] = word[1]
    return True


# goes through a point to check if word is on board
def search(board, x, y, words, dx, dy, word, coords):
    cnt = 0
    curr_word = ""
    for w in words:
        if(word in w):
            cnt += 1
            curr_word = w
    if(cnt == 1 and curr_word == word):
        return word, coords
    elif(cnt == 0):
        return ""
    elif(x + dx < len(board) and x + dx >= 0 and y + dy < len(board[0]) and y + dy >= 0):
        coords.append((x, y))
        return search(board, x + dx, y + dy, words, dx, dy, word + board[x][y], coords)
    else:
        return ""


# checks if player has gotten all the words in the word bank
def check_completion():
    if(set(found_words) == set(tempwords)):
        messagebox.showinfo('Word Search', 'Congrats! You win!\nPlease click the "back" button to find a new board to play')


# generates a random word to reveal on the board
def hint():
    # every word has already been revealed, so there is nothing left to hint
    if(len(revealed_words) == len(indices)):
        return
    found = False
    while not found:
        found = False
        random_ind = random.randint(0, len(indices) - 1)
        for ind in revealed_words:
            if(set(ind) == set(indices[random_ind])):
                found = True
        if(not found):
            revealed_words.append(indices[random_ind])
            for i in indices[random_ind]:
                xpos = i[0]
                ypos = i[1]
                gameboard.create_rectangle(board_pos[xpos][ypos][0], board_pos[xpos][ypos][1], board_pos[xpos][ypos][0] + 22, board_pos[xpos][ypos][1] + 22, outline="red")
            return


# creates game
def create_game(theme, img):
    global board, board_pos, ingame, tempwords, words, gameboard, wordboard_pos, indices, scroll_frame_container, wordboard, found_words, revealed_words, game_menu
    fall_button.pack_forget()
    spring_button.pack_forget()
    summer_button.pack_forget()
    winter_button.pack_forget()
    games_button.pack_forget()
    sports_button.pack_forget()
    food_button.pack_forget()
    animals_button.pack_forget()
    colors_button.pack_forget()
    canvas.delete("all")
    gameboard = Canvas(container, width=1200, height=600, bg="white")
    gameboard.pack(fill="both", expand=True)
    gameboard.bind("<ButtonPress-1>", on_mouse_press)
    gameboard.bind("<B1-Motion>", on_mouse_drag)
    gameboard.bind("<ButtonRelease-1>", on_mouse_release)
    wordboard = tk.Canvas(container, width=1200, height=250)
    wordboard.pack(fill="both", expand=True)
    img = ImageTk.getimage(img)
    img = img.resize((3200, 900), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    wordboard.create_image(0, 0, image=img)
    wordboard.image_reference = img
    words = []
    found_words = []
    revealed_words = []
    ingame = True
    game_menu = Menu(root)
    root.config(menu=game_menu)
    # options_menu = Menu(root, tearoff = False)
    # game_menu.add_cascade(label = "Options")
    game_menu.add_command(label="Back", command=reset)
    game_menu.add_command(label="Hint", command=hint)
    canvas.destroy()
    scroll_frame_container.pack_forget()
    scroll_frame_container.destroy()
    with open('words.json', 'r') as file:
        wordboard_pos = []
        x = 40
        y = 10
        words_data = json.load(file)
        for category in words_data["Categories"]:
            if category["Category"] == theme:
                words_data = category["Words"]
        i = 0
        while i < 3:
            print(words_data)
            word = random.choice(words_data["Short"])
            if(not word in words):
                words.append(word)
                i += 1
                text = wordboard.create_text(x, y, text=word, font=("Helvetica", 10, 'bold'), fill="black")
                bbox = wordboard.bbox(text)
                rect = wordboard.create_rectangle(bbox, fill="white", outline="white")
                wordboard.lower(rect, text)
                wordboard_pos.append(bbox)
                x += 60
        y += 50
        x = 55
        while i < 12:
            word = random.choice(words_data["Medium"])
            if(not word in words):
                words.append(word)
                i += 1
                text = wordboard.create_text(x, y, text=word, font=("Helvetica", 10, 'bold'), fill="black")
                bbox = wordboard.bbox(text)
                rect = wordboard.create_rectangle(bbox, fill="white", outline="white")
                wordboard.lower(rect, text)
                wordboard_pos.append(bbox)
                x += 90
        y += 50
        x = 70
        while i < 17:
            word = random.choice(words_data["Long"])
            if(not word in words):
                words.append(word)
                i += 1
                text = wordboard.create_text(x, y, text=word, font=("Helvetica", 10, 'bold'), fill="black")
                bbox = wordboard.bbox(text)
                rect = wordboard.create_rectangle(bbox, fill="white", outline="white")
                wordboard.lower(rect, text)
                wordboard_pos.append(bbox)
                x += 140
        tempwords = []
        for i in range(len(words)):
            if(" " in words[i]):
                tempwords.append(words[i].replace(" ", "").upper())
            else:
                tempwords.append(words[i].upper())
        print(tempwords)
        board = [['.' for _ in range(68)] for _ in range(25)]
        board_pos = [['.' for _ in range(68)] for _ in range(25)]
        indices = []
        for word in tempwords:
            indice = []
            placed = False
            while not placed:
                random.seed(random.randint(0, 12493914843))
                randomx = random.randint(0, len(board) - 1)
                randomy = random.randint(0, len(board[0]) - 1)
                deltax, deltay = random_direction()
                if(randomx + len(word) * deltax >= 0 and randomx + len(word) * deltax < len(board) and randomy + len(word) * deltay >= 0 and randomy + len(word) * deltay < len(board[0]) and no_letters(len(word), randomx, randomy, deltax, deltay, board)):
                    print(word)
                    for c in word:
                        indice.append((randomx, randomy))
                        board[randomx][randomy] = c
                        randomx += deltax
                        randomy += deltay
                    indices.append(indice)
                    placed = True
        not_unique = True
        while not_unique:
            board = populate(board)
            if(all_unique(board)):
                not_unique = False
    startx = 10
    starty = 10
    for i in range(len(board)):
        for e in range(len(board[i])):
            gameboard.create_rectangle(startx, starty, startx + 22, starty + 22)
            gameboard.create_text(startx + 11, starty + 11, text=board[i][e])
            board_pos[i][e] = (startx, starty)
            startx += 22
        startx = 10
        starty += 22


# reset game
def reset():
    global fall_button, spring_button, summer_button, winter_button, games_button, sports_button, food_button, animals_button, colors_button, ingame, canvas, container, scroll_frame_container, gameboard, wordboard, game_menu
    # reset variables
    ingame = False
    if(gameboard):
        gameboard.delete("all")
        root.config(menu=None)
        gameboard.destroy()
        gameboard = None
        wordboard.delete("all")
        wordboard.destroy()
        wordboard = None
        container.destroy()

    # create canvas and container
    container = ttk.Frame(root)
    canvas = tk.Canvas(container)
    container.pack(fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(bg="blue")
    scroll_frame_container = ScrollableFrame(root)
    scroll_frame_container.pack(fill='both', expand=True)
    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    # create buttons
    fall_button = tk.Button(scroll_frame_container.scrollable_frame, text="Fall", font=("Arial Rounded MT Bold", 40), fg="orange", compound=tk.CENTER, image=fall_photo, command=lambda: b_click(fall_button, 1))
    spring_button = tk.Button(scroll_frame_container.scrollable_frame, text="Spring", font=("Arial Rounded MT Bold", 40), fg="pink", compound=tk.CENTER, image=spring_photo, command=lambda: b_click(spring_button, 2))
    summer_button = tk.Button(scroll_frame_container.scrollable_frame, text="Summer", font=("Arial Rounded MT Bold", 40), fg="yellow", compound=tk.CENTER, image=summer_photo, command=lambda: b_click(summer_button, 3))
    winter_button = tk.Button(scroll_frame_container.scrollable_frame, text="Winter", font=("Arial Rounded MT Bold", 40), fg="blue", compound=tk.CENTER, image=winter_photo, command=lambda: b_click(winter_button, 4))
    games_button = tk.Button(scroll_frame_container.scrollable_frame, text="Games", font=("Arial Rounded MT Bold", 40), fg="green", compound=tk.CENTER, image=games_photo, command=lambda: b_click(games_button, 5))
    sports_button = tk.Button(scroll_frame_container.scrollable_frame, text="Sports", font=("Arial Rounded MT Bold", 40), fg="purple", compound=tk.CENTER, image=sports_photo, command=lambda: b_click(sports_button, 6))
    food_button = tk.Button(scroll_frame_container.scrollable_frame, text="Food", font=("Arial Rounded MT Bold", 40), fg="brown", compound=tk.CENTER, image=food_photo, command=lambda: b_click(food_button, 7))
    animals_button = tk.Button(scroll_frame_container.scrollable_frame, text="Animals", font=("Arial Rounded MT Bold", 40), fg="orange", compound=tk.CENTER, image=animals_photo, command=lambda: b_click(animals_button, 8))
    colors_button = tk.Button(scroll_frame_container.scrollable_frame, text="Colors", font=("Arial Rounded MT Bold", 40), fg="pink", compound=tk.CENTER, image=colors_photo, command=lambda: b_click(colors_button, 9))

    # place buttons
    fall_button.pack(pady=10, padx=10)
    spring_button.pack(pady=10, padx=10)
    summer_button.pack(pady=10, padx=10)
    winter_button.pack(pady=10, padx=10)
    games_button.pack(pady=10, padx=10)
    sports_button.pack(pady=10, padx=10)
    food_button.pack(pady=10, padx=10)
    animals_button.pack(pady=10, padx=10)
    colors_button.pack(pady=10, padx=10)

    # drawing board, strings, etc.
    canvas.create_text(width / 2, 100, text="Word Search", font=("Arial", 120))


reset()


root.mainloop()