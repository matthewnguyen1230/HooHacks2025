import customtkinter
import os
from PIL import Image
from numpy.ma.core import resize


# Main Application Class
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        # Configure grid to allow dynamic resizing
        self.grid_rowconfigure(0, weight=1)  # Make row 0 expandable
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expandable

        # Creates two frames: Title Screen and Pause Menu
        self.title_screen = customtkinter.CTkFrame(self)
        self.pause_menu = customtkinter.CTkFrame(self)

        # Place both frames in the same grid location
        for frame in (self.title_screen, self.pause_menu):
            frame.grid(row=0, column=0, sticky="nsew")

        # Build each frame
        self.build_title_screen()
        self.build_pause_menu()

        # Show the title screen initially
        self.show_frame(self.title_screen)

    def build_title_screen(self):
        """Builds the title screen UI."""
        # Add background
        current_dir = os.path.dirname(__file__)
        size = (self.winfo_screenwidth(), self.winfo_screenheight())
        bg_image_path = os.path.join(current_dir, "../assets/images/background.png")
        bg_image = customtkinter.CTkImage(light_image=Image.open(bg_image_path), size=size)


        bg_label = customtkinter.CTkLabel(self, image=bg_image, text="")
        bg_label.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        # Add title
        label = customtkinter.CTkLabel(self.title_screen, text="TITLE SCREEN", font=("Arial", 24))
        label.pack(pady=20)

        start_button = customtkinter.CTkButton(
            self.title_screen, text="Start Game", command=lambda: self.show_frame(self.pause_menu)
        )
        start_button.pack(pady=10)

    def build_pause_menu(self):
        """Builds the pause menu UI."""
        label = customtkinter.CTkLabel(self.pause_menu, text="PAUSE MENU", font=("Arial", 24))
        label.pack(pady=20)

        resume_button = customtkinter.CTkButton(
            self.pause_menu, text="Resume Game", command=lambda: print("Game Resumed")
        )
        resume_button.pack(pady=10)

        settings_button = customtkinter.CTkButton(
            self.pause_menu, text="Settings", command=lambda: print("Settings Opened")
        )
        settings_button.pack(pady=10)

        quit_button = customtkinter.CTkButton(
            self.pause_menu, text="Quit Game", command=lambda: self.show_frame(self.title_screen)
        )
        quit_button.pack(pady=10)

    def show_frame(self, frame):
        """Raises the specified frame."""
        frame.tkraise()


# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
