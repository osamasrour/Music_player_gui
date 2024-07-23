from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import os
import pygame
from sys import exit
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3, ID3NoHeaderError
from tkinter import filedialog
from io import BytesIO
from datetime import timedelta
from button import Button

# initialize pygame
pygame.init()
# define the App status
AppStatus = "select window"

# window properties
WIDTH, HEIGHT = 400, 550
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

# make some buttons
play_btn = Button("Play", (170, 386), 20)
pouse_btn = Button("Pouse", (240, 386), 20)
rewind_btn = Button("Rewind", (70 , 386), 20)
next_btn = Button("#>", (350, 385), 20)
previosly_btn = Button("<#", (7, 385), 20)
select_btn = Button("Select", (110, 225), 55, bgcolor1="olive")

# ====== create the volume bar ======
def VolumeBar():
    # the volume bar
    pygame.draw.rect(WIN, (255, 51, 51), (50, 450, 300, 20))
    pygame.draw.rect(WIN, (51, 255, 51), (50, 450, pygame.mixer.music.get_volume() * 300, 20))
    # the volume value
    VolumeText = pygame.font.SysFont("Arial", 20).render(str(int(
                    pygame.mixer.music.get_volume() * 100)) + "%", 
                                        True, (127, 0, 255))
    WIN.blit(VolumeText, (355, 450))
    # control the volume value
    MousePosition = pygame.mouse.get_pos()
    if pygame.Rect(50, 450, 300, 20).collidepoint(*MousePosition):
        if pygame.mouse.get_pressed()[0] == True:
            pygame.mixer.music.set_volume((MousePosition[0] - 50) / 300)

# ======== create the RunTime Bar ========
RunTimePos = 0
timer_font = pygame.font.SysFont("Arial", 15)
def RunTimeBar(music_length):
    global RunTimePos, LinePosValue
    # find out how long the song has been going on in (sec)
    LinePosValue = RunTimePos + (pygame.mixer.music.get_pos() / 1000)
    # format the current position and the song's length in a readable string
    formater_time = str(timedelta(seconds=int(LinePosValue)))[2:]
    formater_length = str(timedelta(seconds=int(music_length)))[2:]
    # blit the formated string (current / song's length)
    timer_lable = timer_font.render(f"{formater_time} / {formater_length}", True, (0, 0, 0))
    WIN.blit(timer_lable, (150, 310))
    # representation on a straight line
    pygame.draw.rect(WIN, (255, 251, 251), (50, 332, 300, 5))
    pygame.draw.rect(WIN, "#32a85a", (50, 332, LinePosValue * 300 / music_length, 5))
    # control the current value of the lenght we reach
    MousePosition = pygame.mouse.get_pos()
    if pygame.Rect(50, 330, 300, 10).collidepoint(*MousePosition):
        if pygame.mouse.get_pressed()[0] == True:
            RunTimePos = (MousePosition[0] - 50) * music_length / 300
            pygame.mixer.music.play(start=RunTimePos)

# ======= blit the song name =======
def ShowName():
    """ the function blit the name of the current song """
    global song_name
    lable = pygame.font.SysFont("Arial", 15).render(song_name, True, (0, 0, 0))
    WIN.blit(lable, (WIDTH // 2 - lable.get_width() // 2, 360))

# ======= blit the music cover =======
cover_lable = pygame.font.SysFont("Arail", 40).render("Unvalid Cover", True, (0, 0, 0))
def MusicCover(song_path):
    # create a box to incloud th picture
    pygame.draw.rect(WIN, "#9d9d9d", (75, 50, 250, 250), border_radius=50)
    try:
        # get the picture from the song's metadata if exist
        pic = ID3(song_path).get("APIC:").data
        cover = pygame.transform.scale(pygame.image.load(BytesIO(pic)), (200, 200))
        WIN.blit(cover, (100, 75))
    except (AttributeError, ID3NoHeaderError):
        # if the song does't have a cover blit the cover_lable => Unvalid Cover
        WIN.blit(cover_lable, (200 - cover_lable.get_width() // 2,
                                175 - cover_lable.get_height() // 2))

# ======= the current music handler ========
# the pointer => pointing to the current song in the list
pointer = 0
# music handler function
def MusicSetHandler(songs_list: list, vel: int):
    """
    the function plays the next or the previous song
    in songs_list depending on the parameter "vel"
    """
    global pointer, music_length, song_name, RunTimePos, song_path
    # reset the run time position
    RunTimePos = 0
    # move the pointer
    pointer += vel
    # get the song' path and name
    song_path = os.path.join(songs_list[pointer])
    song_name = os.path.basename(song_path)[:40] + "..."
    try:
        # try to get the length if the song is not corrupted
        music_length = MP3(song_path).info.length
    except HeaderNotFoundError:
        # if the song is corrupted make the length = -1
        music_length = -1
    # unload the current song from the memory
    pygame.mixer.music.unload()
    # load the new song and play it
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

# ====== music player Window ======
def MusicPlayer():
    global music_length, pointer, song_path, songs_list, RunTimePos, LinePosValue
    # call some functions
    RunTimeBar(music_length)
    ShowName()
    VolumeBar()
    # draw the needed buttons and add functionality to it
    next_btn.draw(WIN)
    previosly_btn.draw(WIN)
    if next_btn.isclicked():
        if pointer < len(songs_list) - 1:
            MusicSetHandler(songs_list, 1)
        else:
            pointer = 0
            MusicSetHandler(songs_list, 0)
    elif previosly_btn.isclicked():
        if pointer > 0:
            MusicSetHandler(songs_list, -1)
        else:
            MusicSetHandler(songs_list, len(songs_list) -1)
    play_btn.draw(WIN)
    if play_btn.isclicked():
        pygame.mixer.music.unpause()
    pouse_btn.draw(WIN)
    if pouse_btn.isclicked():
        pygame.mixer.music.pause()
    rewind_btn.draw(WIN)
    if rewind_btn.isclicked():
        pygame.mixer.music.play()
        RunTimePos = 0
    if LinePosValue >= music_length - 1 and pointer < len(songs_list) - 1:
        MusicSetHandler(songs_list, 1)
    elif LinePosValue >= music_length - 1 and pointer == len(songs_list) - 1:
        pointer = 0
        MusicSetHandler(songs_list, 0)
    # Draw the song cover
    MusicCover(song_path)

# ====== select window ======
def SelectMenu():
    global AppStatus, songs_list
    # draw the select button and make it usefull
    select_btn.draw(WIN)
    if select_btn.isclicked() == True:
        # make a list so we can handle the songs in it
        songs_list = []
        # open a pop-up window to select the required files
        for song in filter(lambda filename : os.path.splitext(filename)[1] in (".mp3",),
                            list(filedialog.askopenfilenames())):
            # add the file that have .mp3 as an extention to the list by using filter
            songs_list.append(song)
        # switch the AppStatus to "music player" if we selected some songs
        if len(songs_list) > 0:
            MusicSetHandler(songs_list, pointer)
            AppStatus = "music player"

def App():
    # Main loop
    while True:
        # fill the window by Hex color
        WIN.fill("#c4c4c4")
        # set up the window FPS
        pygame.time.Clock().tick(60)
        # control the App Status flow
        if AppStatus == "select window":
            SelectMenu()
        elif AppStatus == "music player":
            MusicPlayer()
        # event handler
        for event in pygame.event.get():
            # check if the user quit the app
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # updata the window every frame
        pygame.display.update()

# Run the App from the current file only
if __name__ == "__main__":
    App()
    # delete the modulse from the memory after closing the App
    del (environ, os, pygame, exit, MP3, HeaderNotFoundError, ID3, 
            ID3NoHeaderError, filedialog, BytesIO, timedelta, Button)