import customtkinter

# Define button actions
def resume_game():
    #TODO: implement
    print("Game Resumed")

def open_settings():
    #TODO: implement
    print("Settings Opened")

def quit_game():
    #TODO: implement
    print("Game Quit")

# Create main window
root = customtkinter.CTk()
root.geometry("400x300")
root.title("Pause Menu")

# Add title label
title_label = customtkinter.CTkLabel(root, text="PAUSE MENU", font=("Arial", 24))
title_label.pack(pady=20)

# Add buttons
resume_button = customtkinter.CTkButton(root, text="Resume Game", command=resume_game, width=200)
resume_button.pack(pady=10)

settings_button = customtkinter.CTkButton(root, text="Settings", command=open_settings, width=200)
settings_button.pack(pady=10)

quit_button = customtkinter.CTkButton(root, text="Quit Game", command=quit_game, width=200)
quit_button.pack(pady=10)

# Run the app
root.mainloop()
