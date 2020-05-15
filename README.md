# Agenda

This is a command line agenda that I use daily on my computer. It runs using python 3.x. I have NOT tested this on Windows.
I have no plans on making a GUI for it because I spend most of my time in the CLI. Although it is fully functional, I still plan on adding features as I come across them.

To get this to run on your machine, please run setup.py.
Follow the following steps after cloning the repo:

	chmod 700 *.py
	./setup.py
	Edit the 8th line of agenda.py to match your database location.
	        self.conn = sqlite3.connect('/your/database/location/here')
	./agenda.py whenever you would like to run the program.
