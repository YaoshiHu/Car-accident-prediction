from Tkinter import *
from ttk import *
from PIL import Image, ImageTk
import imageio
import threading
import sys, os, time
import numpy as np

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("DL Demo")
        self.pack(fill=BOTH, expand=True)

        result_file = np.load(os.path.join("data", "prediction.npz"))
        self.scores = result_file["data"]
        print("npz file loaded")

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Play", command=self.play_video)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        self.title_frame = Frame(self)
        self.title_frame.pack(side=TOP)
        title_panel = Label(self.title_frame, text="Anticipating Accident in self-involve dashcam videos")
        title_panel.config(font=("Arial", 44))
        title_panel.pack(fill=BOTH, expand=True)

        self.group_member = Frame(self)
        self.group_member.pack(side=TOP)
        group_panel = Label(self.group_member, text="Yimeng Lei (yl3747), Yinan Wang (yw2924), Yaoshi Hu (yh2950)")
        group_panel.config(font=("Times New Roman", 30))
        group_panel.pack(fill=BOTH, expand=True)

        # first frame with dropdown and play botton
        self.frame1 = Frame(self)
        self.frame1.pack(side=TOP)

        # frame2 is used fo the video
        self.frame2 = Frame(self)
        self.frame2.pack(fill=X)

        # frame3 is used for the prediction plotting
        self.frame3 = Frame(self)
        self.frame3.pack(fill=X)

        self.project_abstract = Frame(self)
        self.project_abstract.pack(fill=X)

        summary_label = Label(self.frame2, text="Precision=100%")
        summary_label.config(font=("Times New Roman", 36))
        summary_label.pack(side=TOP, padx=10, pady=20)

        self.video_label = Label(self.frame3)
        self.video_label.pack(side=LEFT, padx=10, pady=40)

        self.score_label = Label(self.frame3)
        self.score_label.pack(side=RIGHT, padx=10, pady=40)

        video_text = Label(self.frame1, text="Select video # ")
        video_text.pack(side=LEFT, padx=5, pady=10)

        self.dropdown = self.set_dropdown(self.frame1, range(1, 11), LEFT)

        play_button = Button(self.frame1, text="play", command=self.play_video)
        play_button.pack(side=LEFT, padx=5, pady=20)

        exit_button = Button(self.frame1, text="quit", command=self.client_exit)
        exit_button.pack(side=LEFT, padx=5, pady=20)

        abstract = "THE BEST PROJECT!"

        project_summary = Label(self.project_abstract, text=abstract)
        project_summary.config(font=("Times New Roman", 20))
        project_summary.pack(side=TOP, padx=10, pady=20)

    def play_video(self):
        video_dir = "data/"

        def stream(video_label, score_label):
            video_label.config(image='')
            score_label.config(image='')
            try:
                index = 0
                for image in video.iter_data():
                    frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize((950, 420)))
                    video_label.config(image=frame_image)
                    video_label.image = frame_image

                    if index < 90:
                        img = os.path.join(score_dir, "000{}.jpg".format(index)[-8:])
                        score_image = ImageTk.PhotoImage(Image.open(img))
                        score_label.config(image=score_image)
                        score_label.image = score_image

                    index += 1
            except:
                print("Quit unexpectedly")

        video_id = "{}.mp4".format(self.dropdown.get())
        video_name = os.path.join(video_dir, "videos", video_id)
        score_dir = os.path.join("data/scores", self.dropdown.get())

        print("playing video {}".format(video_name))

        video = imageio.get_reader(video_name)

        thread = threading.Thread(target=stream, args=(self.video_label, self.score_label, ))
        thread.daemon = 1
        thread.start()

    def set_dropdown(self, frame, video_list, position):

        def resizeFunc():
            newLen = len(dropdown.get())
            dropdown.configure(width=newLen+2)

        dropdown = Combobox(frame, width=3,
            value=video_list,
            postcommand=resizeFunc)

        dropdown.current(0)
        dropdown.pack(side=position, padx=5, pady=20)
        return dropdown

    def client_exit(self):
        self.quit()
        self.destroy()
        exit()

