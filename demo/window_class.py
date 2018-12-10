from Tkinter import *
from ttk import *
from PIL import Image, ImageTk
import imageio
import threading

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):
        # changing the title of our master widget      
        self.master.title("DL Demo")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)
        # create the file object)
        file = Menu(menu)

        file.add_command(label="Play", command=self.show_video)
        file.add_command(label="Exit", command=self.client_exit)
        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)
        # create the file object)
        # play = Menu(menu)
        # # adds a command to the menu option, calling it exit, and the
        # # command it runs on event is client_exit
        # play.
        # #added "file" to our menu
        # menu.add_cascade(label="play", menu=play)

        self.dropdown = self.set_dropdown(range(1, 11), position=[0, 0])

        exit_button = Button(self, text="quit", command=self.client_exit)
        exit_button.grid(row=2, column=0)


    def show_video(self):
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

        print("playing video {}".format(video_name))

        video = imageio.get_reader(video_name)

        video_label = Label(self)
        # video_label.grid(row=2, column=0)
        # video_label.place(x=20, y=20)
        video_label.pack()
        thread = threading.Thread(target=stream, args=(video_label,))
        thread.daemon = 1
        thread.start()


    def set_dropdown(self, video_list, position):

        def resizeFunc():
            newLen = len(dropdown.get())
            dropdown.configure(width=newLen+2)

        dropdown = Combobox(self, width=3,
            value=video_list,
            postcommand=resizeFunc)

        dropdown.current(0)
        dropdown.grid(row=position[0], column=position[1])
        return dropdown


    def client_exit(self):
        exit()

