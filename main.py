import os
import tkinter as tk
from tkinter import ttk
import pygame
from PIL import Image, ImageTk
import pygame.mixer
import random

current_song_index = 0
is_playing = False
is_paused = False


pygame.init()

#create tkinter window
root = tk.Tk()
root.geometry("800x550+200+100")
root.title("SYMPHONY")

#Create the main frame
main_frame = tk.Frame(root)
main_frame.place(x=220, y=0, width=580, height=470)


#Open the gif file to display it in main frame
gif_file = Image.open("icons/fxVE.gif")
gif_file = gif_file.resize((300, 300), resample=Image.Resampling.LANCZOS)

#Create an image object from the gif file
gif_image = ImageTk.PhotoImage(gif_file)

#Create a label widget to display the gif
gif_label = tk.Label(main_frame, image=gif_image, width=580, height=300)
gif_label.place(x=0, y=30)
gif_label.config(bg='black')


#progress bar for playing music
song_progress = ttk.Progressbar(main_frame, orient='horizontal', length=500, mode='determinate')
song_progress.place(x=40, y=350)


#Create the button images
shuffle_img = ImageTk.PhotoImage(Image.open("icons/shuffle.png").resize((39, 39)))
prev_img = ImageTk.PhotoImage(Image.open("icons/prev.png").resize((50, 50)))
play_img = ImageTk.PhotoImage(Image.open("icons/play.png").resize((50, 50)))
next_img = ImageTk.PhotoImage(Image.open("icons/next.png").resize((50, 50)))
vol_img = ImageTk.PhotoImage(Image.open("icons/vol.png").resize((45, 45)))


"""
To shuffle play the songs in the list
"""
def play_random_song():
    current_song_index = random.randint(0, len(mp3_files) - 1)
    mp3_listbox.selection_clear(0, 'end')
    mp3_listbox.activate(current_song_index)
    mp3_listbox.selection_set(current_song_index, last=None)
    selected_song = mp3_listbox.get(current_song_index)
    file_path = os.path.join("/home/gedion/Music", selected_song)
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f'Error: {e}')


shuffle_button = tk.Button(main_frame, image=shuffle_img, bd=0, command=play_random_song)
shuffle_button.place(x=70, y=405.5)



'''
This function updates the progress.
'''
def update_progress():
    if pygame.mixer.music.get_length() != 0:
        song_progress["value"] = round(pygame.mixer.music.get_pos() * 100 / pygame.mixer.music.get_length(), 2)
    root.after(100, update_progress)

'''
This function plays the selected song when pressed as well as stops and resumes the current playing song.
'''
#to use it in below function
play_img = ImageTk.PhotoImage(file="icons/play.png")
pause_img = ImageTk.PhotoImage(file="icons/resume.png")

def play_selected_song():
    global is_playing
    global is_paused

    #checks the current state of the music and change the button image accordingly
    if is_paused:
        play_button.config(image=play_img)
    else:
        play_button.config(image=pause_img)

    selected_song = mp3_listbox.get(mp3_listbox.curselection())
    file_path = os.path.join("/home/gedion/Music", selected_song)
    try:
        song = pygame.mixer.Sound(file_path)
        song_length = song.get_length() * 1000  # convert to milliseconds
        time_interval = song_length / 100  # dividing song length by 100 updates
        if is_playing:
            if is_paused:
                pygame.mixer.music.unpause()
                song_progress.start()
                is_paused = False
                play_button.config(image=pause_img)
            else:
                pygame.mixer.music.pause()
                song_progress.stop()
                is_paused = True
                play_button.config(image=play_img)
        else:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            song_progress.start()
            song_progress["maximum"] = song_length
            is_playing = True
    except Exception as e:
        print(f'Error: {e}')
        play_button.config(image=play_img)


play_button = tk.Button(main_frame, image=play_img, bd=0, command=lambda: play_selected_song())
play_button.place(x=250, y=400)


'''
This function stops the current playing song and plays the next song in the list.
'''
def play_next_song():
    current_song_index = mp3_listbox.curselection()[0]
    current_song_index += 1
    if current_song_index >= len(mp3_files):
        current_song_index = 0
    mp3_listbox.selection_clear(0, 'end')
    mp3_listbox.activate(current_song_index)
    mp3_listbox.selection_set(current_song_index, last=None)
    selected_song = mp3_listbox.get(current_song_index)
    file_path = os.path.join("/home/gedion/Music", selected_song)
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f'Error: {e}')


next_button = tk.Button(main_frame, image=next_img, bd=0, command=play_next_song)
next_button.place(x=340, y=400)


"""
To play previously played song in the list
"""
def play_prev_song():
    current_song_index = mp3_listbox.curselection()[0]
    current_song_index -= 1
    if current_song_index < 0:
        current_song_index = len(mp3_files) - 1
    mp3_listbox.selection_clear(0, 'end')
    mp3_listbox.activate(current_song_index)
    mp3_listbox.selection_set(current_song_index, last=None)
    selected_song = mp3_listbox.get(current_song_index)
    file_path = os.path.join("/home/gedion/Music", selected_song)
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f'Error: {e}')


# Create the previous button
prev_button = tk.Button(main_frame, image=prev_img, bd=0, command=play_prev_song)
prev_button.place(x=155, y=400)



"""
This function creates a slider for volume
"""
def toggle_volume_slider():
    global volume_slider
    volume_slider.place(x=480, y=370)


# icon for the button volume
vol_img = ImageTk.PhotoImage(Image.open("icons/vol.png"))
vol_button = tk.Button(main_frame, image=vol_img, bd=0, command=toggle_volume_slider)
vol_button.place(x=430, y=403)



"""
This function decides which icon to show when volume is > 0 or volume is = 0
"""
def volume(value):
    global vol_img
    global vol_button
    volume = volume_slider.get()
    pygame.mixer.music.set_volume(volume / 10)
    if volume == 0:
        vol_img = ImageTk.PhotoImage(Image.open("icons/mute.png"))
        vol_button.config(image=vol_img)
    else:
        vol_img = ImageTk.PhotoImage(Image.open("icons/vol.png"))
        vol_button.config(image=vol_img)


volume_slider = tk.Scale(main_frame, from_=10, to=0, orient="vertical", command=volume, length=80, width=8)
volume_slider.set(5)


# Create the sidebar frame
sidebar_frame = tk.Frame(root, bg="black")
sidebar_frame.place(x=0, y=0, width=220, height=550)

# Create the all songs label
all_songs_label = tk.Label(sidebar_frame, text="ALL SONGS", bg="black", fg="white", font=("Helvetica", 14, "bold"))
all_songs_label.place(x=0, y=15, width=220, height=20), all_songs_label.config(anchor='center')

# Create the all songs frame
all_songs_frame = tk.Frame(sidebar_frame, bg="black", width=220, height=20)
all_songs_frame.place(x=0, y=30)

# Find all mp3 files in the specific directory
mp3_files = [f for f in os.listdir("/home/gedion/Music") if f.endswith(".mp3")]

# Create the listbox to display the mp3 files
mp3_listbox = tk.Listbox(sidebar_frame)
mp3_listbox.place(x=0, y=33, width=220, height=520)

# Insert the mp3 files into the listbox
for file in mp3_files:
    mp3_listbox.insert(tk.END, file)


if __name__ == '__main__':
    root.mainloop()