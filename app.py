#!/usr/bin/env python
from flask import Flask
from flask_ask import Ask, statement, question, session
from flask import Flask
import requests
from bs4 import BeautifulSoup

import pandas as pd


app = Flask(__name__)
ask = Ask(app, '/')

def getTable():
    url = "http://www.espn.in/football/table/_/league/eng.1"
    contest_file = requests.get(url)
    soup = BeautifulSoup(contest_file.text, 'html.parser')

    row = soup.find_all("tr", attrs={'class': 'standings-row'})

    table = []

    for i in row:
        team = []
        for j in i:
            team.append(j.text)
            if len(team) == 9:
                table.append(team)

    team_name = []
    games_played = []
    wins = []
    draws = []
    losses =[]
    goals_for = []
    goals_against = []
    goals_difference = []
    points = []

    for i in range(0, 20):
        x = str(i+1)
        team_name.append(table[i][0].strip(x))
        games_played.append(table[i][1])
        wins.append(table[i][2])
        draws.append(table[i][3])
        losses.append(table[i][4])
        goals_for.append(table[i][5])
        goals_against.append(table[i][6])
        goals_difference.append(table[i][7])
        points.append(table[i][8])

    df = pd.DataFrame(columns={"Position", "Team", "Games", "Wins", "Draws", "Losses", "For", "Against", "Goals Difference", "Points"})

    pos = []
    for i in range(1,21):
        pos.append(i)

    df["Position"] = pos
    df["Team"] = team_name
    df["Games"] = games_played
    df["Wins"] = wins
    df["Draws"] = draws
    df["Losses"] = losses
    df["For"] = goals_for
    df["Against"] = goals_against
    df["Goals Difference"] = goals_difference
    df["Points"] = points
    return df

@app.route('/')
def homepage():
    return 'Welcome to Premier League Standings'

@ask.launch
def start_skill():
    message = 'Hey..I can tell you about the latest Premier League Standings..... How many top teams would you like to know about?'
    return question(message)

@ask.intent("NumberIntent",convert = {"number" : int})
def team_intent(number):
	#team = intent['slots']['teamname']
    if number == 0:
        return question('Sorry.. please say a non zero number')
    df =  getTable()
    count = 0
    message = "Here are the current top " + str(min(number,20)) + "teams in Premier League....." #adasd
    for i in range(len(df.index)):
        count = count + 1
        message = message + "Team " + str(i + 1) + ".. " + str(df['Team'][i]) + " with " + str(df['Wins'][i]) + " wins, " + str(df['Losses'][i]) + " losses and " + str(df['Points'][i]) + " points....."
        if count == number:
            break
    return statement(message)


@ask.intent("YesIntent")
def yes_Intent():
    message = 'Say the number of top teams would you like to know about'
    return question(message)

@ask.intent("NoIntent")
def no_Intent():
    message = 'Well that is fine...Maybe next time'
    return statement(message)

@ask.intent("AMAZON.CancelIntent")
def cancel_Intent():
    message = 'See you again...bye'
    return statement(message)

@ask.intent("AMAZON.StopIntent")
def stop_Intent():
    message = 'See you again...bye'
    return statement(message)

@ask.intent("AMAZON.HelpIntent")
def help_Intent():
    message = 'Say the number of top teams would you like to know about'
    return question(message)



if __name__ == '__main__':
    app.run(debug = True)