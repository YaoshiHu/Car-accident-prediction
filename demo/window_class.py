from Tkinter import *
from ttk import *
from PIL import Image, ImageTk
import imageio
import threading
import sys, os, time
import numpy as np

video_size = (950, 420)
plot_size = (600, 420)
cur_dir = os.path.dirname(os.path.realpath(__file__))

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

        Style().configure('green/red.TLabel', foreground='red')

    def init_window(self):
        self.master.title("DL Demo")
        self.pack(fill=BOTH, expand=True)

        result_file = np.load(os.path.join(cur_dir, "data", "prediction.npz"))
        self.scores = result_file["data"]
        print("npz file loaded")

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Play", command=self.play_video)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="Control", menu=file)

        self.title_frame = Frame(self)
        self.title_frame.pack(side=TOP)
        title_panel = Label(self.title_frame, text="Anticipating Accident in self-involve dashcam videos")
        title_panel.config(font=("Arial", 44))
        title_panel.pack(fill=BOTH, expand=True)

        self.group_member = Frame(self)
        self.group_member.pack(side=TOP)

        self.button_frame = Frame(self)
        self.button_frame.pack(side=TOP)

        # frame2 is used for result
        self.result_frame = Frame(self)
        self.result_frame.pack(fill=X)

        self.video_frame = Frame(self)
        self.video_frame.pack(fill=X)

        self.summary_frame = Frame(self)
        self.summary_frame.pack(fill=X)

        self.set_group_frame()
        self.set_button_frame()
        self.set_result_frame()
        self.set_video_frame()
        self.set_summary_frame()
        
    def set_group_frame(self):
        group_panel = Label(self.group_member, text="Yimeng Lei (yl3747), Yinan Wang (yw2924), Yaoshi Hu (yh2950)")
        group_panel.config(font=("Times New Roman", 30))
        group_panel.pack(fill=BOTH, expand=True)

    def set_button_frame(self):
        video_text = Label(self.button_frame, text="Select video #")
        video_text.pack(side=LEFT, padx=2, pady=10)

        self.dropdown = self.set_dropdown(self.button_frame, range(1, 11), LEFT)

        play_button = Button(self.button_frame, text="play", command=self.play_video)
        play_button.pack(side=LEFT, padx=5, pady=20)

        exit_button = Button(self.button_frame, text="exit", command=self.client_exit, style='green/red.TLabel')
        exit_button.pack(side=LEFT, padx=5, pady=20)

    def set_result_frame(self):
        label_text = "GCN-AdaLEU: Average precision: 0.9457, Recall=80%, Time to accident: 1.368"
        summary_label = Label(self.result_frame, text=label_text)
        summary_label.config(font=("Times New Roman", 30))
        summary_label.pack(side=TOP, padx=10, pady=10)

    def set_video_frame(self):
        self.video_label = Label(self.video_frame)
        self.video_label.pack(side=LEFT, padx=10, pady=30)

        self.score_label = Label(self.video_frame)
        self.score_label.pack(side=RIGHT, padx=10, pady=30)

    def set_summary_frame(self):
        abstract = '''
        Problem: Predicting whether car accident could happen inthe near future given video recorded by Dash-Cam.
        Our contributions:
        1. Collected a complex car collision datasetwhich could be used at first view car accidentanticipation.
        2. Verified the feature extracted from MaskR-CNN is effective in anticipating car accident.
        3. Proposed a mechanism of fusing graph mapwith object feature.'''

        # the width is defined in text unit
        project_summary = Label(self.summary_frame, text=abstract)
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
                    frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize(video_size))
                    video_label.config(image=frame_image)
                    video_label.image = frame_image

                    if index < 90:
                        img = os.path.join(cur_dir, score_dir, "000{}.jpg".format(index)[-8:])
                        read_score_image = Image.open(img).resize(plot_size)
                        score_image = ImageTk.PhotoImage(read_score_image)
                        score_label.config(image=score_image)
                        score_label.image = score_image

                    index += 1
            except:
                print("Quit unexpectedly")

        video_id = "{}.mp4".format(self.dropdown.get())
        video_name = os.path.join(cur_dir, video_dir, "videos", video_id)
        score_dir = os.path.join(cur_dir, "data/scores", self.dropdown.get())

        print("playing video {}".format(video_name))

        video = imageio.get_reader(video_name)

        thread = threading.Thread(target=stream, args=(self.video_label, self.score_label, ))
        thread.daemon = 1
        thread.start()

    def set_dropdown(self, frame, video_list, position):

        def resizeFunc():
            newLen = len(dropdown.get())
            dropdown.configure(width=newLen+1)

        dropdown = Combobox(frame, width=2,
            value=video_list,
            postcommand=resizeFunc)

        dropdown.current(0)
        dropdown.pack(side=position, padx=2, pady=20)
        return dropdown

    def client_exit(self):
        self.quit()
        self.destroy()
        exit()

