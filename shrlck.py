import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from PassCrack import CrackNTLM
from ScanDevice import ScanSAM

#Scan Drives

#Extract Sam

def dumpSAM(System,Sam):
	Creds = subprocess.run(["python","pwdump.py",System,Sam],stdout=subprocess.PIPE,text=True)
	Users = [i[:i.find(":")] for i in Creds.stdout.split()]
	print(Users)
	Targets = [i for i in input("Enter Target: ").split()]
	with open("/tmp/ShrLck_Hashes.txt","w") as File:
		for i in Creds.stdout.split():
			if i[:i.find(":")] in Targets:
				File.write(i+"\n")


def wincrack_button_clicked():
	# Open a new window for password recovery options
	password_recovery_window = tk.Tk()
	password_recovery_window.title("ShrLck - Password Recovery")

	# Label with ShrLck text
	label = tk.Label(password_recovery_window, text="ShrLck", fg="navy", font=("Arial", 24))
	label.pack(padx=10, pady=10)

	# Variable to store radio button selection
	recovery_method = tk.IntVar(password_recovery_window)
	recovery_method.set(0)  # Set a default value for the variable

	# Radio buttons for recovery method
	extract_radio = tk.Radiobutton(password_recovery_window, text="Extract SAM/SYSTEM", variable=recovery_method, value=0)
	extract_radio.pack(anchor=tk.W)

	dump_radio = tk.Radiobutton(password_recovery_window, text="Dump SAM/SYSTEM", variable=recovery_method, value=1)
	dump_radio.pack(anchor=tk.W)

	def extract_selected():
		#Extract Here
		pass

	def CrackWindow(flag):
		password_recovery_window.destroy()
		if flag == 0:
			extract_selected()
		else:
			Sam = filedialog.askopenfilename(title="Select SAM File")
			System = filedialog.askopenfilename(title="Select SYSTEM File")
		Creds = subprocess.run(["python","pwdump.py",System,Sam],stdout=subprocess.PIPE,text=True)
		Users = [i[:i.find(":")] for i in Creds.stdout.split()]
		crack_window = tk.Tk()
		crack_window.title("ShrLck")
		# Label with ShrLck text
		label = tk.Label(crack_window, text="ShrLck", fg="navy", font=("Arial", 24))
		label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

		# User selection dropdown menu
		label1 = tk.Label(crack_window, text="Select User: ")
		label1.grid(row=1,column=0,pady=10)
		selected_user = tk.StringVar()
		user_dropdown = tk.OptionMenu(crack_window, selected_user, *Users)
		user_dropdown.grid(row=1, column=1, padx=10, pady=10)

		def only_numbers(char):
			return char.isdigit()
		validation = crack_window.register(only_numbers)
		l1 = tk.Label(crack_window, text="Choose processing unit: ")
		l1.grid(row=2,column=0,sticky = 'w',padx= 20,pady=15)
		PUvalue = tk.StringVar(crack_window,value='n')
		r1 = tk.Radiobutton(crack_window,text="CPU",padx=14,variable=PUvalue,value='n')
		r1.grid(row=2,column=1,sticky='w')
		r2 = tk.Radiobutton(crack_window,text="GPU",padx=14,variable=PUvalue,value='y')
		r2.grid(row=2,column=2,sticky='w')

		#choose characters
		char_label = tk.Label(crack_window, text = "Choose Type of Characters present: ")
		char_label.grid(row=4,column=0,sticky = 'w', padx= 20, pady=18)

		var1 = tk.StringVar(crack_window,value=0)
		var2 = tk.StringVar(crack_window,value=0)
		var3 = tk.StringVar(crack_window,value=0)
		var4 = tk.StringVar(crack_window,value=0)

		c_UC = tk.Checkbutton(crack_window, text="Upper Case", variable = var1, onvalue="y", offvalue="n")
		c_UC.deselect()
		c_UC.grid(row=4,column=1,sticky = 'w')

		c_LC = tk.Checkbutton(crack_window, text="Lower Case", variable = var2, onvalue="y", offvalue="n")
		c_LC.deselect()
		c_LC.grid(row=4,column=2,sticky = 'w')

		c_num = tk.Checkbutton(crack_window, text="Number", variable = var3, onvalue="y", offvalue="n")
		c_num.deselect()
		c_num.grid(row=4,column=3,sticky = 'w',padx=45)

		c_Sym = tk.Checkbutton(crack_window, text="Symbol", variable = var4, onvalue="y", offvalue="n")
		c_Sym.deselect()
		c_Sym.grid(row=4,column=4,sticky = 'w')

		# min max password
		global box_max, box_min, answer_max, answer_min

		min_label = tk.Label(crack_window, text="Minimum length of password:")
		min_label.grid(row=5, column=0,sticky = 'w', padx= 20, pady=5)

		box_min = tk.Entry(crack_window,validate="key",validatecommand=(validation,"%S"))
		box_min.grid(row=5, column=1, padx=5,sticky = 'w')

		answer_min = tk.Label(crack_window, text='')
		answer_min.grid(row=6, column=1, padx=10)

		max_label = tk.Label(crack_window, text="Maximum length of password:")
		max_label.grid(row=7, column=0, sticky = 'w', padx= 20)

		box_max = tk.Entry(crack_window,validate="key",validatecommand=(validation,"%S"))
		box_max.grid(row=7, column=1, padx=5,pady=20,sticky = 'w')

		answer_max = tk.Label(crack_window, text='')
		answer_max.grid(row=8, column=1, padx=10)

		# Exit and Crack buttons
		exit_button = tk.Button(crack_window, text="Exit", command=crack_window.destroy)
		exit_button.grid(row=9, column=0, pady=10)

		def Main_Event(gpu,User,LC,UC,NUM,SC,Min,Max):
			print(gpu,LC,UC,NUM,SC,Min,Max)
			with open("/tmp/ShrLck_Hashes.txt","w") as File:
				for i in Creds.stdout.split():
					if i[:i.find(":")] in User:
						File.write(i+"\n")

			if gpu == 'y':
				CrackNTLM(LC,UC,NUM,SC,Min,Max,"/tmp/ShrLck_Hashes.txt")

			def execute(x):
				Execute = tk.Toplevel()
				Execute.geometry("200x100")

				result = tk.Label(Execute,text="Password :")
				result.grid(row=2,column=0,padx=30,pady=35)
				output = tk.Text(Execute,height=1,width=45,border=0,bg="#f0f0f0")
				output.grid(row=2,column=1,columnspan=3)
				output.insert(tk.END,x)
				output.config(state="disabled")

			with open("/tmp/ShrLck_Password.txt","r") as passfile:
				tmp = passfile.readline()
				password = tmp[tmp.rfind(":")+1:].strip()
				filename = tmp[tmp.rfind("/"):tmp.rfind(":")+1].strip()
				execute(password)
		crack_button = tk.Button(crack_window, text="Crack", command=lambda: Main_Event(PUvalue.get(),selected_user.get(),var1.get(),var2.get(),var3.get(),var4.get(),box_min.get(),box_max.get()))  # Replace with actual password cracking logic
		crack_button.grid(row=9, column=1, padx=10, pady=10)

		crack_window.mainloop()
	# Exit and Continue buttons
	exit_button = tk.Button(password_recovery_window, text="Exit", command=password_recovery_window.destroy)
	exit_button.pack(side=tk.LEFT, padx=10, pady=10)

	continue_button = tk.Button(password_recovery_window, text="Continue", command=lambda: CrackWindow(recovery_method.get()))
	continue_button.pack(side=tk.RIGHT, padx=10, pady=10)

	password_recovery_window.mainloop()

def recover_files_button_clicked():
    # Your Recover Files button functionality here
    print("Recover Files button clicked!")

def metadata_button_clicked():
    # Your MetaData button functionality here
    print("MetaData button clicked!")

window = tk.Tk()
window.title("ShrLck")

# Create a label with bigger font and navy color
label = tk.Label(window, text="ShrLck", fg="navy", font=("Arial", 24))
label.pack(padx=10, pady=10)

# Create buttons with respective functionality and uniform width
wincrack_button = tk.Button(window, text="WinCrack", command=wincrack_button_clicked, width=13)
wincrack_button.pack(pady=5)

recover_files_button = tk.Button(window, text="Recover Files", command=recover_files_button_clicked, width=13)
recover_files_button.pack(pady=5)

metadata_button = tk.Button(window, text="MetaData", command=metadata_button_clicked, width=13)
metadata_button.pack(pady=5)

# Center the window
window.geometry("300x200+500+200")

window.mainloop()

#scan()
"""
dumpSAM("/home/kali/Downloads/system","/home/kali/Downloads/sam")
CrackNTLM('n','n','y','n','2','10','/tmp/ShrLck_Hashes.txt')
os.system("cat /tmp/Password.txt")
"""
