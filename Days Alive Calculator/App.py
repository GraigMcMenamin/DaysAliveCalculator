from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

def calculate_days_alive(birthdate):
    #Main function, take birthdate as an argument and returns days alive, or nothing with a error variable as True.

    def getdate():
        #This function imports today's date and sets separate global varibles for the year, month, and day.
        from datetime import date
        today = str(date.today())
        global thisyear, thismonth, thisday
        thisyear = int(today[0:4])
        thismonth = int(today[5:7])
        thisday = int(today[8:])

    getdate()



    def monthdays(x):
        #This function is passed a month in the form of a number (ex 07 for july) and returns how many days are in that month.
        #If it is a leap year and the function is passed feburary, that is accounted for later.
        if (x==1) or (x==3) or (x==5) or (x==7) or (x==8) or (x==10) or (x==12):
            return int(31)
        elif (x==4) or (x==6) or (x==9) or (x==11):
            return int(30)
        elif (x==2):
            return int(28)

    def getbirthdate(birthdate):
        #This function checks that the date entered is valid.

        global error   #This variable will become true if the users date entered is invalid.
        error = False

        if len(birthdate) == 10:   #Checks that the date string is the correct length.

            if (birthdate[6:11].isnumeric() == True) and (birthdate[0:2].isnumeric() == True) and (birthdate[3:5].isnumeric() == True):   #Checks that numbers in date are numeric and not letters.

                if birthdate[2] == "/" and birthdate[5] == "/":   #Checks slashes in date are placed correctly.

                    #Set separate global variables for users birthyear, month, and day.
                    global birthyear, birthmonth, birthday
                    birthyear = int(birthdate[6:11])
                    birthmonth = int(birthdate[0:2])
                    birthday = int(birthdate[3:5])

                    #Checks that year, month, and day entered are valid and not in the future.
                    if birthyear <= thisyear:
                        if birthmonth <= 12:
                            if birthday <= monthdays(birthmonth):
                                return
        
        error = True   #If the function does not end at the above return, the date did not pass all validity checks.
        return
    

    getbirthdate(birthdate)


    if error == True:
        return
        


    def calcage():
        #This function returns the users age. It also sets a boolean variable, bdaypassed, according to whether or not the users birthday has passed this year.
        global bdaypassed
        if birthmonth < thismonth:   #Checks if birth month passed.
            bdaypassed = True
            return thisyear - birthyear
        elif birthmonth == thismonth:   #Checks if this month is the birthmonth, and if so, checks if birthday passed.
            if birthday <= thisday:
                bdaypassed = True
                return thisyear - birthyear
        else:
            bdaypassed = False   #Sets variable to false if user hasn't had a birthday this year.
            return (thisyear - birthyear) - 1   # -1 is added to this line because their birthday has not passed this year.

    age = calcage()



    def dayssincebirth():
        #This function calculates how long the user has been alive for. It sets varibles for how many days, hours, minutes, seconds, and leap years the users has been alive for.

        global days, extradays
        days = age*365   #Adds 365 days for each year in age

        #Adds one day for each leap year.
        i = birthyear
        leapyear = int(1900)
        extradays = int(0)
        while i <= 2020:   #Loops through all the years user has been alive.
            while leapyear <= 2020:   #Loops through all leap years since 1900.
                if i == leapyear:
                    extradays += 1
                leapyear += 4
            leapyear = int(1900)
            i += 1
        days += extradays

        #Each of the following three conditions calculate how many days have past since users last birthday.

        #For condition that user's birthday has past and it is not their birthmonth.
        if (bdaypassed == True) and (birthmonth != thismonth):
            #Calculates how many days have passed in the user's birth month after their birthday. (ex. if born on July 20th, calculates 11 days)
            days_in_bmonth_after_bday = monthdays(birthmonth) - birthday
            days += days_in_bmonth_after_bday
            imonth = birthmonth + 1   #imonth is used to increment months.
            while (imonth) != thismonth:   #Increments from birthmonth to current month.
                days += monthdays(imonth)   #Adds amount of days in each month incremented.
                imonth += 1
            days += thisday   #Adds how manys days have past since in the current month. (Ex. if it's november 11th adds 11.)

        #For the condition that user's birthday has past and it is still their birthmonth.
        elif (bdaypassed == True) and (birthmonth == thismonth):
            #For this condition we only have to add how many days have passed in the birthmonth since user's birthday.
            days_since_bday = thisday - birthday
            if days_since_bday == 0:
                print('Happy Birthday!')
            days += days_since_bday


        #For the condition that the user's birthday has not yet passed this year.
        elif (bdaypassed == False):
            #Calculates how many days have passed in the user's birth month after their birthday. (ex. if born on July 20th, calculates 11 days)
            days_in_bmonth_after_bday = monthdays(birthmonth) - birthday
            days += days_in_bmonth_after_bday
            imonth = birthmonth + 1   #imonth is used to increment months.
            while (imonth) != 13:   #Increments through months from the month after birth month last year, to december last year.
                days += monthdays(imonth)   #Adds amount of days in each month incremented.
                imonth += 1
            imonth = 1
            while (imonth) != thismonth:   #Increments through months from janurary this year to current month.
                days += monthdays(imonth)   #Adds amount of days in each month incremented.
                imonth += 1
            days += thisday   #Adds how manys days have past since in the current month. (Ex. if it's november 11th adds 11.)

        else:
            error == True
            print("Unexpected error")   #One of these will conditions have to be true unless an invalid date was entered and not caught at the start.

    dayssincebirth()
    if error == True:
        return
    return days



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        birthdate = request.form['birthday']   #Get user input from html page
        days = calculate_days_alive(birthdate)   #Run main function
        if error != True:
            #Use days alive to calculate hours, minutes, and seconds alive. this is only done if there's no errors with the entered date.
            hours = days*24
            return render_template('results.html', days=days, hours=hours)
        else:
            return render_template('error.html')
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
