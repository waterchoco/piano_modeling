#basic library imports for Piano in Python
import pygame
import piano_lists as pl
from pygame import mixer
import io

#this will initialize the pygame library
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(50)


# Create a silent sound buffer with proper WAV headers
def create_silent_sound(duration=1):
    byte_rate = 44100 * 2  # 44100 samples per second, 2 bytes per sample
    num_samples = 44100 * duration
    data_size = num_samples * 2
    o = io.BytesIO()
    o.write(b'RIFF')
    o.write((data_size + 36).to_bytes(4, 'little'))  # Size of the rest of the file
    o.write(b'WAVEfmt ')
    o.write((16).to_bytes(4, 'little'))  # Subchunk size (PCM)
    o.write((1).to_bytes(2, 'little'))  # Audio format (1 is PCM)
    o.write((1).to_bytes(2, 'little'))  # Num channels
    o.write((44100).to_bytes(4, 'little'))  # Sample rate
    o.write((byte_rate).to_bytes(4, 'little'))  # Byte rate
    o.write((2).to_bytes(2, 'little'))  # Block align
    o.write((16).to_bytes(2, 'little'))  # Bits per sample
    o.write(b'data')
    o.write(data_size.to_bytes(4, 'little'))
    o.write(b'\x00' * data_size)
    o.seek(0)
    return mixer.Sound(o)

# Create a 1-second silent sound
silent_sound = create_silent_sound()


#this is the path to fonts that we will use
#other variables for the sound and window
font = pygame.font.SysFont('arial', 48)
#the below is the declaration for the different size of fonts that we are going to use
medium_font = pygame.font.SysFont('arial', 28)
small_font = pygame.font.SysFont('arial', 16)
real_small_font = pygame.font.SysFont('arial', 10)
fps = 60

#enables the creation of a fresh Clock object that may be used to monitor time. Additionally, the clock offers a number of options for regulating the framerate of a game.
#Every frame should include one call to this function. It will calculate the number of milliseconds since the last call.
timer = pygame.time.Clock()
WIDTH = 14.8 * 19
HEIGHT = 400
screen = pygame.display.set_mode([WIDTH, HEIGHT])

active_whites = []
active_blacks = []
left_oct = 4
right_oct = 5

left_hand = pl.left_hand
right_hand = pl.right_hand
piano_notes = pl.piano_notes
white_notes = pl.white_notes
black_notes = pl.black_notes
black_labels = pl.black_labels


# Variables for the sound
white_sounds = []
black_sounds = []

# Load sound files for white and black notes, or use silent sound if not found
file_location = "C:/PyCharm 2024.1/Piano Project/"


for filename in pl.white_notes:
    try:
        sound = mixer.Sound(f'{file_location}{filename}.wav')

    except FileNotFoundError:
        sound = silent_sound
    white_sounds.append(sound)

for filename1 in pl.black_labels :
    try:
        sound = mixer.Sound(f'{file_location}{filename1}.wav')
    except FileNotFoundError:
        sound = silent_sound
    black_sounds.append(sound)


#this function will draw the piano keys on the window of Piano in Python
def draw_piano(whites, blacks):
    white_rects = []
    for i in range(52):
        #we made use of rect() function in order to draw the key of the piano for white keys
        rect = pygame.draw.rect(screen, 'white', [i * 35-803.8, HEIGHT - 300, 35, 300], 0, 2)
        white_rects.append(rect)
        #same goes for black keys on paino
        pygame.draw.rect(screen, 'black', [i * 35-803.8, HEIGHT - 300, 35, 300], 2, 2)
        key_label = small_font.render(white_notes[i], True, 'black')
        screen.blit(key_label, (i * 35-803.8 + 3, HEIGHT - 20))
    skip_count = 0
    last_skip = 2
    skip_track = 2
    black_rects = []
    for i in range(36):
        #this is to draw the small black rectangles on the larger keys in GUI Piano in Python
        rect = pygame.draw.rect(screen, 'black', [23 + (i * 35-803.8) + (skip_count * 35), HEIGHT - 300, 24, 200], 0, 2)
        for q in range(len(blacks)):
            #this conditional will keep thrack of the green marker that we want to show up on each key
            #whenever a user pesses the key of Piano App in Python, a green marker should show up
            if blacks[q][0] == i:
                if blacks[q][1] > 0:
                    pygame.draw.rect(screen, 'green', [23 + (i * 35-803.8) + (skip_count * 35), HEIGHT - 300, 24, 200], 2, 2)
                    blacks[q][1] -= 1

        #this variable will handle all the labels that the keys will have in our project
        key_label = real_small_font.render(black_labels[i], True, 'white')
        screen.blit(key_label, (25 + (i * 35) + (skip_count * 35)-803.8, HEIGHT - 120))
        black_rects.append(rect)
        skip_track += 1
        if last_skip == 2 and skip_track == 3:
            last_skip = 3
            skip_track = 0
            skip_count += 1
        elif last_skip == 3 and skip_track == 2:
            last_skip = 2
            skip_track = 0
            skip_count += 1

    for i in range(len(whites)):
        if whites[i][1] > 0:
            j = whites[i][0]
            pygame.draw.rect(screen, 'green', [j * 35-803.8, HEIGHT - 300, 35, 300], 2, 2)
            whites[i][1] -= 1

    return white_rects, black_rects, whites, blacks


def draw_hands(rightOct, leftOct, rightHand, leftHand):
    # left hand
    pygame.draw.rect(screen, 'dark gray', [(leftOct * 245) - 175 -803.8, HEIGHT - 60, 245, 30], 0, 4)
    pygame.draw.rect(screen, 'black', [(leftOct * 245) - 175 -803.8, HEIGHT - 60, 245, 30], 4, 4)
    text = small_font.render(leftHand[0], True, 'white')
    screen.blit(text, ((leftOct * 245) - 165-803.8, HEIGHT - 55))
    text = small_font.render(leftHand[2], True, 'white')
    screen.blit(text, ((leftOct * 245) - 130-803.8, HEIGHT - 55))
    text = small_font.render(leftHand[4], True, 'white')
    screen.blit(text, ((leftOct * 245) - 95-803.8, HEIGHT - 55))
    text = small_font.render(leftHand[5], True, 'white')
    screen.blit(text, ((leftOct * 245) - 60-803.8, HEIGHT - 55))
    text = small_font.render(leftHand[7], True, 'white')
    screen.blit(text, ((leftOct * 245) - 25-803.8, HEIGHT - 55))
    text = small_font.render(leftHand[9], True, 'white')
    screen.blit(text, ((leftOct * 245) + 10-803.8, HEIGHT - 55))
    text = small_font.render(leftHand[11], True, 'white')
    screen.blit(text, ((leftOct * 245) + 45-803.8, HEIGHT - 55))
    text = small_font.render(leftHand[1], True, 'black')
    screen.blit(text, ((leftOct * 245) - 148-803.8, HEIGHT - 55))
    text = small_font.render(leftHand[3], True, 'black')
    screen.blit(text, ((leftOct * 245) - 113-803.8, HEIGHT - 55))
    text = small_font.render(leftHand[6], True, 'black')
    screen.blit(text, ((leftOct * 245) - 43-803.8, HEIGHT - 55))
    text = small_font.render(leftHand[8], True, 'black')
    screen.blit(text, ((leftOct * 245) - 8-803.8, HEIGHT - 55))
    text = small_font.render(leftHand[10], True, 'black')
    screen.blit(text, ((leftOct * 245) + 27-803.8, HEIGHT - 55))
    # right hand
    pygame.draw.rect(screen, 'dark gray', [(rightOct * 245) - 175-803.8, HEIGHT - 60, 245, 30], 0, 4)
    pygame.draw.rect(screen, 'black', [(rightOct * 245) - 175-803.8, HEIGHT - 60, 245, 30], 4, 4)
    text = small_font.render(rightHand[0], True, 'white')
    screen.blit(text, ((rightOct * 245) - 165-803.8, HEIGHT - 55))
    text = small_font.render(rightHand[2], True, 'white')
    screen.blit(text, ((rightOct * 245) - 130-803.8, HEIGHT - 55))
    text = small_font.render(rightHand[4], True, 'white')
    screen.blit(text, ((rightOct * 245) - 95-803.8, HEIGHT - 55))
    text = small_font.render(rightHand[5], True, 'white')
    screen.blit(text, ((rightOct * 245) - 60-803.8, HEIGHT - 55))
    text = small_font.render(rightHand[7], True, 'white')
    screen.blit(text, ((rightOct * 245) - 25-803.8, HEIGHT - 55))
    text = small_font.render(rightHand[9], True, 'white')
    screen.blit(text, ((rightOct * 245) + 10-803.8, HEIGHT - 55))
    text = small_font.render(rightHand[11], True, 'white')
    screen.blit(text, ((rightOct * 245) + 45-803.8, HEIGHT - 55))
    text = small_font.render(rightHand[1], True, 'black')
    screen.blit(text, ((rightOct * 245) - 148-803.8, HEIGHT - 55))
    text = small_font.render(rightHand[3], True, 'black')
    screen.blit(text, ((rightOct * 245) - 113-803.8, HEIGHT - 55))
    text = small_font.render(rightHand[6], True, 'black')
    screen.blit(text, ((rightOct * 245) - 43-803.8, HEIGHT - 55))
    text = small_font.render(rightHand[8], True, 'black')
    screen.blit(text, ((rightOct * 245) - 8-803.8, HEIGHT - 55))
    text = small_font.render(rightHand[10], True, 'black')
    screen.blit(text, ((rightOct * 245) + 27-803.8, HEIGHT - 55))

#this will draw the upper section of Piano GUI In Python
def draw_title_bar():
    '''
    instruction_text = medium_font.render('Up/Down Arrows Change Left Hand', True, 'black')
    screen.blit(instruction_text, (WIDTH - 500, 10))
    instruction_text2 = medium_font.render('Left/Right Arrows Change Right Hand', True, 'black')
    screen.blit(instruction_text2, (WIDTH - 500, 50))
    '''
    title_text = font.render('Play Piano', True, 'white')
    screen.blit(title_text, (43, 18))
    title_text = font.render('Play Piano!', True, 'black')
    screen.blit(title_text, (45, 20))
    instruction_text2 = real_small_font.render('215357_Jeong Min Lee, 215363_ Jin Woo Lee, 233262_Min Sun Kim', True, 'black')
    screen.blit(instruction_text2, (WIDTH - 280, 10))


run = True
#while loop for all the keys
while run:
    left_dict = {'Z': f'C{left_oct}',
                 'S': f'C#{left_oct}',
                 'X': f'D{left_oct}',
                 'D': f'D#{left_oct}',
                 'C': f'E{left_oct}',
                 'V': f'F{left_oct}',
                 'G': f'F#{left_oct}',
                 'B': f'G{left_oct}',
                 'H': f'G#{left_oct}',
                 'N': f'A{left_oct}',
                 'J': f'A#{left_oct}',
                 'M': f'B{left_oct}'}

    right_dict = {'R': f'C{right_oct}',
                  '5': f'C#{right_oct}',
                  'T': f'D{right_oct}',
                  '6': f'D#{right_oct}',
                  'Y': f'E{right_oct}',
                  'U': f'F{right_oct}',
                  '8': f'F#{right_oct}',
                  'I': f'G{right_oct}',
                  '9': f'G#{right_oct}',
                  'O': f'A{right_oct}',
                  '0': f'A#{right_oct}',
                  'P': f'B{right_oct}'}
    timer.tick(fps)
    screen.fill('gray')
    white_keys, black_keys, active_whites, active_blacks = draw_piano(active_whites, active_blacks)
    draw_hands(right_oct, left_oct, right_hand, left_hand)
    draw_title_bar()

    #this for loop is to handle the mouse click events in Piano in Python

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            black_key = False
            for i in range(len(black_keys)):
                #The PyGame Rect class has documentation on the point-collision. In essence, you provide PyGame a coordinate.
                # If a point is located inside the boundaries of the rectangle, the function Rect. collidepoint() will return True.
                if black_keys[i].collidepoint(event.pos):
                    black_sounds[i].play(0, 1000)
                    black_key = True
                    active_blacks.append([i, 30])
            for i in range(len(white_keys)):
                if white_keys[i].collidepoint(event.pos) and not black_key:

                    white_sounds[i].play(0,3000)
                    active_whites.append([i, 30])
        if event.type == pygame.TEXTINPUT:
            if event.text.upper() in left_dict:
                if left_dict[event.text.upper()][1] == '#':
                    #The Python index() function aids in locating a certain element's or item's position inside a string of characters or a list of items.
                    #It produces the list's supplied element's lowest possible index.
                    #A ValueError is returned if the requested item doesn't exist in the list.
                    index = black_labels.index(left_dict[event.text.upper()])
                    black_sounds[index].play(0, 1000)
                    active_blacks.append([index, 30])
                else:
                    index = white_notes.index(left_dict[event.text.upper()])
                    white_sounds[index].play(0, 1000)
                    active_whites.append([index, 30])
            if event.text.upper() in right_dict:
                if right_dict[event.text.upper()][1] == '#':
                    index = black_labels.index(right_dict[event.text.upper()])
                    #black_sounds[index].play(0, 1000)
                    active_blacks.append([index, 30])
                else:
                    index = white_notes.index(right_dict[event.text.upper()])
                    white_sounds[index].play(0, 1000)
                    active_whites.append([index, 30])

        #this conditional block is to handle the arrow keys event for the working of Piano in Python
        #we used conditionals to keep track of the arrow keys press event

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if right_oct < 8:
                    right_oct += 1
            if event.key == pygame.K_LEFT:
                if right_oct > 0:
                    right_oct -= 1
            if event.key == pygame.K_UP:
                if left_oct < 8:
                    left_oct += 1
            if event.key == pygame.K_DOWN:
                if left_oct > 0:
                    left_oct -= 1


    pygame.display.flip()
#this will quite the  window of the pygame
pygame.quit() 