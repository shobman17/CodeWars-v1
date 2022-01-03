from random import randint


def ActRobot(robot):
        # if robot.GetVirus() > 1000:
        #         robot.DeployVirus(200)       
        cnt = 0
        # if robot.investigate_up()=='enemy':
        #         cnt+=1
        # if robot.investigate_down()=='enemy':
        #         cnt+=1

        cnt = int(robot.investigate_up()=='enemy') + int(robot.investigate_down()=='enemy') + int(robot.investigate_left()=='enemy') + int(robot.investigate_right()=='enemy') + int(robot.investigate_nw()=='enemy') + int(robot.investigate_ne()=='enemy') + int(robot.investigate_sw()=='enemy') + int(robot.investigate_se()=='enemy')

        if cnt >= 6:
                robot.DeployVirus(400)       
        elif cnt >= 3:
                robot.DeployVirus(300)       
        else :
                robot.DeployVirus(100)                               


        init_signal = robot.GetInitialSignal()
        if init_signal.find('defender')!=-1:
                base_x = int(init_signal[8:10])
                base_y = int(init_signal[10:])
                x,y = robot.GetPosition()
                if x > base_x:
                        return 4        
                if x < base_x:
                        return 2
                if y > base_y:
                        return 1        
                if y < base_y:
                        return 3                                
                if x == base_x and y == base_y:
                        return randint(1,4) 
        if init_signal.find('attacker')!=-1:
                base_x = int(init_signal[8:10])
                base_y = int(init_signal[10:])
                x,y = robot.GetPosition()

                if robot.investigate_up()=='friend-base':
                        return 3
                if robot.investigate_down()=='friend-base':
                        return 1
                if robot.investigate_left()=='friend-base':
                        return 2
                if robot.investigate_right()=='friend-base':
                        return 4
                return randint(1,4)                                        
        return randint(1,4)


def ActBase(base):
    '''
    Add your code here
    
    '''
    enemy = ["enemy", "enemy-base"]
    base_location_data = {}
    base_location_data["up"] = base.investigate_up()
    base_location_data["down"] = base.investigate_down()
    base_location_data["left"] = base.investigate_left()
    base_location_data["right"] = base.investigate_right()
    base_location_data["nw"] = base.investigate_nw()
    base_location_data["ne"] = base.investigate_ne()
    base_location_data["sw"] = base.investigate_sw()
    base_location_data["se"] = base.investigate_se()

    if ((base_location_data["up"] in enemy) + (base_location_data["down"] in enemy) + (base_location_data["left"] in enemy) + (base_location_data["right"] in enemy) + (base_location_data["ne"] in enemy) + (base_location_data["nw"] in enemy) + (base_location_data["se"] in enemy) + (base_location_data["sw"] in enemy)):
        base.DeployVirus((base.GetVirus()/4))  #About 250
    if base.GetElixir() > 500:
            p = randint(0,5)
            if p != 0:
                x,y = base.GetPosition()    
                msg_x = str(x)
                msg_y = str(y)
                if x < 10:
                        msg_x = '0' + msg_x
                if y < 10:
                        msg_y = '0' + msg_y 
                base.create_robot('attacker'+msg_x+msg_y)
            else :
                x,y = base.GetPosition()    
                msg_x = str(x)
                msg_y = str(y)
                if x < 10:
                        msg_x = '0' + msg_x
                if y < 10:
                        msg_y = '0' + msg_y        
                base.create_robot('defender' + msg_x + msg_y)            
    return