from Tkinter import *
from ttk import *
from PIL import Image, ImageTk
import imageio
import threading
import sys, os

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("DL Demo")
        self.pack(fill=BOTH, expand=True)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Play", command=self.show_video)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        # first frame with dropdown and play botton
        self.frame1 = Frame(self)
        self.frame1.pack(fill=X)

        video_text = Label(self.frame1, text="Select video # ")
        video_text.pack(side=LEFT, padx=5, pady=5)

        self.dropdown = self.set_dropdown(range(1, 11), LEFT)

        play_button = Button(self.frame1, text="play", command=self.show_video)
        play_button.pack(side=LEFT, padx=5, pady=5)

        exit_button = Button(self.frame1, text="quit", command=self.client_exit)
        exit_button.pack(side=LEFT, padx=5, pady=5)

        # frame2 is used fo the video
        self.frame2 = Frame(self)
        self.frame2.pack(fill=X)


    def show_video(self):
        video_dir = "data/"

        def stream(label):
            label.config(image='')

            try:
                for image in video.iter_data():
                    frame_image = ImageTk.PhotoImage(Image.fromarray(image))
                    label.config(image=frame_image)
                    label.image = frame_image
            except:
                print("Quit unexpectedly")
            finally:
                label.config(image='')

        video_id = self.dropdown.get()

        if video_id in [str(i) for i in range(1, 6)]:
            video_name = "0123.mp4" #This is your video file path
        else:
            video_name = "0440.mp4"

        video_name = os.path.join(video_dir, video_name)

        print("playing video {}".format(video_name))

        video = imageio.get_reader(video_name)

        video_label = Label(self.frame2)
        video_label.pack(side=TOP, padx=5, pady=5)
        thread = threading.Thread(target=stream, args=(video_label,))
        thread.daemon = 1
        thread.start()


    def set_dropdown(self, video_list, position):

        def resizeFunc():
            newLen = len(dropdown.get())
            dropdown.configure(width=newLen+2)

        dropdown = Combobox(self.frame1, width=3,
            value=video_list,
            postcommand=resizeFunc)

        dropdown.current(0)
        dropdown.pack(side=position, padx=5, pady=5)
        return dropdown


    def client_exit(self):
        exit()

