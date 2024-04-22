import tkinter as tk
import os
import subprocess
from ScanDevice import FindDevices
# Dummy list for drives (replace with actual drive retrieval logic)
drives = FindDevices().keys()

def File_Recovery():
    def handle_image_checkbox(var):
        # Implement logic here based on the variable state (True/False)
        # For example, enable/disable additional widgets related to drive imaging
        if var.get():
            print("Drive Imaging selected")
        else:
            print("Drive Imaging deselected")


    def get_selected_info():
        # This function collects the selected information from the window
        drive = drive_var.get()
        drive = "/dev/sdc"
        file_types = " -t "
        if var1.get():
            file_types += "png,jpg,gif,"
        if var2.get():
            file_types += "doc,pdf,"
        if var3.get():
            file_types += "mp4,avi,"
        file_types = file_types[:-1]
        create_image = image_var.get()
        print(f"Selected Drive: {drive}")
        print(f"Selected File Types: {', '.join(file_types)}")
        print(f"Create Drive Image: {create_image}")
        os.system("foremost -q -i "+drive+file_types+" -T -v")


    def close_window():
        window.destroy()

    # Create the main window
    window = tk.Tk()
    window.title("File Recovery App")

    # Create a frame to group elements (improves organization)
    main_frame = tk.Frame(window)
    main_frame.pack(padx=10, pady=10)

    # Frame for drive selection (label and dropdown side-by-side)
    drive_frame = tk.Frame(main_frame)
    drive_frame.pack()

    # Drive Selection Label
    drive_label = tk.Label(drive_frame, text="Select Drive:")
    drive_label.pack(side="left")

    # Drive Selection Dropdown
    drive_var = tk.StringVar(window)
    drive_menu = tk.OptionMenu(drive_frame, drive_var, *drives)
    drive_menu.pack(side="left", padx=5)  # Add padding between label and dropdown

    # "Create Drive Image" Checkbox with padding
    image_var = tk.IntVar()
    image_checkbox = tk.Checkbutton(
        main_frame, text="Create Drive Image (Before Recovery)", variable=image_var, command=lambda: handle_image_checkbox(image_var)
    )
    image_checkbox.pack(pady=5)  # Add padding above and below the checkbox

    # File Type Selection Label with larger font size and padding
    file_type_label = tk.Label(main_frame, text="Select File Types:", font=("Arial", 12, "bold"))
    file_type_label.pack(pady=5)  # Add padding above and below the label

    # Checkboxes for file types with left alignment
    var1 = tk.IntVar()
    var2 = tk.IntVar()
    var3 = tk.IntVar()

    file_type_checkbox1 = tk.Checkbutton(main_frame, text="Images (.jpg, .png)", variable=var1, anchor="w")
    file_type_checkbox1.pack(anchor="w", pady=5)  # Add padding below the checkbox

    file_type_checkbox2 = tk.Checkbutton(main_frame, text="Documents (.docx, .pdf)", variable=var2, anchor="w")
    file_type_checkbox2.pack(anchor="w", pady=5)  # Add padding below the checkbox

    file_type_checkbox3 = tk.Checkbutton(main_frame, text="Videos (.mp4, .avi)", variable=var3, anchor="w")
    file_type_checkbox3.pack(anchor="w", pady=5)  # Add padding below the checkbox

    # Buttons in a frame side-by-side (using pack with side="left")
    button_frame = tk.Frame(main_frame)
    button_frame.pack()

    recover_button = tk.Button(button_frame, text="Recover Files", command=get_selected_info)
    recover_button.pack(side="left", padx=5, pady=5)  # Add padding

    close_button = tk.Button(button_frame, text="Close", command=close_window)
    close_button.pack(side="left", padx=5, pady=5)  # Add padding

    # Keep the window running
    window.mainloop()

print(FindDevices())
syscmd = subprocess.run(["sudo","lsblk","-o","NAME,LABEL"],stdout=subprocess.PIPE,text=True)
#print(syscmd.stdout)
File_Recovery()
