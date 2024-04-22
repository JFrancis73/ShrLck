import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess
from prettytable import PrettyTable
import opencage.geocoder

def MetaData():
    def choose_file_type():
        global file_type
        file_type = file_type_var.get()
        file_type_window.destroy()
        root.deiconify()

    def get_file_path():
        file_path = filedialog.askopenfilename()
        if file_path:
            entry_path.delete(0, tk.END)
            entry_path.insert(0, file_path)

    def store_file_path():
        global selected_file_path
        selected_file_path = entry_path.get()
        metadata = get_file_metadata(selected_file_path)
        if metadata:
            print_metadata_table(metadata)
        else:
            print("Please select a file.")

    def get_file_metadata(file_path):
        try:
            metadata_output = subprocess.check_output(["exiftool", file_path]).decode("utf-8")
            metadata_lines = metadata_output.strip().split('\n')
            metadata_dict = {}
            for line in metadata_lines:
                key, value = line.split(':', 1)
                metadata_dict[key.strip()] = value.strip()

            if 'GPS Latitude' in metadata_dict and 'GPS Longitude' in metadata_dict:
                latitude = metadata_dict['GPS Latitude']
                longitude = metadata_dict['GPS Longitude']
                lat_degrees, lat_minutes, lat_seconds = map(float, latitude.split())
                lon_degrees, lon_minutes, lon_seconds = map(float, longitude.split())
                lat_decimal = lat_degrees + (lat_minutes / 60) + (lat_seconds / 3600)
                lon_decimal = lon_degrees + (lon_minutes / 60) + (lon_seconds / 3600)
                geocoder = opencage.geocoder.OpenCageGeocode('YOUR_OPENCAGE_API_KEY')

                result = geocoder.reverse_geocode(lat_decimal, lon_decimal)

                if result and len(result):
                    metadata_dict['Location'] = result[0]['formatted']
                else:
                    metadata_dict['Location'] = 'Location not found'

            return metadata_dict
        except Exception as e:
            print("Error:", e)
            return None

    def print_metadata_table(metadata):
        table = PrettyTable(['Property', 'Value'])
        for key, value in metadata.items():
            table.add_row([key, value])
        print(table)

        if 'Location' in metadata:
            label_location.config(text="Location:", font=('Arial', 10, 'bold'))
            entry_location.delete(0, tk.END)
            entry_location.insert(0, metadata['Location'])
            label_location.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
            entry_location.grid(row=3, column=1, padx=5, pady=5, columnspan=2, sticky=tk.W)

    file_type_window = tk.Tk()
    file_type_window.title("Choose File Type")
    file_type_var = tk.StringVar()
    file_type_label = ttk.Label(file_type_window, text="Choose file type to extract metadata from:")
    file_type_label.pack(padx=10, pady=10)
    file_type_combobox = ttk.Combobox(file_type_window, textvariable=file_type_var, values=["Image", "Other"])
    file_type_combobox.pack(padx=10, pady=5)
    file_type_button = ttk.Button(file_type_window, text="Choose", command=choose_file_type)
    file_type_button.pack(padx=10, pady=5)

    file_type = None

    root = tk.Tk()
    root.title("File Metadata Extractor")

    label_path = tk.Label(root, text="File Path:")
    label_path.grid(row=0, column=0, padx=5, pady=5)
    entry_path = tk.Entry(root, width=40)
    entry_path.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
    button_browse = tk.Button(root, text="Browse", command=get_file_path)
    button_browse.grid(row=0, column=3, padx=5, pady=5)
    button_submit = tk.Button(root, text="Extract Metadata", command=store_file_path)
    button_submit.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

    label_location = tk.Label(root, text="", font=('Arial', 10, 'bold'))
    entry_location = tk.Entry(root, width=40)

    button_close = tk.Button(root, text="Close", command=root.quit)
    button_close.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
    selected_file_path = None
    root.withdraw()

    file_type_window.mainloop()
MetaData()
