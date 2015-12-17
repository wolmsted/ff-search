### Program that uses reddit API to search for keywords in fantasy football subreddits ###

import sys
import praw
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 525, 650)
		self.setWindowTitle("Fantasy Football Helper")
		self.setWindowIcon(QtGui.QIcon('res/football.png'))
		self.home()

	def home(self):
		lbl = QtGui.QLabel(self)
		lbl.setText("Enter a player's name or keyword: ")
		lbl.move(10, 15)
		lbl.adjustSize()

		self.searchbar = QtGui.QLineEdit(self)
		self.searchbar.resize(self.searchbar.sizeHint())
		self.searchbar.move(lbl.frameGeometry().width() + 15, 10)
		self.searchbar.returnPressed.connect(self.search_player)

		searchbtn = QtGui.QPushButton("Search", self)
		searchbtn.clicked.connect(self.search_player)
		searchbtn.resize(searchbtn.sizeHint())
		searchbtn.move(self.searchbar.frameGeometry().width() + lbl.frameGeometry().width() + 20 , 5)

		refreshbtn = QtGui.QPushButton("Refresh", self)
		refreshbtn.clicked.connect(self.refresh_data)
		refreshbtn.resize(refreshbtn.sizeHint())
		refreshbtn.move(self.searchbar.frameGeometry().width() + lbl.frameGeometry().width() + searchbtn.frameGeometry().width() + 10, 5)

		self.display = QtGui.QTextBrowser(self)
		self.display.setGeometry(0, 50, self.frameGeometry().width(), self.frameGeometry().height() - 50)
		self.display.setOpenExternalLinks(True)
		self.show()

	# checks the new tab in the given subreddit for titles matching the given keyword
	def search_subreddit(self, prawObj, subreddit, text):
		submissions = prawObj.get_subreddit(subreddit).get_new(limit=50)
		submissionList = []
		for title in submissions:
			titleStr = str(title)
			titleStr = titleStr.split(' :: ')[1] # cleans up the title from the given submission
			url = title.permalink
			tupleObj = (titleStr, url)
			submissionList.append(tupleObj)
		submissionList = [elem for elem in submissionList if text.lower() in elem[0].lower()]
		self.display.append("<b>Related titles in r/" + subreddit + " new: </b>")
		for data in submissionList:
			self.display.append("")
			self.display.append("<a href=\"" + data[1] + "\">" + data[0] + "</a>") # hyperlink to the comments
		self.display.append("")

	# function called to search, takes text in searchbar and uses it as keyword
	def search_player(self):
		text = str(self.searchbar.text())
		if (text == ''):
			self.display.setText("<b>No name entered...</b>")
		else:
			self.setWindowTitle("Fantasy Football Helper - " + text)
			prawObj = praw.Reddit(user_agent='ff_application')
			self.display.clear()
			self.search_subreddit(prawObj, 'fantasyfootball', text)
			self.search_subreddit(prawObj, 'nfl', text)			

	def refresh_data(self):
		self.search_player()

def main():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

if __name__ == "__main__":
    main()
