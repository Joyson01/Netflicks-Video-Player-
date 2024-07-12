import tkinter as tk
import webbrowser
from datetime import timedelta

import vlc
from PIL import Image, ImageTk


class App:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='black')
        self.root.attributes("-fullscreen", True)
        self.root.iconbitmap('Images/nf_icon.ico')
        self.sc_width, self.sc_height = root.winfo_screenwidth(), root.winfo_screenheight()
        self.thumb_width, self.thumb_height = max(int(self.sc_width * 0.2), 50), max(int(self.sc_height * 0.2), 50)
        self.play_intro_video()

    def resize_ico(self, image_path, width_factor, height_factor):
        width = max(int(self.sc_width * width_factor), 50)
        height = max(int(self.sc_height * height_factor), 50)
        return ImageTk.PhotoImage(Image.open(image_path).resize((width, height), Image.LANCZOS))

    def play_intro_video(self):
        def show_profile_selection():
            player.stop()
            self.profile_selection()

        instance = vlc.Instance()
        player = instance.media_player_new()
        player.set_media(instance.media_new("Audio/nf.mp4"))
        player.set_fullscreen(True)
        player.play()
        self.root.after(5000, show_profile_selection)

    def profile_selection(self):
        def open_url(url):
            webbrowser.open(url)

        self.root.update()

        img = self.resize_ico("Images/Profiles/profile.png", 1, 1)
        image_label = tk.Label(self.root, image=img, bg='black')
        image_label.image = img
        image_label.pack(expand=True, fill="both")

        button_data = [
            ("Images/Profiles/add.png", 0.07, 0.14, lambda: open_url("https://www.netflix.com/in/"), (0.70, 0.38)),
            ("Images/Profiles/Manage.png", 0.25, 0.1, lambda: open_url
             ("https://www.netflix.com/login?nextpage=https%3A%2F%2Fwww.netflix.com%2Fprofiles%2Fmanage"),
             (0.36, 0.7)), ("Images/Profiles/sb1.png", 0.1, 0.21, lambda: self.create_menu(), (0.2, 0.34)),
            ("Images/Profiles/sb2.png", 0.1, 0.21, lambda: self.create_menu(), (0.324, 0.34)),
            ("Images/Profiles/sb3.png", 0.1, 0.21, lambda: self.create_menu(), (0.444, 0.34)),
            ("Images/Profiles/sb4.png", 0.1, 0.21, lambda: self.create_menu(), (0.568, 0.34))]

        for img_path, width_factor, height_factor, command, position in button_data:
            resized_img = self.resize_ico(img_path, width_factor, height_factor)
            button = tk.Button(self.root, image=resized_img, bg='#141414', command=command, bd=0, highlightthickness=0,
                               highlightbackground="#141414", highlightcolor="#141414", activebackground="#141414")
            button.image = resized_img
            button.place(relx=position[0], rely=position[1])

    def create_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        def hide_sidebar(event=None):
            if event and event.widget == self.root:
                sidebar.place_forget()

        def show_sidebar():
            sidebar.place(x=0, y=0, relheight=1)
            sidebar.lift()

        def toggle_sidebar():
            if sidebar.winfo_ismapped():
                hide_sidebar()
            else:
                show_sidebar()

        def on_enter(event):
            hovered_button = event.widget
            button_index = thumbnails_buttons.index(hovered_button)
            bg_image_path = bg_paths[button_index]
            bg_img_loop = self.resize_ico(bg_image_path, 1, 1)
            bg_label.config(image=bg_img_loop)
            bg_label.image = bg_img_loop

        def on_leave(event):
            back_img = self.resize_ico('Images/Thumbnails/bg_img.png', 1, 1)
            bg_label.config(image=back_img)
            bg_label.image = back_img

        def open_video_player(video_path):
            root = tk.Toplevel()
            root.title("Video Player")
            root.attributes('-fullscreen', True)
            root.configure(bg='black')

            current_file = video_path

            instance = vlc.Instance()
            media_player = instance.media_player_new()
            playing_video = False
            video_paused = False

            def play_video():
                nonlocal playing_video
                if not playing_video:
                    media = instance.media_new(current_file)
                    media_player.set_media(media)
                    media_player.set_hwnd(media_canvas.winfo_id())
                    media_player.play()
                    playing_video = True
                    update_time()
                    play_pause_button.config(image=pause_image)

            def play_pause_video(event=None):
                nonlocal video_paused
                if playing_video:
                    if not video_paused:
                        media_player.pause()
                        video_paused = True
                        play_pause_button.config(image=play_image)
                    else:
                        media_player.play()
                        video_paused = False
                        play_pause_button.config(image=pause_image)

            def stop(event=None):
                nonlocal playing_video
                playing_video = False
                media_player.stop()
                root.destroy()

            def update_time():
                if playing_video:
                    current_time = media_player.get_time() // 1000
                    total_duration = media_player.get_length() // 1000

                    current_time_str = str(timedelta(seconds=max(current_time, 0)))
                    total_duration_str = str(
                        timedelta(seconds=max(total_duration, 0))) if total_duration != -1 else "00:00:00"

                    time_label.config(text=f"{current_time_str} / {total_duration_str}")

                    if total_duration > 0:
                        progress_bar.config(to=total_duration)
                        progress_bar.set(max(current_time, 0))

                    root.after(200, update_time)

            def fast_forward(event=None):
                if playing_video:
                    current_time = media_player.get_time()
                    total_duration = media_player.get_length()
                    new_time = min(current_time + 10000, total_duration)
                    media_player.set_time(new_time)
                    progress_bar.set(media_player.get_time() // 1000)

            def rewind(event=None):
                if playing_video:
                    current_time = media_player.get_time() - 10000
                    media_player.set_time(max(current_time, 0))
                    progress_bar.set(media_player.get_time() // 1000)

            def seek_video(event):
                if playing_video:
                    new_time = progress_bar.get() * 1000
                    media_player.set_time(new_time)
                    progress_bar.set(media_player.get_time() // 1000)

            media_canvas = tk.Canvas(root, bg='#141414', highlightthickness=0)
            media_canvas.pack(fill=tk.BOTH, expand=True)

            overlay_frame = tk.Frame(root, highlightthickness=0, bg='#141414')
            overlay_frame.place(relx=0.5, rely=1, anchor=tk.S)

            play_image = ImageTk.PhotoImage(Image.open("Images/Video Player/play.png"))
            pause_image = ImageTk.PhotoImage(Image.open("Images/Video Player/pause.png"))
            exit_image = ImageTk.PhotoImage(Image.open("Images/Video Player/exit.png"))
            nxt_image = ImageTk.PhotoImage(Image.open("Images/Video Player/next.png"))
            prv_image = ImageTk.PhotoImage(Image.open("Images/Video Player/previous.png"))

            progress_bar = tk.Scale(overlay_frame, from_=0, to=100, orient=tk.HORIZONTAL, fg="white", bg="#4a4a4a",
                                    troughcolor="#141414", sliderlength=30, highlightthickness=0, showvalue=0,
                                    length=root.winfo_screenwidth(), sliderrelief='flat', highlightbackground='black',
                                    activebackground='red', borderwidth=0)
            progress_bar.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)
            progress_bar.bind("<ButtonRelease-1>", seek_video)

            rewind_button = tk.Button(overlay_frame, image=prv_image, command=rewind, bd=0, bg='#141414',
                                      activebackground='#141414')
            rewind_button.pack(side=tk.LEFT, padx=10, pady=5)

            play_pause_button = tk.Button(overlay_frame, image=play_image, command=play_pause_video, bd=0, bg='#141414',
                                          activebackground='#141414')
            play_pause_button.pack(side=tk.LEFT, padx=10, pady=5)

            fast_forward_button = tk.Button(overlay_frame, image=nxt_image, command=fast_forward, bd=0, bg='#141414',
                                            activebackground='#141414')
            fast_forward_button.pack(side=tk.LEFT, padx=10, pady=5)

            time_label = tk.Label(overlay_frame, text="00:00:00 / 00:00:00", font=("Arial", 12, "bold"), bg='#141414',
                                  fg='white')
            time_label.place(anchor=tk.CENTER, x=(root.winfo_screenwidth() / 2), rely=0.6)

            stop_button = tk.Button(overlay_frame, image=exit_image, command=stop, bd=0, bg='#141414',
                                    activebackground='#141414')
            stop_button.pack(side=tk.RIGHT, padx=10, pady=5)

            root.bind("<space>", play_pause_video)
            root.bind("<Escape>", stop)
            root.bind("<Left>", rewind)
            root.bind("<Right>", fast_forward)

            play_video()
            update_time()

            root.mainloop()

        image_path = "Images/Thumbnails/bg_img.png"
        image = Image.open(image_path)
        background_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(self.root, image=background_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = background_image

        sidebar = tk.Frame(self.root, bg="black", width=160)

        thumbnails_path = [f"Images/Thumbnails/thum{i}.png" for i in range(1, 10)]
        bg_paths = [f"Images/Thumbnails/bg{i}.png" for i in range(1, 10)]

        canvas = tk.Canvas(self.root, width=self.sc_width, height=self.thumb_height + 10, bg='#181818',
                           highlightthickness=0)
        canvas.place(relx=0.5, rely=0.875, anchor=tk.CENTER)

        thumbnails_buttons = []
        for index, path in enumerate(thumbnails_path):
            resized_image = self.resize_ico(path, 0.2, 0.2)
            b = tk.Button(canvas, image=resized_image, bg='#181818', highlightthickness=0,
                          highlightbackground="#181818", highlightcolor="#181818", activebackground="#181818", border=4,
                          command=lambda p=index: open_video_player(f"Audio/T{p + 1}.mp4"))
            b.image = resized_image
            canvas.create_window((index * (self.thumb_width + 15), 10), window=b, anchor='nw')
            b.bind('<Enter>', on_enter)
            b.bind('<Leave>', on_leave)

            thumbnails_buttons.append(b)

        scrollbar = tk.Scrollbar(self.root, orient='horizontal', command=canvas.xview)
        scrollbar.config(bg='#181818', troughcolor='#181818', activebackground='#181818')
        scrollbar.place(relx=0.5, rely=0.99, anchor=tk.CENTER, width=self.sc_width, height=15)

        canvas.configure(xscrollcommand=scrollbar.set)

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))

        self.root.bind('<Configure>', on_configure)

        image_paths = ["Images/Menu/search.png", "Images/Menu/something more.png", "Images/Menu/home.png",
                       "Images/Menu/trending.png", "Images/Menu/tv shows.png", "Images/Menu/movies.png",
                       "Images/Menu/my list.png", "Images/Menu/wt.png"]

        texts = ["Search", "Play Something", "Home", "News & Popular", "TV Shows", "Movies", "My List", '', "Exit"]

        preloaded_images = [self.resize_ico(path, 0.05, 0.08) for path in image_paths]

        custom_font = ("Arial", 14, "bold")

        for i, (img, text) in enumerate(zip(preloaded_images, texts)):
            frame = tk.Frame(sidebar, bg='black')
            frame.grid(row=i, column=0, padx=10, pady=10, sticky='w')

            if img:
                image_label = tk.Label(frame, image=img, bg='black')
                image_label.image = img
                image_label.pack(side='left')

                text_label = tk.Label(frame, text=text, bg='black', fg='white', font=custom_font)
                text_label.pack(side='left', padx=10)

        exit_img = self.resize_ico('Images/Menu/exit.png', 0.05, 0.08)

        exit_button_frame = tk.Frame(sidebar, bg='black')
        exit_button_frame.grid(row=len(image_paths), column=0, padx=10, pady=(25, 100), sticky='w')

        exit_button = tk.Button(exit_button_frame, image=exit_img, command=self.root.destroy, bg='black', bd=0,
                                highlightthickness=0, activebackground='black')
        exit_button.image = exit_img
        exit_button.grid(row=0, column=0, sticky='w')

        exit_button_text = tk.Label(exit_button_frame, text="Exit", bg='black', fg='white', font=custom_font)
        exit_button_text.grid(row=0, column=1, padx=10, sticky='w')

        menu_image = self.resize_ico("Images/Menu/menu.png", 0.05, 0.08)
        menu_button = tk.Button(self.root, image=menu_image, bg='#181818', activebackground='#181818',
                                command=toggle_sidebar, bd=0, highlightthickness=0, highlightbackground='black',
                                highlightcolor='#181818')
        menu_button.image = menu_image
        menu_button.place(x=int(self.root.winfo_screenwidth() * 0.01), y=int(self.root.winfo_screenheight() * 0.01))

        menu_text_label = tk.Label(self.root, text="Menu Bar", bg="#181818", fg="white", font=custom_font)
        menu_text_label.place(x=int(self.root.winfo_screenwidth() * 0.07), y=int(self.root.winfo_screenheight() * 0.04))

        sidebar.place_forget()

        self.root.bind("<Escape>", lambda event: sidebar.place_forget())
        self.root.bind("<Button-1>", hide_sidebar)


main = tk.Tk()
app = App(main)
main.mainloop()
