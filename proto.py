from random import randint

# Robot signal in form [BotType and details][xxyy][enemy_base_found][xxyy]
# BotType and details is a string of length 3. xx and yy are base co-ordinates
# enemy_base_found is a one letter string either T or F. Initialised as F
# The xx and yy after are the enemy base coordinates initialised as 0000


def isCloseTo(initPos, finalPos):
    #determine wether finalPos is one move or less away from initPos or not. initPos and finalPos are tuples storing cartesian co-ordinates
    #returns a boolean

    return ((abs(initPos[1] - finalPos[1]) <= 1) and (abs(initPos[0] - finalPos[0]) <= 1))

def moveTowards(initPos, finalPos):
    #determine which step to take if bot wants to move from one point ot another. initPos and finalPos are tuples storing cartesian co-ordinates

    difX = finalPos[0] - initPos[0]
    difY = finalPos[1] - initPos[1]
    probab_factor = randint(1,100)
    probabX = (difX*100)/(difY+difX + 1)
    if ((abs(initPos[1] - finalPos[1]) == 0) and (abs(initPos[0] - finalPos[0]) == 0)):
        return 0
    if (probab_factor <= probabX):
        if (difX>0):
            return 2
        if (difX<0):
            return 4
        else:
            if (difY>0):
                return 1
            if (difY<0):
                return 3

    else:
        if (difY>0):
            return 1
        if (difY<0):
            return 3
        else:
            if (difX>0):
                return 2
            if (difX<0):
                return 4

    #currently works by moving in the y-axis till the y co-ordinates are same and then moving in the x-axis
    up = finalPos[1] - initPos[1]
    right = finalPos[0] - initPos[0]
    if(up != 0):
        return (2 - ((up>0) - (up<0))) # this snippet ((up>0) - (up<0)) basically acts as a sign function. returns 1 if up>0 and -1 if up<0
    elif(right != 0):
        return (3 - ((right>0) - (right<0))) # same for the snippet here
    else:
        return 0
def ActRobot(robot):
"""
    Flowchart for a bot:
    1) Get data about neighbouring cells.
    2) Check if there is an enemy bot or base near it and deploy virus. Avoid it after that.
    3) Update base location.
    4) Perform type specific function.
"""

    enemy = ["enemy", "enemy-base"]
    friend = ["friend", "friend-base"]

    # Get data about neighbouring cells
    location_data = {}
    location_data["up"] = robot.investigate_up()
    location_data["down"] = robot.investigate_down()
    location_data["left"] = robot.investigate_left()
    location_data["right"] = robot.investigate_right()
    location_data["ne"] = robot.investigate_ne()
    location_data["nw"] = robot.investigate_nw()
    location_data["se"] = robot.investigate_se()
    location_data["sw"] = robot.investigate_sw()
    location_data["Map"] = (robot.GetDimensionX(), robot.GetDimensionY())
    location_data["self_cor"] = robot.GetPosition()
    print(robot.GetPosition())

    # Check if there is an enemy bot or base near it and deploy virus. Avoid it after that
    if (((location_data["up"] in enemy)+(location_data["down"] in enemy)+(location_data["left"] in enemy)+(location_data["right"] in enemy)+(location_data["ne"] in enemy)+(location_data["nw"] in enemy)+(location_data["se"] in enemy)+(location_data["sw"] in enemy))):
        robot.DeployVirus(800)
        if location_data["up"] == "enemy":
            return 1
        if location_data["down"] == "enemy":
            return 3
        if location_data["left"] == "enemy":
            return 4
        if location_data["right"] == "enemy":
            return 2

    # Update base location
    initSig = robot.GetInitialSignal()
    xx = int(initSig[3:5])
    yy = int(initSig[5:7])
    location_data["base_corr"] = (xx,yy)

    # Perform type specific fucntion
    curSig = (robot.GetYourSignal() if len(robot.GetYourSignal()) >=8 else initSig)

    #If init signal is defender, activate defender function
    if (initSig[0] == "D"):
        out =  ActDefender(location_data, initSig)
        return out
    else:
        if (curSig[0] == "S"):
            out = ActScout(location_data, curSig)
            robot.setSignal(out[1])
            return out[0]
        else:
            #determine if attacker bot is close to enemy base. If it is, deploy all the virus that the base has
            if(isCloseTo(location_data["self_corr"], (int(curSig[8:10]), int(curSig[10:12])))):
                tot_virus = robot.GetVirus()
                robot.DeployVirus (tot_virus/2)

            #Otherwise, keep moving towards enemy base
            return (moveTowards(location_data["self_corr"], (int(curSig[8:10]), int(curSig[10:12]))))

def ActScout(location_data, sig):
"""
    Scout bot flowchart:
    1) Get coordinates of bot, base. Get dimensions of Map and current signal.
    2) Check if scouting has failed for the bot. If it has, change scouting type.
    3) Generate enemy base co-ordinates for each type of scouting bot.
    4) If bot is next to generated enemy base co-ordinates, check for two cases:
      .) If enemy-base is actually located next to bot, send co-ordinates to base.
      .) If enemy-base is not there at expected co-ordinates, fail this certain scouting case.
    5) Move towards enemy base if nothing interesting is happening((according to their Type).
"""

    # Get coordinates of bot, base. Get dimensions of Map and current signal.
    robx = location_data["self_cor"][0]
    roby = location_data["self_cor"][1]
    base_coorX = location_data["base_corr"][0]
    base_coorY = location_data["base_corr"][1]
    robx = location_data["self_cor"][0]
    roby = location_data["self_cor"][1]
    x_length = location_data["Map"][0]
    y_length = location_data["Map"][1]
    out = []

    # Check if scouting has failed for the bot. If it has, change scouting type.
    if sig[2] == "F":
        initSType = sig[1]
        newSType = (initSType + 1)%5
        newSignal = "S" + str(newSType) + "T" + sig[3:]

    #base could be at 5 possible places so I'm defining 5 types of robot for every base to search.
    #After defining Scout type we'll accordingly give enemy X and Y coordinates
    # and will write a same code for them with their corresponding position and their respective potential enemy coor
    if (sig[:2] == "S1"):
        enemyX=x_length-base_coorX+1
        enemyY=base_coorY
    if (sig[:2] == "S2"):
        enemyX=y_length-base_coorY+1
        enemyY=x_length-base_coorX+1
    if (sig[:2] == "S3"):
        enemyX=x_length-base_coorX+1
        enemyY=y_length-base_coorY+1
    if (sig[:2] == "S4"):
        enemyX=base_coorX
        enemyY=y_length-base_coorY+1
    if (sig[:2] == "S5"):
        enemyY=base_coorX
        enemyX=base_coorY

    # If found Enemy base then send signal to base
    if (location_data["up"] == 'enemy-base') :
       sig = (sig[:2] + "F" + sig[3:8] + "T" + f"{str(robx):02d}" + f"{str(roby+1):02d}")
       out = [0, sig]
       return out

    if (location_data["down"] == 'enemy-base') :
        sig = (sig[:2] + "F" + sig[3:8] + "T" + f"{str(robx):02d}" + f"{str(roby-1):02d}")
        out = [0, sig]
        return out

    if (location_data["left"] == 'enemy-base') :
        sig = (sig[:2] + "F" + sig[3:8] + "T" + f"{str(robx-1):02d}" + f"{str(roby-1):02d}")
        out = [0, sig]
        return out

    if (location_data["right"] == 'enemy-base') :
        sig = (sig[:2] + "F" + sig[3:8] + "T" + f"{str(robx+1):02d}" + f"{str(roby-1):02d}")
        out = [0, sig]
        return out

    if (location_data["nw"] == 'enemy-base') :
        sig = (sig[:2] + "F" + sig[3:8] + "T" + f"{str(robx-1):02d}" + f"{str(roby+1):02d}")
        out = [0, sig]
        return out

    if (location_data["ne"] == 'enemy-base') :
        sig = (sig[:2] + "F" + sig[3:8] + "T" + f"{str(robx+1):02d}" + f"{str(roby+1):02d}")
        out = [0, sig]
        return out

    if (location_data["se"] == 'enemy-base') :
        sig = (sig[:2] + "F" + sig[3:8] + "T" + f"{str(robx+1):02d}" + f"{str(roby-1):02d}")
        out = [0, sig]
        return out

    if (location_data["sw"] == 'enemy-base') :
        sig = (sig[:2] + "F" + sig[3:8] + "T" + f"{str(robx-1):02d}" + f"{str(roby-1):02d}")
        out = [0, sig]
        return out

    # Check if base is nearby, if not, fail scouting
    if(isCloseTo(location_data["self_cor"], (enemyX, enemyY))):
        sig = sig[:2] + "F" + sig[3:]
        out = [0, sig]
        return out

    # Scout if nothing interesting is happening
    out.append(moveTowards(location_data["self_cor"], (enemyX, enemyY)))
    out.append(sig)
    return out

def ActDefender(location_data, sig):
    #co-ordinates of the robot and home base
    robx = location_data["self_cor"][0]
    roby = location_data["self_cor"][1]
    base_coorX = int(sig[3:5])
    base_coorY = int(sig[5:7])
    x_length = location_data["Map"][0]
    y_length = location_data["Map"][1]

    #8 defender bots are arranged arounbase three units out.
    out = 0

    defendertype = int(sig[1])
    if defendertype == 1 :
        out = moveTowards(location_data["self_cor"], (base_coorX, base_coorY+3))
    elif defendertype == 2 :
        out = moveTowards(location_data["self_cor"], (base_coorX+3, base_coorY+3))
    elif defendertype == 3 :
        out = moveTowards(location_data["self_cor"], (base_coorX+3, base_coorY))
    elif defendertype == 4 :
        out = moveTowards(location_data["self_cor"], (base_coorX+3, base_coorY-3))
    elif defendertype == 5 :
        out = moveTowards(location_data["self_cor"], (base_coorX, base_coorY-3))
    elif defendertype == 6 :
        out = moveTowards(location_data["self_cor"], (base_coorX-3, base_coorY-3))
    elif defendertype == 7 :
        out = moveTowards(location_data["self_cor"], (base_coorX-3, base_coorY))
    elif defendertype == 8 :
        out = moveTowards(location_data["self_cor"], (base_coorX-3, base_coorY+3))

    return out

def ActBase(base):

"""
    Flowchart for a base:
    1) Get data about neighbouring cells.
    2) Check if there is an enemy near base and wreck it.
    3) Get list of all bot signals and perform comands.
"""


    enemy = ["enemy", "enemy-base"]
    friend = ["friend", "friend-base"]

    # Get data about neighbouring cells
    base_location_data = {}
    base_location_data["up"] = base.investigate_up()
    base_location_data["down"] = base.investigate_down()
    base_location_data["left"] = base.investigate_left()
    base_location_data["right"] = base.investigate_right()
    base_location_data["nw"] = base.investigate_nw()
    base_location_data["ne"] = base.investigate_ne()
    base_location_data["sw"] = base.investigate_sw()
    base_location_data["se"] = base.investigate_se()
    self_corr = (str(f"{base.GetPosition()[0]:02d}"), str(f"{base.GetPosition()[0]:02d}"))
    print("base at: " + str(base.GetPosition()[0]) + "," + str(base.GetPosition()[1]))

    # Check if there is an enemy near base and wreck it
    if ((base_location_data["up"] in enemy) + (base_location_data["down"] in enemy) + (base_location_data["left"] in enemy) + (base_location_data["right"] in enemy) + (base_location_data["ne"] in enemy) + (base_location_data["nw"] in enemy) + (base_location_data["se"] in enemy) + (base_location_data["sw"] in enemy)):
        base.DeployVirus((1200) if (base.GetVirus()>4800) else (base.GetVirus()/4))

    enemy_base_found = False
    enemy_base_corr = ("00","00")

    # Get list of all bot signals and perform commands
    sig_list = base.GetListOfSignals()

    if(base.GetElixir() > 400):
        #Check if scouts and defenders are alive or not. Check if enemy base has been found
        defCheck = set([1,2,3,4,5,6,7,8])
        scoCheck = set([1,2,3,4,5])
        defRead = []
        scoRead = []
        for s in sig_list:
            if(len(s)>=8):
                if (s[0] == "D"):
                        defRead.append(int(s[1]))
                elif (s[0] == "S"):
                    if(s[2] == "F"):
                        scoCheck.remove(int(s[1]))
                    if(s[7] == "T"):
                        enemy_base_found = True
                        enemy_base_corr[0] = s[8:10]
                        enemy_base_corr[1] = s[10:12]
                        base.SetYourSignal("A00" + self_corr[0] + self_corr[1] + "T" + enemy_base_corr[0] + enemy_base_corr[1])
                    scoRead.append(int(s[1]))
                else:
                    continue


        defCreate = defCheck - set(defRead)
        scoCreate = scoCheck - set(scoRead)
        for d in defCreate:
            base.create_robot("D" + str(d) + "0" + self_corr[0] + self_corr[1] + ("T" if enemy_base_found else "F") + enemy_base_corr[0] + enemy_base_corr[1])
        for sc in scoCreate:
            base.create_robot("S" + str(sc) + "T" + self_corr[0] + self_corr[1] + ("T" if enemy_base_found else "F") + enemy_base_corr[0] + enemy_base_corr[1])

        # If enemy base is found, deploy a lot of attackers
        if(enemy_base_found):
            while(base.GetElixir()>400):
                base.create_robot("A00" + self_corr[0] + self_corr[1] + "T" + enemy_base_corr[0] + enemy_base_corr[1])
    return
    """
