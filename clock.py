# importing whole module
from tkinter import *
from tkinter.ttk import *
from time import sleep
from datetime import datetime
from threading import Thread
from nebula.hivemind import DataBorg

class Clock:
	def __init__(self):
		# creating tkinter window
		self.root = Tk()
		self.root.title('Clock')
		self.hivemind = DataBorg()

		# This function is used to
		# display time on the label

		# Styling the label widget so that clock
		# will look more attractive
		self.lbl = Label(self.root, font=('calibri', 250, 'bold'),
						 background='black',
						 foreground='white')

		# Placing clock at the centre
		# of the tkinter window
		self.lbl.pack(anchor='center')
		self.window_closed = False

		# bind key events
		self.root.bind("<Key>", self.key_handler)
		self.go_flag = False
		self.end_flag = True

	def on_close(self):
		"""
        Callback function for when the window is closed.
        """
		self.window_closed = True

	def mainloop(self):
		clock_thread = Thread(target=self.make_clock)
		clock_thread.start()
		self.root.mainloop()

	def key_handler(self, event):
		print(event.char, event.keysym, event.keycode)
		if event.char == "y":
			self.go_flag = True
			self.end_flag = False
		elif event.char == "n":
			self.hivemind.MASTER_RUNNING = False

	def make_clock(self):
		"""
		Loop to update the window content at 10 Hz.
		"""
		# while self.hivemind.MASTER_RUNNING:
		if self.end_flag:
			string = "READY FOR NEXT EXPERIMENT? (y/n)"
		else:
			# string = strftime('%H:%M:%S')
			string = datetime.now().strftime('%H:%M:%S.%f')[:-3]

		self.lbl.config(text=string)
		# self.lbl.after(10, self.time)

		self.root.update_idletasks()
		self.root.update()
		if self.window_closed is True:
			self.root.destroy()
			# break
			# sleep(0.1)
