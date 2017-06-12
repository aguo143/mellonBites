from tkinter import *
from datetime import datetime
import math, calendar, random, os, string, copy

### Generic Functions ###

# Initializing variables
def init(data):
    data.mode = data.latestMode = "home"
    data.homeCoords = []
    
    initLogin(data)
    initNewUser(data)
    initNewUserModel(data)
    initMain(data)
    initLogFood(data)
    initScore(data)
    initVisualize(data)

# Controls mousePress events and distributes to sub functions
def mousePressed(event, data):
    if data.mode == "home":
        homeMousePressed(event,data)
    elif data.mode == "newUser":
        newUserMousePressed(event,data)
    elif data.mode == "calculate":
        calculateMousePressed(event,data)
    elif data.mode == "main":
        mainMousePressed(event,data)
    elif data.mode == "Log Food":
        logFoodMousePressed(event,data)
    elif data.mode == "login":
        loginMousePressed(event,data)
    elif data.mode == "score":
        scoreMousePressed(event,data)
    elif data.mode == "Recommend" or data.mode == "Grocery List":
        pageUCMousePressed(event,data)
    elif data.mode == "Visualize":
        visualizeMousePressed(event,data)

# KeyPress function (no function)
def keyPressed(event, data):
    if data.mode == "newUser":
        newUserKeyPressed(event,data)
    elif data.mode == "main":
        mainKeyPressed(event,data)
    elif data.mode == "login":
        loginKeyPressed(event,data)

# Retrieves the current hour, min, and weekday
# EDIT STYLE
def timerFired(data):
    pass

# All text color names found at goo.gl/JBBZ3g and rgb values at goo.gl/x8CvEQ
# Redraws all of the functions for each mode
def redrawAll(canvas, data):
    if data.mode == "home":
        homeRedrawAll(canvas,data)
    elif data.mode == "newUser":
        newUserRedrawAll(canvas,data)
    elif data.mode == "calculate":
        calculateRedrawAll(canvas,data)
    elif data.mode == "main":
        mainRedrawAll(canvas,data)
    elif data.mode == "Log Food":
        logFoodRedrawAll(canvas,data)
    elif data.mode == "login":
        loginRedrawAll(canvas,data)
    elif data.mode == "score":
        scoreRedrawAll(canvas,data)
    elif data.mode == "Recommend" or data.mode == "Grocery List":
        pageUCRedrawAll(canvas,data)
    elif data.mode == "Visualize":
        visualizeRedrawAll(canvas,data)

### Generic Helpers ###

# Determines if a mouseclick is in bounds or not
def inBounds(x0,x1,y0,y1,targetX,targetY):
    return ((targetX <= x1) and (targetX >= x0) and
            (targetY <= y1) and (targetY >= y0))

# RGB function directly from goo.gl/lO6A8w
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

### Home ###

# Redraws all the box buttons on the menu page
def homeRedrawAll(canvas,data):
    horizStretch, vertStretch = 0.5, 0.3
    canvas.create_text(data.width*horizStretch, data.height*vertStretch,
        text="mellonBites", font="Arial 80 bold")

    homeGetCoords(data)

    for (x0,x1,y0,y1,textX,textY,color,text) in data.homeCoords:
        canvas.create_rectangle(x0,y0,x1,y1,fill=color,width=0)
        canvas.create_text(textX,textY,text=text,
            font="Arial 20",fill="black")

# Gets the coordinates for the boxes in the home screen
def homeGetCoords(data):
    x0, x1, textX = 300, 500, 400
    y0, y1, padding = 225, 275, 80
    colors = ["DodgerBlue2", "aquamarine"]
    text = ["New User","Login"]

    for i in range(len(colors)):
        y0 += padding
        y1 += padding
        textY = ((y1-y0)/2) + y0
        data.homeCoords.append([x0,x1,y0,y1,textX,textY,colors[i],text[i]])

# Controls the mouse function for the home screen
def homeMousePressed(event,data):
    for (x0,x1,y0,y1,textX,textY,color,text) in data.homeCoords:
        if inBounds(x0,x1,y0,y1,event.x,event.y):
            if text == "New User":
                data.mode = "newUser"
            elif text == "Login":
                data.mode = "login"

### New User ###

# Initializes new values for new input
def initNewUser(data):
    data.userProfile = {"gender":"","actLev":"","calDef":""}
    data.userProfCoords = {"user":[],
        "password":[],"gender":[],"weight":[],
        "height":[],"age":[],"actLev":[],"calDef":[]}
    data.messages = {"user":"","password":"","weight":"",
                    "height":"","age":""}
    data.doneCoords, data.doneText = (600,560,750,580), (675,570)
    data.backCoords, data.backText = (50,560,200,580), (125,570)
    data.newUserTypeCoords = None
    data.typing = False
    data.macros = [90, 90, 90]
    data.bpColors = {"gender":[False, False],
                     "actLev":[False, False, False, False, False],
                     "calDef":[False, False, False]}
    data.tryAgain = False
    data.saturatedFat = data.cholesterol = data.sodium = data.dietaryFiber = 0

# Continues storing the input from the new user
def initNewUserModel(data):
    data.newUserQsCoords = getNewUserQsCoords(data.width,data.height)
    data.textBoxCoords = getTextBoxCoords(data.newUserQsCoords)
    data.genderCoords = getGenderCoords(data,data.newUserQsCoords)
    for (x0,y0,x1,y1,code) in data.textBoxCoords:
        data.userProfCoords[code] = [x0,y0,x1,y1]

    data.userProfCoords["gender"].extend([data.genderCoords[0][:-1],
                                    data.genderCoords[1][:-1]])

    data.actLevelsCoords = getActLevelsCoords(data,data.newUserQsCoords)
    actLevels = []
    for i in range(len(data.actLevelsCoords)):
        actLevels += [data.actLevelsCoords[i][:-1]]
    data.userProfCoords["actLev"].extend(actLevels)

    data.calDefCoords = getCalDefCoords(data,data.newUserQsCoords)
    calDefs = []
    for i in range(len(data.calDefCoords)):
        calDefs += [data.calDefCoords[i][:-1]]
    data.userProfCoords["calDef"].extend(calDefs)

# Controls the function for clicking and typing, as well as
# selecting in the new User mode
def newUserMousePressed(event,data):
    dX0, dY0, dX1, dY1 = data.doneCoords
    bX0, bY0, bX1, bY1 = data.backCoords
    if inBounds(dX0,dX1,dY0,dY1,event.x,event.y):
        data.mode = "calculate"
        stripUserInfo(data)
    elif inBounds(bX0,bX1,bY0,bY1,event.x,event.y):
        data.mode = "home"
        init(data)
    newUserAnswersMousePressed(event,data)

# Detects whether a box has been selected so text can be
# inserted or a box selected out of multiple choices
def newUserAnswersMousePressed(event,data):
    codes = ["user","password","gender","weight",
        "height","age","actLev","calDef"]
    for code in codes:
        coords = data.userProfCoords[code]
        if not isinstance(coords[0],list):
            x0, y0, x1, y1 = coords
            if inBounds(x0,x1,y0,y1,event.x,event.y):
                data.tryAgain = False
                data.typing = True
                data.newUserTypeCoords = [x0,y0,x1,y1]
        else:
            for i in range(len(coords)):
                x0, y0, x1, y1, category = coords[i]
                if inBounds(x0,x1,y0,y1,event.x,event.y):
                    data.tryAgain = False
                    data.userProfile[code] = category
                    data.bpColors[code][i] = not data.bpColors[code][i]
                else:
                    data.bpColors[code][i] = False

# Collects this data and calls the calculation function - 
# if it doesn't work, sets tryAgain to true to get more input
def stripUserInfo(data):
    try:
        user = data.messages['user']
        password = data.messages['password']
        gender = data.userProfile['gender']
        weight = float(data.messages['weight'])
        height = float(data.messages['height'])
        age = float(data.messages['age'])
        actLev = data.userProfile['actLev']
        calDef = data.userProfile['calDef']
        calculate(data,user,password,gender,weight,height,age,actLev,calDef)
    except:
        data.tryAgain = True
        data.mode = 'newUser' 

# Controls key presses (typing in boxes) for new user mode
def newUserKeyPressed(event,data):
    currCode = None
    if data.typing == True:
        for code in data.userProfCoords:
            if data.userProfCoords[code] == data.newUserTypeCoords:
                currCode = code
        if currCode != None:
            key = event.keysym
            if key == 'BackSpace':
                if data.messages[currCode] != '':
                    data.messages[currCode] = data.messages[currCode][:-1]
            if (key in string.ascii_letters) or (key in string.digits):
                key = key.lower()
                data.messages[currCode] += key

# Redraws all the items for the newUser screen, with 
# buttons to go to different modes also
def newUserRedrawAll(canvas,data):
    horizStretch, vertStretch = 0.4, 0.1
    canvas.create_text(data.width*horizStretch, data.height*vertStretch,
        text="building your body profile...", font="Arial 45 bold")
    horizStretch, vertStretch = 0.28, 0.18
    canvas.create_text(data.width*horizStretch, data.height*vertStretch,
        text="(Click in the gray boxes to type, and select colored boxes)",
        fill="DodgerBlue2")

    newUserAnswersRedrawAll(canvas,data)

    canvas.create_rectangle(data.doneCoords, fill="black")
    canvas.create_text(data.doneText,fill="white",
        text="Calculate!",font="Arial 12")
    canvas.create_rectangle(data.backCoords, fill="black")
    canvas.create_text(data.backText,fill="white",text="Back",font="Arial 12")

    for key in data.messages:
        x0, y0, x1, y1 = data.userProfCoords[key]
        textX, textY = x0 + (x1-x0)/2, y0 + (y1-y0)/2
        canvas.create_text(textX, textY, text=data.messages[key])

# Redraws all the items for the newUser screen, with different
# colors for when the boxes are selected
def newUserAnswersRedrawAll(canvas,data):
    for (textX, textY, text) in data.newUserQsCoords:
        canvas.create_text(textX, textY, text=text, font="Arial 15")
    for (x0,y0,x1,y1,code) in data.textBoxCoords:
        canvas.create_rectangle(x0,y0,x1,y1,fill="grey",width=0)

    text = """Error: Weight, Height, and Age must be numbers.\n
    Make sure you have completed all selections."""
    ratio = 0.95
    if data.tryAgain == True:
        canvas.create_text(data.width/2, data.height*ratio,
            text=text, font="Arial 12", fill="fireBrick")
    
    newUserGenderRedrawAll(canvas,data)
    newUserActLevelRedrawAll(canvas,data)
    newUserCalDefRedrawAll(canvas,data)

# Redraws the gender buttons
def newUserGenderRedrawAll(canvas,data):
    c0 = ("pink" if (data.bpColors["gender"][0] == False) 
            else rgbString(255,128,175))
    c1 = ("dodgerBlue2" if (data.bpColors["gender"][1] == False) 
            else rgbString(0,102,230))
    colors = [c0,c1]
    for i, (x0,y0,x1,y1,gender,color) in enumerate(data.genderCoords):
        canvas.create_rectangle(x0,y0,x1,y1,fill=colors[i],width=0)
        canvas.create_text((x1-x0)/2+x0,(y1-y0)/2+y0,text=gender)

# Redraws the actLevel buttons
def newUserActLevelRedrawAll(canvas,data):
    upColors = ["salmon","orange",rgbString(255,255,102),
                "aquamarine",rgbString(60,210,255)]
    downColors = [rgbString(255,102,102), rgbString(255,128,0),
                rgbString(255,239,0), rgbString(51,255,153),
                rgbString(0,182,238)]
    newColors = copy.deepcopy(upColors)
    for i in range(len(upColors)):
        if data.bpColors["actLev"][i] == True:
            newColors[i] = downColors[i]
    for i,(x0,y0,x1,y1,actLevel,color) in enumerate(data.actLevelsCoords):
        canvas.create_rectangle(x0,y0,x1,y1,fill=newColors[i],width=0)
        canvas.create_text((x1-x0)/2+x0,(y1-y0)/2+y0,text=actLevel)

#Redraws the calDef buttons
def newUserCalDefRedrawAll(canvas,data):
    upColors = ["wheat1","gray",rgbString(255,153,153)]
    downColors = ["goldenrod","gray42",rgbString(255,102,102)]
    newColors = copy.deepcopy(upColors)
    for i in range(len(upColors)):
        if data.bpColors["calDef"][i] == True:
            newColors[i] = downColors[i]
    for i,(x0,y0,x1,y1,calDef,color) in enumerate(data.calDefCoords):
        canvas.create_rectangle(x0,y0,x1,y1,fill=newColors[i],width=0)
        canvas.create_text((x1-x0)/2+x0,(y1-y0)/2+y0,text=calDef)

# Gets the coordinates for these boxes
def getNewUserQsCoords(width, height):
    result = []
    xRatio, yRatio, paddingRatio = 0.2, 0.25, 0.08
    xStart = xRatio * width
    yStart, padding = yRatio * height, paddingRatio * height
    text = ["Username (no spaces please):","Password:","Gender:",
            "Weight (lbs):","Height (in. (4ft=48,5ft=60,6ft=72)):",
            "Age:","Activity Level:","Future state goals:"]

    for i in range(len(text)):
        result.append([xStart, yStart + padding * i, text[i]])
    return result

# Gets the coordinates for these boxes
def getTextBoxCoords(questionCoords):
    result = []
    textBoxIndices = [0, 1, 3, 4, 5]
    textBoxWidth = 200
    cX, startY = 560, 130
    height = 30
    codes = ["user","password","gender","weight",
        "height","age","actLev","calDef"]

    for i in range(len(codes)):
        if i in textBoxIndices:
            x0 = cX - (textBoxWidth/2)
            x1 = x0 + textBoxWidth
            y0 = questionCoords[i][1] - (height/2)
            y1 = y0 + height
            result.append([x0,y0,x1,y1,codes[i]])
    return result

# Gets the coordinates for these boxes
def getGenderCoords(data,questionCoords):
    genderIndex = 2
    textBoxWidth = 200
    cX, startY = 560, 130
    height = 30
    vertMargin = 10

    x0 = cX - (textBoxWidth/2)
    x1 = x0 + textBoxWidth
    y0 = questionCoords[genderIndex][1] - (height/2)
    y1 = y0 + height

    newX1 = (x1 - x0)/2 + x0 - vertMargin
    newX0 = (x1 - x0)/2 + x0 + vertMargin
    return [[x0,y0,newX1,y1,"Female","pink"],
            [newX0,y0,x1,y1,"Male","dodgerBlue2"]]

# Gets the coordinates for these boxes
def getActLevelsCoords(data,questionCoords):
    result = []
    actLevelIndex = 6
    textBoxWidth = 400
    cX, startY = 560, 130
    height, margin = 30, 10
    n = 5
    colors = ["salmon","orange","yellow","aquamarine",rgbString(60,210,255)]
    text = ["Sedentary","1-3x/wk","3-5x/wk","6-7x/wk","Athlete"]
    codes = ["user","password","gender","weight",
            "height","age","actLev","calDef"]

    x0 = cX - (textBoxWidth/2)
    x1 = x0 + textBoxWidth
    y0 = questionCoords[actLevelIndex][1] - (height/2)
    y1 = y0 + height
    x1 = (x1-x0)/n + x0 - margin
    for i in range(n):
        result.append([x0,y0,x1,y1,text[i],colors[i]])
        x0 = x1 + margin
        x1 = x0 + ((textBoxWidth - (margin * n))/n)
    return result

# Gets the coordinates for these boxes
def getCalDefCoords(data,questionCoords):
    result = []
    calDefIndex = 7
    textBoxWidth = 300
    cX, startY = 560, 130
    height, margin = 30, 10
    n = 3
    colors = ["wheat1","gray","light coral"]
    text = ["Sedentary","Avg Adult","Toned"]
    codes = ["user","password","gender","weight",
        "height","age","actLev","calDef"]

    x0 = cX - (textBoxWidth/2)
    x1 = x0 + textBoxWidth
    y0 = questionCoords[calDefIndex][1] - (height/2)
    y1 = y0 + height
    x1 = (x1-x0)/n + x0 - margin
    for i in range(n):
        result.append([x0,y0,x1,y1,text[i],colors[i]])
        x0 = x1 + margin
        x1 = x0 + ((textBoxWidth - (margin * n))/n)
    return result

### Calculate ###

# Check that these are valid inputs! and input them from dict
# Formula Values from goo.gl/HeTXfq (BMR and Ratios)
def calculate(data,user,password,gender,weight,height,age,actLev,calDef): #toolong
    try:
        # Borrowed Ratios:
        femaleB, fWRatio, fHRatio, fARatio = 655, 4.35, 4.7, 4.7
        maleB, mWRatio, mHRatio, mARatio = 66, 6.23, 12.7, 6.8
        if gender == "Female":
            BMR = femaleB + (fWRatio*weight) + (fHRatio*height) - (fARatio*age)
        elif gender == "Male":
            BMR = maleB + (mWRatio * weight) + (mHRatio * height) - (mARatio * age)
        caloricDeficitVal = 125 # 1/4 lb per week estimate

        # Borrowed Ratios
        actLevDirectory = {"Sedentary":1.2,"1-3x/wk":1.375,"3-5x/wk":1.55,
                            "6-7x/wk":1.725,"Athlete":1.9}
        calsPerDay = BMR * actLevDirectory[actLev] - caloricDeficitVal

        # Borrowed Ratios, but personally readjusted a little bit
        proteinPercentages = [0.6, 0.9, 1.2]
        fatPercentages = [0.25, 0.35, 0.45]
     
        calDefDirectory = ["Sedentary","Avg Adult","Toned"]
        percentIndex = calDefDirectory.index(calDef)

        proteinCalsPerGram, fatCalsPerGram = 4, 9

        protein = proteinPercentages[percentIndex] * weight * proteinCalsPerGram
        fat = fatPercentages[percentIndex] * weight * fatCalsPerGram
        carbs = calsPerDay - protein - fat

        data.macros = [carbs, protein, fat]
    except:
        data.tryAgain = True
        data.mode = 'newUser'

# Redraws everything on the calculate page
def calculateRedrawAll(canvas,data):
    horizStretch, vertStretch = 0.3, 0.15
    canvas.create_text(data.width*horizStretch, data.height*vertStretch,
        text="the breakdown...", font="Arial 45 bold")

    calculatePieChartRedrawAll(canvas,data)
    calculateTextRedrawAll(canvas,data)

    canvas.create_rectangle(data.doneCoords, fill="black")
    canvas.create_text(data.doneText,fill="white",
        text="Let's Go!",font="Arial 12")
    canvas.create_rectangle(data.backCoords, fill="black")
    canvas.create_text(data.backText,fill="white",text="Back",font="Arial 12")

# Redraws the piechart based on some trigonometry and ratios
def calculatePieChartRedrawAll(canvas,data):
    pieCoords = (70,150,370,450)
    pieCx, pieCy = ((370-70)/2 + 70, (450-150)/2 + 150)
    piDegrees, radius, multiplier = 180, 150/2, 100/360
    ogStart = 90

    info = getPieSectorsCoords(data)
    percents = [info[1]*multiplier,info[4]*multiplier,info[7]*multiplier]
    colors = ["dodgerBlue2","salmon","aquamarine"]
    macros = ["carbs: %0.01f%%" % (percents[0]),
              "protein: %0.01f%%" % (percents[1]),
              "fats: %0.01f%%" % (percents[2])]

    for i in range(len(colors)):
        start = info[i * len(colors)]
        extent = info[i * len(colors) + 1]
        macroText = info[i * len(colors) + 1]
        fill = colors[i]
        canvas.create_arc(pieCoords, start = start, extent = extent,
                fill = fill, outline = fill)

        degree = (extent)/2 + start
        rads = (degree * math.pi / piDegrees)
        cx = pieCx + radius * math.cos(rads)
        cy = pieCy - radius * math.sin(rads)
        canvas.create_text(cx, cy, text=macros[i])

# Gets the coordinates to change model outside of the redraw function
def getPieSectorsCoords(data):
    ogStart = 90
    piDegrees = 180
    macros = ["carbs","protein","fats"]
    extent = []
    result = []

    if data.macros != [None, None, None]:
        total = sum(data.macros)
        for i in range(len(macros)):
            extent += [data.macros[i] / total * (piDegrees * 2)]
    start = [ogStart, ogStart + extent[0], ogStart + extent[0] + extent[1]]

    for i in range(len(extent)):
        result += [start[i], extent[i], macros[i]]
    return result

# Redraws all the text for the calculate screen
def calculateTextRedrawAll(canvas,data):
    caloriesText = "Total Calories Per Day: %d" % (sum(data.macros))
    caloriesX, caloriesY = 220, 470
    canvas.create_text(caloriesX, caloriesY, text=caloriesText)

    gramsPerCal = [4, 4, 9]
    centerX, startY = 625, 175
    titlePadding, regPadding = 100, 30
    macros = ["Carbs:","Protein:","Fats:"]

    for i in range(len(gramsPerCal)):
        x, y = centerX, startY + i * titlePadding
        canvas.create_text(x, y, text=macros[i], fill="dodgerBlue2",
                           font="Arial 20")

        y += regPadding
        text = "%d calories, %d grams/day" % (data.macros[i],
                data.macros[i]/gramsPerCal[i])
        canvas.create_text(x, y, text=text)

# Functions to open/edit file taken from goo.gl/qnf4CV
def calculateMousePressed(event,data):
    dX0, dY0, dX1, dY1 = data.doneCoords
    bX0, bY0, bX1, bY1 = data.backCoords
    if inBounds(dX0,dX1,dY0,dY1,event.x,event.y):
        data.mode = "main"
        with open("users.txt","a") as file:
            file.write(assembleNewUser(data))
    elif inBounds(bX0,bX1,bY0,bY1,event.x,event.y):
        data.mode = "newUser"

# Prepares the user's info to be submitted to the outside text file
def assembleNewUser(data):
    user = data.messages['user']
    password = data.messages['password']
    gender = data.userProfile['gender']
    weight = float(data.messages['weight'])
    height = float(data.messages['height'])
    age = float(data.messages['age'])
    actLev = data.userProfile['actLev']
    calDef = data.userProfile['calDef']
    carbs = data.macros[0]
    protein = data.macros[1]
    fats = data.macros[2]
    calories = sum(data.macros)
    (data.saturatedFat, data.cholesterol, 
        data.sodium, data.dietaryFiber) = getUserPDV(calories)

    return assemble(user, password, gender, weight, height, age, actLev,
        calDef, carbs, protein, fats, calories, data.saturatedFat,
        data.cholesterol,data.sodium,data.dietaryFiber)

# Gets the user's percent daily values and stores them in data
def getUserPDV(calories):
    result = [None, None, None, None]

    saturatedFatRatio = 20/2000 # 20g / 2000 cal diet
    cholesterolRatio = 300/2000 # 300mg / 2000 cal diet
    sodiumRatio = 2400/200 # 2400mg / 2000 cal diet
    dietaryFiberRatio = 25/2000 # 25g / 2000 cal diet

    ratioList = [saturatedFatRatio, cholesterolRatio,
                 sodiumRatio, dietaryFiberRatio]

    for i in range(len(ratioList)):
        result[i] = calories * ratioList[i]
    return result

# Makes all the needed values into a string that is appended to the doc
def assemble(*args):
    s = "\n"
    length = len(args)
    for i,variable in enumerate(args):
        if i != (length - 1):
            s += str(variable) + ","
        else:
            s += str(variable)
    return s

### Main ###

# Initializes variables for the main screen
def initMain(data):
    data.settingsCoords, data.settingsText = (600,20,750,40), (675,30)
    data.dailyArcCoords = [(350,50,450,150),(150,200,250,300),
                           (350,200,450,300),(550,200,650,300)]
    data.dailyFillCoords = [(360,60,440,140),(160,210,240,290),
                           (360,210,440,290),(560,210,640,290)]
    data.dailyTextCoords = [(400,110),(200,260),(400,260),(600,260)]
    data.dailyMacroCoords = [(400,90),(200,240),(400,240),(600,240)]
    data.dailyText = ["calories","carbs","protein","fats"]
    data.currMacros = [0, 0, 0, 0] #get Cals, Carbs, Protein, Fats
    data.boxCoords = [(150,350,375,425),(425,350,650,425),
                 (150,450,375,525),(425,450,650,525)]
    data.redirectTextCoords = [(262.5,387.5),(537.5,387.5),
                  (262.5,487.5),(537.5,487.5)]
    data.redirectButtons = ["Log Food", "Visualize",
                            "Recommend", "Grocery List"]

# Redraws the main screen
def mainRedrawAll(canvas,data):
    # Menu buttons
    canvas.create_rectangle(data.settingsCoords, fill="black")
    canvas.create_text(data.settingsText,fill="white",
        text="Settings",font="Arial 12")
    canvas.create_rectangle(data.backCoords, fill="black")
    canvas.create_text(data.backText,fill="white",text="Back",font="Arial 12")

    result = getDailyMacroPercentCoords(data)
    ogStart = 90
    color = rgbString(0,206,238)

    # Draw figures for general trackers
    todayX, todayY = 400, 30
    canvas.create_text(todayX,todayY,text="Today",fill="gray",font="Arial 14")
    for i, (coords) in enumerate(data.dailyArcCoords):
        canvas.create_arc(coords, start=ogStart, extent=result[i],
                          fill=color, outline=color)
        canvas.create_oval(data.dailyFillCoords[i], fill="white", width=0)
        canvas.create_text(data.dailyTextCoords[i], text=data.dailyText[i])
        canvas.create_text(data.dailyMacroCoords[i],
                          text=data.currMacros[i],font="Arial 20")

    drawRedirectBoxes(canvas,data)

# Gets the coordinates for the area the arc should sweep out
# in the trackers at the top of the page
def getDailyMacroPercentCoords(data):
    result = []
    ogStart = 90
    piDegrees = 180
    for i in range(len(data.currMacros)):
        if data.macros != [None, None, None]:
            total = sum(data.macros) if (i == 0) else data.macros[i-1]
            result.append(data.currMacros[i] / total * piDegrees * 2)
    return result

# Controls the mosuePress functions for the main screen
def mainMousePressed(event,data):
    dX0, dY0, dX1, dY1 = data.settingsCoords
    bX0, bY0, bX1, bY1 = data.backCoords
    if inBounds(dX0,dX1,dY0,dY1,event.x,event.y):
        data.mode = "newUser"
    elif inBounds(bX0,bX1,bY0,bY1,event.x,event.y):
        data.mode = "calculate"
    for i,(x0,y0,x1,y1) in enumerate(data.boxCoords):
        if inBounds(x0,x1,y0,y1,event.x,event.y):
            data.mode = data.redirectButtons[i]

# Draws the boxes that change the modes in this screen
def drawRedirectBoxes(canvas,data):
    for i,(x0,y0,x1,y1) in enumerate(data.boxCoords):
        canvas.create_rectangle(x0,y0,x1,y1,fill="white",
                                outline="gray",width=5)
        canvas.create_text(data.redirectTextCoords[i],
                           text=data.redirectButtons[i])

# Controls keypresses for the main screen
def mainKeyPressed(event,data):
    if event.keysym == "Left":
        pass
    elif event.keysym == "Right":
        pass

### Log Food ###

# Initializes coordinates and the dictionaries for collecting
# the values of each food
def initLogFood(data):
    data.locationBackGroundCoords = [(100,175,300,210),
                                     (100,215,300,250),
                                     (100,255,300,290),
                                     (100,295,300,330)]
    data.mealBackGroundCoords = [(500,175,700,210),
                                 (500,215,700,250),
                                 (500,255,700,290),
                                 (500,295,700,330),
                                 (500,335,700,370)]
    data.selectedLocation = None
    data.selectedMeal = None
    data.mealText = None
    data.logMealTryAgain = False
    data.locationColors = [False, False, False, False]
    data.mealColors = [False, False, False, False, False]
    data.lastLocationIndex = None
    data.lastMealIndex = None
    data.nutriFacts = {"Calories":1,"Total Fat":1,"Saturated Fat":1,
    "Trans Fat":1,"Cholesterol":1,"Sodium":1,"Total Carbohydrate":1,
    "Dietary Fiber":1,"Sugars":1,"Protein":1,"Vitamin A":1,"Vitamin C":1,
    "Calcium":1,"Iron":1}
    initLogFoodCategories(data)

# Holds the foods, fildNames, and location for food on campus
def initLogFoodCategories(data):
    data.TAZ = {"Cranberry Scone":"cranberryScone.html",
                "Super Grain Bagel":"superGrainBagel.html",
                "Triple Berry Apple Tart":"tripleBerryAppleTart.html",
                "Veggie Frittata":"veggieFrittata.html",
                "Beans and Greens Panini":"beansAndGreensPanini.html"}
    data.EXC = {"Mac and Cheese":"macAndCheese.html","Chicken Fingers":
                "chickenFingers.html","Beef Stroganoff":"beefStroganoff.html",
                "Bulgar Wheat Kale Salad":"bulgarWheatKaleSalad.html",
                "Vegetable Wrap":"vegetableWrap.html",}
    data.CRP = {"Wake Up Crepe":"wakeUpCrepe.html",
                "Vegetarian Crepe":"vegetarianCrepe.html",
                "Buffalo Chicken Crepe":"buffaloChickenCrepe.html",
                "Banana Split Crepe":"bananaSplitCrepe.html",
                "Strawberry Sundae Crepe":"strawberrySundaeCrepe.html"}
    data.UGD = {"Chicken Quesadilla":"chickenQuesadilla.html",
                "Classic Caesar Salad":"classicCaesarSalad.html",
                "Crunchy Quinoa Salad":"crunchyQuinoaSalad.html",
                "Italian Wedding Soup":"italianWeddingSoup.html",
                "Black Bean Quinoa Burger":"blackBeanQuinoaBurger.html"}

# Redraws the food logging screen
def logFoodRedrawAll(canvas,data):
    # Menu buttons
    canvas.create_rectangle(data.settingsCoords, fill="black")
    canvas.create_text(data.settingsText,fill="white",
        text="Settings",font="Arial 12")
    canvas.create_rectangle(data.backCoords, fill="black")
    canvas.create_text(data.backText,fill="white",text="Back",font="Arial 12")
    canvas.create_rectangle(data.doneCoords, fill="black")
    canvas.create_text(data.doneText,fill="white",
        text="Submit",font="Arial 12")

    horizStretch, vertStretch = 0.2, 0.1
    canvas.create_text(data.width*horizStretch, data.height*vertStretch,
        text="log a meal...", font="Arial 45 bold")

    logFoodLocationRedrawAll(canvas,data)
    logFoodMealRedrawAll(canvas,data)
    logFoodNutritionRedrawAll(canvas,data)

    if data.logMealTryAgain == True:
        canvas.create_text(660, 520,
            text="Please fill out all values!",fill="fireBrick")

# Redraws the available locations
def logFoodLocationRedrawAll(canvas,data):
    text = ["Tazza D'Oro", "Exchange","Creperie","Underground"]
    canvas.create_text(200,150,text="Select a location:",
        font="Arial 16")

    colors = ["maroon1"] * len(text)
    downColor = "yellow"
    newColors = copy.deepcopy(colors)
    margin = 5
    for i in range(len(colors)):
        if data.locationColors[i] == True:
            newColors[i] = downColor

    for j,(x0,y0,x1,y1) in enumerate(data.locationBackGroundCoords):
        canvas.create_rectangle(x0,y0,x1,y1,fill="gray",width=0)
        x0, y0, x1, y1 = x0 + margin, y0 + margin, x1 - margin, y1 - margin
        canvas.create_rectangle(x0,y0,x1,y1,fill=newColors[j],width=0)
        textX, textY = (x1-x0)/2 + x0, (y1-y0)/2 + y0
        canvas.create_text(textX, textY, text=text[j])

def logFoodMealRedrawAll(canvas,data):
    length = 5
    canvas.create_text(600,150,text="Select a meal:",font="Arial 16")
    if data.selectedLocation != None:
        locations = ["Tazza D'Oro", "Exchange","Creperie","Underground"]
        varNames = [data.TAZ, data.EXC, data.CRP, data.UGD]
        index = locations.index(data.selectedLocation)
        data.mealText = [key for key in varNames[index]]

        colors = ["yellow"] * length
        downColor = "maroon1"
        newColors = copy.deepcopy(colors)
        for i in range(len(colors)):
            if data.mealColors[i] == True:
                newColors[i] = downColor
        margin = 5

        for j,(x0,y0,x1,y1) in enumerate(data.mealBackGroundCoords):
            canvas.create_rectangle(x0,y0,x1,y1,fill="gray",width=0)
            x0, y0, x1, y1 = x0 + margin, y0 + margin, x1 - margin, y1 - margin
            canvas.create_rectangle(x0,y0,x1,y1,fill=newColors[j],width=0)
            textX, textY = (x1-x0)/2 + x0, (y1-y0)/2 + y0
            canvas.create_text(textX, textY, text=data.mealText[j])

def logFoodNutritionRedrawAll(canvas,data):
    canvas.create_text(400,350,text="Nutrition Facts:",font="Arial 18")
    if data.selectedMeal != None:
        locations = ["Tazza D'Oro", "Exchange","Creperie","Underground"]
        varNames = [data.TAZ, data.EXC, data.CRP, data.UGD]
        index = locations.index(data.selectedLocation)
        data.mealText = [key for key in varNames[index]]
        text = varNames[index][data.selectedMeal]
        data.nutriFacts = getNutrition(text)
        cx, cy = 400, 370
        margin = 15
        for key in data.nutriFacts:
            text = key + ": " + data.nutriFacts[key]
            canvas.create_text(cx,cy,text=text)
            cy += margin

def logFoodMousePressed(event,data):
    sX0, sY0, sX1, sY1 = data.settingsCoords
    dX0, dY0, dX1, dY1 = data.doneCoords
    bX0, bY0, bX1, bY1 = data.backCoords
    if inBounds(dX0,dX1,dY0,dY1,event.x,event.y):
        if data.selectedLocation != None and data.selectedMeal != None:
            data.mode = "score"
            data.currMacros[0] = float(data.nutriFacts["Calories"])
            temp = stripNonNumbers(data.nutriFacts["Total Carbohydrate"])
            data.currMacros[1] = temp * 4
            temp = stripNonNumbers(data.nutriFacts["Protein"])
            data.currMacros[2] = temp * 4
            temp = stripNonNumbers(data.nutriFacts["Total Fat"])
            data.currMacros[3] = temp * 9
            with open("timeData.txt","a") as file:
                file.write(assembleTimeData(data))
        else:
            data.logMealTryAgain = True
    elif inBounds(bX0,bX1,bY0,bY1,event.x,event.y):
        data.mode = "main"
    elif inBounds(sX0,sX1,sY0,sY1,event.x,event.y):
        data.mode = "newUser"

    logFoodLocationMousePressed(event,data)
    logFoodMealMousePressed(event,data)

def logFoodLocationMousePressed(event,data):
    codes = ["Tazza D'Oro", "Exchange","Creperie","Underground"]
    for i,code in enumerate(codes):
        x0, y0, x1, y1 = data.locationBackGroundCoords[i]
        if inBounds(x0,x1,y0,y1,event.x,event.y):
            data.logMealTryAgain = False
            data.selectedLocation = code
            data.locationColors[i] = not data.locationColors[i]
            data.lastLocationIndex = i
            data.lastMealIndex = None
            data.selectedMeal = None
        else:
            data.locationColors[i] = False
    if True not in data.locationColors:
        if data.lastLocationIndex != None:
            data.locationColors[data.lastLocationIndex] = True

def logFoodMealMousePressed(event,data):
    if data.mealText != None:
        codes = data.mealText
        for i,code in enumerate(codes):
            x0, y0, x1, y1 = data.mealBackGroundCoords[i]
            if inBounds(x0,x1,y0,y1,event.x,event.y):
                data.logMealTryAgain = False
                data.selectedMeal = code
                data.mealColors[i] = not data.mealColors[i]
                data.lastMealIndex = i
            else:
                data.mealColors[i] = False
    if True not in data.mealColors:
        if data.lastMealIndex != None:
            data.mealColors[data.lastMealIndex] = True

### WebScraping-ish Process ###

# def getFiles(path):
#     nutriFacts = dict()
#     for fileName in os.listdir(path):
#         newPath = path + "/" + fileName
#         if (os.path.isdir(newPath) == False and
#             fileName != ".DS_Store" and fileName != "foobar.py"
#             and fileName != "removeDsStore.py"):
#             nutriFacts[fileName] = getNutrition(fileName)
#     return nutriFacts

# 'open' and 'repr' commands from goo.gl/EwjmQc
def getNutrition(fileName):
    nutrition = dict()
    file = open(fileName,"r")
    txt = repr(file.read())
    values = ["Calories","Total Fat","Saturated Fat","Trans Fat",
        "Cholesterol","Sodium","Total Carbohydrate","Dietary Fiber",
        "Sugars","Protein","Vitamin A","Vitamin C","Calcium","Iron"]
    for val in values:
        guessLen = 12
        length = len(val)
        index = txt.index(val)
        guess = txt[index+length:index+length+guessLen]
        guess = guess.replace("</b>","")
        nutrition[val] = ""
        while guess[0] != "<":
            if guess[0] != " ":
                nutrition[val] += guess[0]
            guess = guess[1:]
    return nutrition

### Score ###

def initScore(data):
    data.scoreRatio = 1
    data.scoreNutriFacts = {"Calories":1,"Total Fat":1,"Saturated Fat":1,
    "Trans Fat":1,"Cholesterol":1,"Sodium":1,"Total Carbohydrate":1,
    "Dietary Fiber":1,"Sugars":1,"Protein":1,"Vitamin A":1,"Vitamin C":1,
    "Calcium":1,"Iron":1}
    data.subScores = []

    getScoreOutOf100Cals(data)

def getScoreOutOf100Cals(data):
    for key in data.nutriFacts:
        if key != "Calories":
            data.scoreNutriFacts[key] = data.nutriFacts[key] / data.scoreRatio

# Gets the score for each of the categories for the score based on weights
def getScore(data):
    try:
        weights = [0.25,0.05,0.2,0.2,0.3]
        data.scoreRatio = float(data.nutriFacts["Calories"]) / 100
        score1 = scoreSect1(data) * weights[0]
        score2 = scoreSect2(data) * weights[1]
        score3 = scoreSect3(data) * weights[2]
        score4 = scoreSect4(data) * weights[3]
        score5 = scoreSect5(data) * weights[4]
        total = score1 + score2+ score3 + score4 + score5

        data.subScores = [score1,score2,score3,score4,score5]

        if (total >= 9): letter = "A"
        elif (total >= 8): letter = "B"
        elif (total >= 7): letter = "C"
        else: letter = "D"
    except:
        letter = "D"
    return letter

def scoreSect1(data):
    ratio = 0.1
    startScore = 10
    # Gives what 10% of User's Daily Value is
    tempList = [data.saturatedFat, data.cholesterol, data.sodium]
    for i,item in enumerate(tempList):
        if not isinstance(item, float):
            tempList[i] = stripNonNumbers(tempList[i])
    ratios = {"Saturated Fat": ratio * tempList[0],
            "Cholesterol": ratio * tempList[1],
            "Sodium": ratio * tempList[2]}
    results = {"Saturated Fat": startScore,
            "Cholesterol": startScore,
            "Sodium": startScore, "Sugars": startScore}

    for key in data.nutriFacts:
        if key in ["Saturated Fat","Cholesterol","Sodium"]:
            foodVal = stripNonNumbers(data.nutriFacts[key]) # Actual value of food
            diff = abs(foodVal - ratios[key])
            diff = math.floor(diff / ratios[key])
            results[key] -= diff
    # Test for sugar separately, amount out of 100 calories
    maxSugar = 5
    if data.scoreNutriFacts["Sugars"] > maxSugar:
        results["Sugars"] -= data.scoreNutriFacts["Sugars"] / maxSugar
    return getAverage(results)

def stripNonNumbers(s):
    newS = ""
    for c in s:
        if c in string.digits:
            newS += c
        else:
            break
    return float(newS)

# Tries to keep trans fats close to 0, and subtracts points as it increases
def scoreSect2(data):
    maxTransFats = 3
    score = 10
    if data.scoreNutriFacts["Trans Fat"] > maxTransFats:
        score -= data.scoreNutriFacts["Trans Fat"] / maxTransFats
    return score

# Ideal = 0.2 - 0.3% of percent daily value
def scoreSect3(data):
    minRatio, maxRatio = 0.2, 0.3
    score, count = 10, 0
    dietFib = float(data.dietaryFiber)
    done = False
    while done == False:
        if ((data.scoreNutriFacts["Dietary Fiber"] >= minRatio * dietFib) or 
            (data.scoreNutriFacts["Dietary Fiber"] <= maxRatio * dietFib)):
            done = True
            return score - count
        else:
            count += 1
            minRatio *= count
            maxRatio *= count
    return score

# Ideal = 0.2 - 0.3% of percent daily value
def scoreSect4(data):
    score = 10
    results = {"Vitamin A":score, "Vitamin C":score,
               "Calcium":score, "Iron":score}
    for key in results:
        minRatio, maxRatio = 0.2, 0.3
        count = 0
        done = False
        while done == False:
            if ((stripNonNumbers(data.nutriFacts[key]) >= minRatio) or
                (stripNonNumbers(data.nutriFacts[key]) <= maxRatio)):
                done = True
                results[key] = score - count
            else:
                count += 1
                minRatio *= count
                maxRatio *= count
    return getAverage(results)

# Keeps the macro percents in the ideal ones calculated as ideal
def scoreSect5(data):
    score = 10
    gramsPerCal = [4, 4, 9]
    names = ["Total Carbohydrate", "Protein","Total Fat"]
    results = {"Total Carbohydrate":score,"Protein":score,
                "Total Fat":score}
    for i,key in enumerate(names):
        projectedGrams = data.macros[i] / gramsPerCal[i]
        realGrams = stripNonNumbers(data.nutriFacts[key])
        percentDiff = abs(projectedGrams - realGrams) / projectedGrams * 100
        results[key] -= percentDiff // 10
    return getAverage(results)

def getAverage(results):
    total, count = 0, 0
    for key in results:
        total += results[key]
        count += 1
    return total / count

def scoreRedrawAll(canvas,data):
    # Menu buttons
    canvas.create_rectangle(data.settingsCoords, fill="black")
    canvas.create_text(data.settingsText,fill="white",
        text="Settings",font="Arial 12")
    canvas.create_rectangle(data.backCoords, fill="black")
    canvas.create_text(data.backText,fill="white",text="Back",font="Arial 12")
    canvas.create_rectangle(data.doneCoords, fill="black")
    canvas.create_text(data.doneText,fill="white",
        text="Done",font="Arial 12")

    horizStretch, vertStretch = 0.3, 0.1
    canvas.create_text(data.width*horizStretch, data.height*vertStretch,
        text="your meal score...", font="Arial 45 bold")

    overallScoreRedrawAll(canvas,data)
    subScoreRedrawAll(canvas,data)

def overallScoreRedrawAll(canvas,data):
    letter = getScore(data)
    outerCoords = 300,150,500,350
    middleCoords = 310,160,490,340
    innerCoords = 315,165,485,335
    textX, textY = 400,250
    canvas.create_oval(outerCoords,fill="aquamarine",width=0)
    canvas.create_oval(middleCoords,fill="white",width=0)
    canvas.create_oval(innerCoords,fill="aquamarine",width=0)
    canvas.create_text(textX,textY,text=letter,fill="white",font="Arial 70")
    canvas.create_text(textX,textY + 120, text="Overall:")

def subScoreRedrawAll(canvas,data):
    weights = [2.5, .5, 2, 2, 3]
    text = ["Bad Micros:","Bad Fats:","Fiber:","Good Micros:","Macros:"]

    start = 400 / 5.5
    smallPad, largePad = 2, 5
    oX0,oY0,oX1,oY1 = start,385,2 * start,385 + start
    if data.subScores != []:
        for i in range(len(weights)):
            if i != 0:
                oX0,oY0,oX1,oY1 = oX0+2*start,oY0,oX1+2*start,oY1

            mX0,mY0,mX1,mY1 = oX0+largePad,oY0+largePad,oX1-largePad,oY1-largePad
            iX0,iY0,iX1,iY1 = mX0+smallPad,mY0+smallPad,mX1-smallPad,mY1-smallPad
            textX, textY = (oX1-oX0)/2+oX0, (oY1-oY0)/2+oY0
            if data.subScores[i] != []:
                innerText = "%0.1f/%0.1f" % (data.subScores[i],weights[i])

            canvas.create_oval(oX0,oY0,oX1,oY1,fill="salmon",width=0)
            canvas.create_oval(mX0,mY0,mX1,mY1,fill="white",width=0)
            canvas.create_oval(iX0,iY0,iX1,iY1,fill="salmon",width=0)
            if data.subScores[i] != []:
                canvas.create_text(textX,textY,text=innerText,
                    fill="white",font="Arial 15")
            canvas.create_text(textX,textY + 0.75 * start,text=text[i])

def scoreMousePressed(event,data):
    sX0, sY0, sX1, sY1 = data.settingsCoords
    dX0, dY0, dX1, dY1 = data.doneCoords
    bX0, bY0, bX1, bY1 = data.backCoords
    if inBounds(dX0,dX1,dY0,dY1,event.x,event.y):
        data.mode = "main"
    elif inBounds(bX0,bX1,bY0,bY1,event.x,event.y):
        data.mode = "Log Food"
    elif inBounds(sX0,sX1,sY0,sY1,event.x,event.y):
        data.mode = "newUser"

### Visualize ###

def initVisualize(data):
    data.date = str(datetime.now())[0:10]
    data.year = int(data.date[0:4])
    if data.date[5] == '0':
        data.month = int(data.date[6])
    else:
        data.month = int(data.date[5:7])
    data.day = int(data.date[8:10])
    data.lastSevenDays = []
    data.visualizeCals = {}

    getLastSevenDays(data)

def visualizeRedrawAll(canvas,data):
    horizStretch, vertStretch = 0.2, 0.1
    canvas.create_text(data.width*horizStretch, data.height*vertStretch,
        text="visualize...", font="Arial 45 bold")

    canvas.create_rectangle(data.settingsCoords, fill="black")
    canvas.create_text(data.settingsText,fill="white",
        text="Settings",font="Arial 12")
    canvas.create_rectangle(data.backCoords, fill="black")
    canvas.create_text(data.backText,fill="white",text="Back",font="Arial 12")

    visualizeGraphBasicsRedrawAll(canvas,data)
    importTimeData(data)
    drawBarsRedrawAll(canvas,data)

    calorieHeight = 1 - (sum(data.macros) / 3000) #3000 = guess of maxCals
    calorieHeight = (500-150) * calorieHeight + 150
    canvas.create_line(150,calorieHeight,650,calorieHeight,fill="red",width=5)
    canvas.create_text(75,calorieHeight,text="Your Target Cals")

def drawBarsRedrawAll(canvas,data):
    horizAxisHeight = 525
    startX = 185
    gap = (650-150)/7
    calWidth = 20
    lastSevenDays = data.lastSevenDays[::-1]
    for i,date in enumerate(lastSevenDays):
        if date in data.visualizeCals:
            cals = float(data.visualizeCals[date])
            calXStart = startX + gap * i
            calHeight = 1 - (cals / 3000)
            calHeight = (500-150) * calHeight + 150
            canvas.create_rectangle(calXStart - calWidth,calHeight,
                calXStart + calWidth,500,
                fill="dodgerBlue2",width=0)
            canvas.create_text(calXStart,530,text=date)

def visualizeGraphBasicsRedrawAll(canvas,data):
    canvas.create_line(150,150,150,500)
    canvas.create_line(150,500,650,500)
    canvas.create_text(400,550,text="Days")
    canvas.create_text(125,325,text="Cals")
    canvas.create_text(100,150,text="3000")
    canvas.create_text(100,500,text="0")

def visualizeMousePressed(event,data):
    sX0, sY0, sX1, sY1 = data.settingsCoords
    bX0, bY0, bX1, bY1 = data.backCoords
    if inBounds(bX0,bX1,bY0,bY1,event.x,event.y):
        data.mode = "main"
    elif inBounds(sX0,sX1,sY0,sY1,event.x,event.y):
        data.mode = "newUser"

# Sends the data out to the timeData.txt file
def assembleTimeData(data):
    date = "%s/%s/%s" % (str(data.month),str(data.day),str(data.year))
    return assemble(data.messages["user"],date,str(sum(data.currMacros)))

# Finds out the "mm/dd/yy" formula of the past seven days
def getLastSevenDays(data):
    numDays = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,
               9:30,10:31,11:30,12:31}
    if data.year % 4 == 0:
        numDays[2] = 29
    dMonth,dDate = 0, 1
    month,day,year = data.month, data.day, data.year
    for i in range(7):
        if month == 0:
            year -= 1
            month = 12
        if day == 0:
            if month == 1:
                day = numDays[12]
                month = 12
            else:
                day = numDays[month-1]
                month -= 1
        data.lastSevenDays.append("%s/%s/%s" % (str(month),str(day),str(year)))
        day -= 1

# Gets the time / calories for the day of the user from the file
def importTimeData(data):
    file = open("timeData.txt","r")
    txt = str(file.read())
    for info in txt.splitlines():
        for i,elem in enumerate(info.split(",")):
            if elem == data.messages["user"]:
                result = [elem for elem in info.split(",")]
                data.messages['user'] = result[0]
                for i in range(1,len(result)):
                    if (i%2) != 0: # ODD, so it's a date
                        data.visualizeCals[result[i]] = 0
                    else: # EVEN, so it's a calorie count
                        data.visualizeCals[result[i-1]] = result[i]


### Recommend + Grocery List ###

def pageUCRedrawAll(canvas,data):
    canvas.create_rectangle(data.settingsCoords, fill="black")
    canvas.create_text(data.settingsText,fill="white",
        text="Settings",font="Arial 12")
    canvas.create_rectangle(data.backCoords, fill="black")
    canvas.create_text(data.backText,fill="white",text="Back",font="Arial 12")

    canvas.create_text(data.width/2,data.height/2,
        text="Page Under Construction! :(",font="Arial 40")

def pageUCMousePressed(event,data):
    sX0, sY0, sX1, sY1 = data.settingsCoords
    bX0, bY0, bX1, bY1 = data.backCoords
    if inBounds(bX0,bX1,bY0,bY1,event.x,event.y):
        data.mode = "main"
    elif inBounds(sX0,sX1,sY0,sY1,event.x,event.y):
        data.mode = "newUser"

### Login ###

def initLogin(data):
    data.loginCoords = []
    data.loginMsgs = ["",""]
    data.loginTyping = False
    data.currLoginCoords = None
    data.loginTryAgain = False
    data.validLogin = False

    getLoginCoords(data)

def loginRedrawAll(canvas,data):
    horizStretch, vertStretch = 0.2, 0.1
    canvas.create_text(data.width*horizStretch, data.height*vertStretch,
        text="login:", font="Arial 45 bold")

    canvas.create_rectangle(data.backCoords, fill="black")
    canvas.create_text(data.backText,fill="white",text="Back",font="Arial 12")
    canvas.create_rectangle(data.doneCoords, fill="black")
    canvas.create_text(data.doneText,fill="white",
        text="Login",font="Arial 12")

    for i,(x0,x1,y0,y1,textX,textY,title) in enumerate(data.loginCoords):
        padding = 40
        canvas.create_rectangle(x0,y0,x1,y1)
        canvas.create_text(textX, textY - padding, text=title)
        canvas.create_text(textX, textY, text=data.loginMsgs[i])

    if data.loginTryAgain == True:
        textX, textY = 400, 550
        canvas.create_text(textX, textY, 
            text="Not valid. Try again.",fill="fireBrick")

def getLoginCoords(data):
    x0, x1, textX = 300, 500, 400
    y0, y1, padding = 150, 200, 80
    text = ["Username","Password"]

    for i in range(len(text)):
        y0 += padding
        y1 += padding
        textY = ((y1-y0)/2) + y0
        data.loginCoords.append([x0,x1,y0,y1,textX,textY,text[i]])

def loginMousePressed(event,data):
    dX0, dY0, dX1, dY1 = data.doneCoords
    bX0, bY0, bX1, bY1 = data.backCoords
    if inBounds(dX0,dX1,dY0,dY1,event.x,event.y):
        getUserInfo(data,data.loginMsgs[0],data.loginMsgs[1])
        if data.validLogin:
            data.mode = "main"
            user = data.loginMsgs[0]
            password = data.loginMsgs[1]
    elif inBounds(bX0,bX1,bY0,bY1,event.x,event.y):
        data.mode = "home"
        init(data)
    for i,(x0,x1,y0,y1,textX,textY,title) in enumerate(data.loginCoords):
        if inBounds(x0,x1,y0,y1,event.x,event.y):
            data.loginTyping = True
            data.currLoginCoords = (x0,x1,y0,y1)

def loginKeyPressed(event,data):
    if data.loginTyping == True:
        for i,(x0,x1,y0,y1,textX,textY,text) in enumerate(data.loginCoords):
            if (x0,x1,y0,y1) == data.currLoginCoords:
                key = event.keysym
                if key == 'BackSpace':
                    if data.loginMsgs[i] != '':
                        data.loginMsgs[i] = data.loginMsgs[i][:-1]
                if (key in string.ascii_letters) or (key in string.digits):
                    key = key.lower()
                    data.loginMsgs[i] += key

# 'open' and 'repr' commands from goo.gl/EwjmQc
def getUserInfo(data,user,password):
    file = open("users.txt","r")
    txt = repr(file.read())
    try:
        userIndex = txt.index(user)
        passwordIndex = txt.index(password)
        if passwordIndex == (userIndex + len(user) + 1):
            data.loginTryAgain = False
            data.validLogin = True
            importUserInfo(data,user)
        else:
            data.mode = 'login'
            data.loginTryAgain = True
    except:
        data.mode = 'login'
        data.loginTryAgain = True

# Gets the user info from the file and stores it
# in the available variables here
def importUserInfo(data,user):
    file = open("users.txt","r")
    txt = str(file.read())
    for info in txt.splitlines():
        for i,elem in enumerate(info.split(",")):
            if elem == user:
                result = [elem for elem in info.split(",")]
                data.messages['user'] = result[0]
                data.messages['password'] = result[1]
                data.userProfile['gender'] = result[2]
                data.messages['weight'] = float(result[3])
                data.messages['height'] = float(result[4])
                data.messages['age'] = float(result[5])
                data.userProfile['actLev'] = result[6]
                data.userProfile['calDef'] = result[7]
                data.macros[0] = float(result[8])
                data.macros[1] = float(result[9])
                data.macros[2] = float(result[10])
                # Skip 11: Calories are accounted for through macros
                data.saturatedFat = result[12]
                data.cholesterol = result[13]
                data.sodium = result[14]
                data.dietaryFiber = result[15]

####################################
# Run function from goo.gl/ihrY8K
####################################

# Run function from 15-112
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()

    # Note change #1:
    root.resizable(width=FALSE, height=FALSE)

    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def mellonBites():
    run(800,600)

mellonBites()