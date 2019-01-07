import sqlite3 as sql, tkinter as tk
from tkinter import messagebox


"""
1) gui interface
2) best champ vs enemy
3) best champ for side in roll
4) auto log games with image recognition
https://www.tutorialspoint.com/python/python_gui_programming.htm



"""
class Application(tk.Frame):
	champ_list = ["AATROX", "AHRI", "AKALI", "ALISTAR", "AMUMU", "ANIVIA", "ANNIE", "ASHE",
				"AURELION SOL", "AZIR", "BARD", "BLITZCRANK", "BRAND", "BRAUM", "CAITLYN",
				"CAMILLE", "CASSIOPEIA", "CHO'GATH", "CORKI", "DARIUS", "DIANA", "DR. MUNDO",
				"DRAVEN", "EKKO", "ELISE", "EVELYNN", "EZREAL", "FIDDLESTICKS", "FIORA",
				"FIZZ", "GALIO", "GANGPLANK", "GAREN", "GRAR", "GRAGAS", "GRAVES", "HECARIM",
				"HEIMERDINGER", "ILLAOI", "IRELIA", "IVERN", "JANNA", "JARVAN", "JARVAN IV",
				"JAX", "JAYCE", "JHIN", "JINX", "KAI'SA", "KALISTA", "KARMA", "KARTHUS",
				"KASSADIN", "KATARINA", "KAYLE", "KAYN", "KENNEN", "KHA'ZIX", "KINDRED", "KLED",
				"KOG'MAW", "LEBLANC", "LEE SIN", "LEONA", "LISSANDRA", "LUCIAN", "LULU", "LUX",
				"MALPHITE", "MALZAHAR", "MAOKAI", "MASTER YI", "MISS FORTUNE", "MORDEKAISER",
				"MORGANA", "NAMI", "NASUS", "NAUTILUS", "NIDALEE", "NEEKO", "NOCTURNE", "NUNU", "NUNU & WILLUMP",
				"OLAF", "ORIANNA", "ORNN", "PANTHEON", "POPPY", "PYKE", "QUINN", "RAKAN", "RAMMUS",
				"REK'SAI", "RENEKTON", "RENGAR", "RIVEN", "RUMBLE", "RYZE", "SEJUANI", "SHACO",
				"SHEN", "SHYVANA", "SINGED", "SION", "SIVIR", "SKARNER", "SONA", "SORAKA", "SWAIN",
				"SYNDRA", "TAHM KENCH", "TALIYAH", "TALON", "TARIC", "TEEMO", "THRESH", "TRISTANA",
				"TRUNDLE", "TRYNDAMERE", "TWISTED FATE", "TWITCH", "UDYR", "URGOT", "VARUS",
				"VAYNE", "VEIGAR", "VEL'KOZ", "VI", "VIKTOR", "VLADIMIR", "VOLIBEAR", "WARWOCK",
				"WUKONG", "XAYAH", "XERATH", "XIN ZHAO", "YASUO", "YORICK", "ZAC", "ZED", "ZIGGS",
				"ZILEAN", "ZOE", "ZYRA"]
	def __init__(self, master  = None):
		self.root = tk.Tk()
		self.root.title("League Log")
		self.root.protocol("WM_DELETE_WINDOW", self.on_close)
		master = self.root
		super().__init__(master)
		self.pack()
		self.create_widgets()
		self.database = league_log()
		self.root.config(menu = self.menu_bar)
	def on_close(self):
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			self.database.close()
			self.root.destroy()
	def create_widgets(self):

		# Set up menu bar
		self.menu_bar = tk.Menu(self.root)
		self.file_menu = tk.Menu(self.menu_bar, tearoff = 0)
		self.file_menu.add_command(label = "Clear Fields", command = self.clear_inputs)
		self.file_menu.add_command(label = "Save", command = self.save_database)
		self.database_menu = tk.Menu(self.menu_bar, tearoff = 0)
		self.database_menu.add_command(label = "Reset Log", command = self.reset_database)
		self.menu_bar.add_cascade(label = "File", menu=self.file_menu)
		self.menu_bar.add_cascade(label = "Database", menu=self.database_menu)

		# Set up labels and entry boxes
		self.champ_label = tk.Label(self, text = "Champion").grid(row = 1, column = 0, padx = 5, stick = "w")
		self.champ_entry = tk.Entry(self, width = 35)
		self.champ_entry.grid(row = 1,column = 1, columnspan = 2)

		self.roll_label = tk.Label(self, text = "Roll").grid(row = 2, column = 0, padx = 5, stick = "w")
		self.roll_entry = tk.Entry(self, width = 35)
		self.roll_entry.grid(row = 2,column = 1, columnspan = 2)

		self.enemy_label = tk.Label(self, text = "Enemy").grid(row = 3, column = 0, padx = 5, stick = "w")
		self.enemy_entry = tk.Entry(self, width = 35)
		self.enemy_entry.grid(row = 3,column = 1, columnspan = 2)

		# Set up radio buttons
		self.side_radio = tk.IntVar()
		self.result_radio = tk.IntVar()
		self.no_side = tk.Radiobutton(self, text = "None", value = 0, variable = self.side_radio)
		self.blue_side = tk.Radiobutton(self, text = "Blue", value = 1, variable = self.side_radio)
		self.red_side = tk.Radiobutton(self, text = "Red", value = 2, variable = self.side_radio)
		self.no_side.grid(row = 1, column = 4)
		self.blue_side.grid(row = 2, column = 4)
		self.red_side.grid(row = 3, column = 4)
		self.no_result = tk.Radiobutton(self, text = "None", value = 0, variable = self.result_radio)
		self.win_result = tk.Radiobutton(self, text = "Win", value = 1, variable = self.result_radio)
		self.loss_result = tk.Radiobutton(self, text = "Loss", value = 2, variable = self.result_radio)
		self.no_result.grid(row = 1, column = 5)
		self.win_result.grid(row = 2, column = 5)
		self.loss_result.grid(row = 3, column = 5)

		# Set up buttons
		self.check_button = tk.Button(self, text = "Check Winrate", width = 20, command = self.check_winrate).grid(row = 4, columnspan = 2, column = 0)
		self.show_button = tk.Button(self, text = "Show Matches", width = 20, command = self.show_matches).grid(row = 4, columnspan = 2, column = 2)
		self.log_button = tk.Button(self, text = "Log Games", width = 20, command = self.log_game).grid(row = 4, columnspan = 2, column = 4)

		self.output = tk.Text(self, width = 50)
		self.output.grid(row = 5,column = 0, columnspan = 6)
	def reset_database(self):
		#This needs to have a check to confirm that you really want to do it.
		pass
	def check_winrate(self):
		champ = self.champ_entry.get()
		roll = self.roll_entry.get()
		enemy = self.enemy_entry.get()

		if self.side_radio.get() != 0:
			if self.side_radio.get() == 1:
				side = "Blue"
			else:
				side = "Red"
		else:
			side = "%"
		if champ == "":
			champ = '%'
		if roll == "":
			roll = '%'
		if enemy == "":
			enemy = '%'

		win_rate = self.database.win_rate(champ, roll, enemy, side)
		self.print_to_screen(win_rate)
	def show_matches(self):
		pass
	def log_game(self):
		''' this is a string '''
		try:
			champ = self.get_champ(True)
			roll = self.get_roll(False)
			enemy = self.get_enemy(False)
			result = self.get_result(True)
			side = self.get_side(False)

			if result == 1:
				result_text = "Win"
			else:
				result_text = "Loss"

			output_string = "Game Logged:"
			for item, value in zip(["Champion", "Roll", "Enemy", "Result", "Side"], [champ, roll, enemy, result_text, side]):
				if value != "":
					output_string += "\n\t{}: {}".format(item, value)

			self.database.add(champ, result, enemy, side, roll)
			self.print_to_screen(output_string)
			self.no_result.select()
		except Error:
			pass
	def print_to_screen(self, string, clear = True):
		if clear:
			self.output.delete(1.0, tk.END)
		self.output.insert(1.0, string)
	def get_champ(self, required ):
		"""
		retrieves the champion from the champ_entry box,
		raises error if empty and required or if champ is not recognized
		"""
		champ_data = self.champ_entry.get()
		if champ_data == "":
			if required :
				self.print_to_screen("No Champion entered")
				raise(Error())
		else:
			if champ_data.upper() not in self.champ_list:
				self.print_to_screen("Champion not recognized")
				raise(Error())
		return champ_data
	def get_roll(self, required):
		"""
		Retrieves data from the roll_entry box,
		raises error if roll is not recognized
		"""
		roll_data = self.roll_entry.get()
		if roll_data != "":
			if roll_data.upper() not in ["TOP", "JUNGLE", "SUPPORT", "MID", "MARKSMAN"]:
				self.print_to_screen("Roll not recognized")
				raise(Error())
		elif required:
			self.print_to_screen("No roll entered")
			raise(Error())
		return roll_data
	def get_enemy(self, required):
		"""
		retrieves the enemy champion from the enemy_entry box,
		raises error if empty and required or if champ is not recognized
		"""
		enemy_data = self.enemy_entry.get()
		if enemy_data == "":
			if required:
				self.print_to_screen("No enemy champion entered")
				raise(Error())
		else:
			if enemy_data.upper() not in self.champ_list:
				self.print_to_screen("Enemy Champion not recognized")
				raise(Error())
		return enemy_data
	def get_result(self, required):
		"""
		Retrieves the entry for the results radio buttons.
		If the "none" is selected but an answer is required
		an error is raised. Otherwise returns either 1 for a win
		or 0 for a loss.
		"""
		print(self.result_radio.get())
		if self.result_radio.get() != 0:
			if self.result_radio.get() == 2:
				return 0
			else:
				return 1
		elif required:
			self.print_to_screen("No result given")
			raise(Error())
	def get_side(self, required):
		if self.side_radio.get() != 0:
			if self.side_radio.get() == 1:
				return "Blue"
			else:
				return "Red"
		elif required:
			self.print_to_screen("No side selected")
			raise(Error())
	def clear_inputs(self):
		self.champ_entry.delete(0,'end')
		self.roll_entry.delete(0,'end')
		self.enemy_entry.delete(0,'end')
		self.no_side.select()
		self.no_result.select()
	def save_database(self):
		self.database.save()

class league_log():
	def __init__(self):		#""" connects to the league_log database, sets-up a database cursor and runs the setup method """
		self.conn = sql.connect("league_log")
		self.cursor = self.conn.cursor()
		self.setup()
	def setup(self):		#""" Creates the champions table if it does not exist with columns titled: games as primary key, champ as text, result as integer, enemy as text, side as text and roll as text """
		self.cursor.execute("CREATE TABLE IF NOT EXISTS champions (game integer PRIMARY KEY, champ text, result integer, enemy text, side text, roll text)")
	def add(self, champ, result, enemy = None, side = None, roll = None):		#""" Enters given item into the database. Champ and results are required. Everything else isn't """
		if not enemy:
			enemy = ""
		if not side:
			side = ""
		if not roll:
			roll = ""
		self.cursor.execute("INSERT INTO champions (champ, result, enemy, side, roll) VALUES (?,?, ?, ?, ?)", (champ, result, enemy, side, roll))
	def retrieve(self, champ = None):		#""" Retrieves a list of games for the given champion. if none is given returns all games """
		if not champ:
			output = self.cursor.execute("SELECT * FROM champions")
		else:
			champ = champ.upper()
			output = self.cursor.execute("SELECT champ, result FROM champions WHERE UPPER(champ) = ?", (champ,))
		for i in output:
			print(i)
	def win_rate(self, champ, roll, enemy, side):
		output = self.cursor.execute("""SELECT champ, ROUND(SUM(CAST(result AS float))/COUNT(result),3) AS test, COUNT(result)
                                                FROM champions
                                                WHERE UPPER(champ) LIKE ? AND UPPER(roll) LIKE ? AND UPPER(enemy) LIKE ? AND UPPER(side) LIKE ?
                                                GROUP BY champ
                                                ORDER BY test DESC""", (champ, roll, enemy, side))
		output_list = output.fetchall()
		if output_list != []:
			return_string =  "Champion\t\tWin Rate\t\tNumber of Games\n------------------------------------------------\n"
			for i in output_list:
				winRate = str(i[1] *100)
				if len(winRate) > 5:
					winRate = winRate[0:5]
				return_string += "{}\t\t{}\t\t{}\n".format(i[0], winRate, i[2])
			return return_string
		else:
			return "No Games with those criteria have been played"
	def close(self):
		self.conn.commit()
		self.conn.close()
	def update(self, ind, enemy, side):
		self.cursor.execute("""UPDATE champions SET enemy = ?, side = ? WHERE ?""", (enemy, side, ind))
	def sql_select(self, mode, columns, data):
		if mode == 1:
			pull = "result"
		elif mode == 2:
			pull = "*"
		if len(data) == 1:
			output = self.cursor.execute("SELECT {} FROM champions WHERE UPPER({}) = ?".format(pull, columns[0]), (data[0],))
		elif len(data) == 2:
			output = self.cursor.execute("SELECT {} FROM champions WHERE UPPER({}) = ? AND UPPER({}) = ?".format(pull, columns[0], columns[1]), (data[0], data[1]))
		elif len(data) == 3:
			output = self.cursor.execute("SELECT {} FROM champions WHERE UPPER({}) = ? AND UPPER({}) = ? AND UPPER({}) = ?".format(pull, columns[0], columns[1], columns[2]), (data[0], data[1], data[2]))
		elif len(data) == 4:
			output = self.cursor.execute("SELECT {} FROM champions WHERE UPPER({}) = ? AND UPPER({}) = ? AND UPPER({}) = ? AND UPPER({}) = ?".format(pull, columns[0], columns[1], columns[2], columns[3]), (data[0], data[1], data[2], data[3]))
		else:
			output = self.cursor.execute("SELECT {} FROM champions".format(pull))
		return output
	def save(self):
		self.conn.commit()

class Error(Exception):
	pass


# b = league_log()
# c = b.cursor
# a(c.execute("""SELECT champ, ROUND(SUM(CAST(result AS float))/COUNT(result),3) AS test, COUNT(result)
# FROM champions
# WHERE UPPER(champ) LIKE 'ZILEAN' AND UPPER(roll) LIKE '%' AND UPPER(enemy) LIKE '%' AND UPPER(side) LIKE '%'
# GROUP BY champ
# ORDER BY test DESC"""))
# c.execute("DROP TABLE champions")
app = Application()
app.mainloop()
