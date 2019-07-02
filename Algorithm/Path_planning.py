#initialising lists and variables

bot_ini_pos = [[0,0,0]]    #to be provided by localization team in format (x_coord,y_coord,0). Bots then sorted according to priority
bot_final_pos = [[2,5]]  #calculated using dynamic allocation of setpoints (x_coord,y_coord)
all_path = []   #list containing paths of all bots
path = []   #list to store path of each bot
t=0     #time co-ordinate
z=0     #counter for traversing through next_options list
i=0     #counter for traversing through co-ordinate info. of each bot
g=0     #cost reqd. to get to particular node
h=0     #heuristic
f=0     #f=g+h
p=0     #counter for adding extra obstacles to avoid head on collision
f_min=0 #optimal next movement
total_bots = 1
obs_len = 0
obstacles = []  #list for adding obstacles to bots
avoid_crossing = [] #list to avoid head on collision. Appended to obstacles
reject = 0  # checking if a particular node is available for movement
debug=0
while(i<total_bots):
    
    #take particular bot information
    start_node = bot_ini_pos[i]
    print(start_node)
    end_node = bot_final_pos[i]
    print(end_node)
    x_end = end_node[0]
    y_end = end_node[1]
    curr_node = start_node
    x = curr_node[0]
    y = curr_node[1]
    #print("1") for debugging
    
    while x!= end_node[0] and y!= end_node[1]: #checking that goal has not been reached
        x = curr_node[0]
        y = curr_node[1]
        next_options = [[x,y],[x+1,y+1],[x-1,y+1],[x-1,y-1],[x+1,y-1],[x+1,y],[x-1,y],[x,y-1],[x,y+1]]#possible spaces to move ignoring time co-ordinate
        g=g+1#bot can travel only one unit in one unit of time
        obs_len = len(obstacles)

        #print(1) for debugging this loop
        
        while(z<=7):#checking best possible next option
            #print(1) for debugging
            while(obs_len>0):#checking that next_move is not in the obstacle list
                if next_options[z][0] == obstacles[obs_len][0] and next_options[z][1] == obstacles[obs_len][1]:
                    reject = 1
                obs_len = obs_len-1
                       
            if reject == 0 :            
                poss_x = next_options[z][0]
                poss_y = next_options[z][1]
                h = max(abs(x_end-poss_x),abs(y_end-poss_y))#calculation of heuristic
                f=g+h
                if z==0: #checking best next node
                    f_min = f
                    #z=z+1

                elif z!=0:
                    if f<f_min:
                        f_min = f
                        curr_node[0] = next_options[z][0]#current node of bot
                        curr_node[1] = next_options[z][1]
                        #z=z+1
            elif reject == 1:
                #z=z+1
                debug=1
            z=z+1    
            # print(z)
        t=t+1    
        curr_node[2] = curr_node[2] + t#adding time co-ordinate to bot
        z=0
        path.append(curr_node)
        print(path)
        curr_node[2]=0
    all_path.append(path)
    

    #adding obstacles according to priority . The ith path is now declared as an obstacle for the remaining bots
    
    obstacles.append(all_path[i])
    avoid_crossing = all_path[i]#adding list for avoiding head on collisions
    p = len(all_path[i])-1
    while(p>=0):#incrementing time co ordinate
        avoid_crossing[p][2] = avoid_crossing[p][2] + 1
        p = p-1

    obstacles.append(avoid_crossing)#final obstacle list
    #reinitialising the parameters for the next bot
    path = []
    i = i+1
    f=0
    g=0
    h=0
    reject = 0
    t=0
    z=0
    f_min = 0
    print("1")
    
#Printing all paths
#bot_num = 1
#while(bot_num-1>=0):
    #print("The respective path of bot_number" + bot_num + "is :" + all_path[bot_num])
   
    #bot_num = bot_num - 1
print(all_path)
