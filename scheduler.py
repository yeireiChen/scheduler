import operator

def _tasaSimpleAlgorithms(motes, local_q, edges, max_assignable_slot, start_offset, max_assignable_channel):

    reSentCount = 2
    endSlot = {}
    result = []
    edge_relation = {}
    global_q = {}
    children = {}
    leaf = list()
    level = {}

    #prepare data
    for relation in edges:
        edge_relation[relation['u']] = relation['v']
        global_q[relation['u']] = local_q[relation['u']]
        children[relation['v']] = list()    #initialize children, then produce later

    #get childrens
    for child in edges:
        if children[child['v']] != None:
            children[child['v']].append(child['u'])


    #get leafs
    parent = children.keys()
    for item in edges:
        if item['u'] not in parent:
            leaf.append(item['u'])

    #get root
    childTemp = edge_relation.keys()
    parentTemp = children.keys()
    for i in range(0,parentTemp.__len__(),1):
        if parentTemp[i] not in childTemp:
            root = parentTemp[i]

    print "root is ",root

    #get topology level
    levelCount=0
    tempCount=0
    for leafs in leaf:
        now_parent = edge_relation[leafs]
        tempCount+=1
        while(now_parent!=root):
            now_parent = edge_relation[now_parent]
            tempCount+=1
            if(tempCount>levelCount):
                levelCount = tempCount

        tempCount=0

    print "MaxLevel is ",levelCount

    #getNode's level
    for i in range(1,levelCount+1):
        level[i] = list()
    counter=0
    for node in edge_relation.keys():
        now_parent = edge_relation[node]
        counter+=1
        while(now_parent!=root):
            now_parent = edge_relation[now_parent]
            counter+=1
        level[counter].append(node)
        counter=0

    print "node level is",level
    print level.__len__()





    #produce global queue
    for nodes in edge_relation:
        now = nodes
        number = local_q[now]
        while now != root:
            #calculate global_q
            if edge_relation[now] != root:
                global_q[edge_relation[now]]+=number
                now=edge_relation[now]
            else:
                break

    #get biggest global_q
    sorted_x = sorted(global_q.items(), key=lambda x:(x[1],x[0]), reverse=True)

    #prepare to schedule
    cant_list = []  #check
    temp = 0

    for slotOffset in range(start_offset, start_offset + max_assignable_slot):
        for channelOffset in range(0,max_assignable_channel,1):#max_assignable_channel
            node_pick = ''
            for check in sorted_x:
                if check[0] not in cant_list and local_q[check[0]] != 0:
                    temp = [k for k, v in global_q.iteritems() if v == global_q[check[0]] and k not in cant_list] #get keys by value
                    if temp.__len__() == 1:
                        node_pick = temp[0]
                    else:
                        temp.sort()
                        localTemp = []
                        for localQ in temp:
                            if local_q[localQ] != 0:
                                localTemp.append((localQ,local_q[localQ]))

                        temper = sorted(sorted(localTemp, key = lambda x : x[0]), key = lambda x : x[1], reverse = True)#sort x[1], if same,then sort x[0]
                        node_pick = temper[0][0]

                    #find node that can't schedule
                    #child_list
                    if node_pick in children.keys():
                        for tempCheck in children[node_pick]:
                            if tempCheck not in cant_list:
                                cant_list.append(tempCheck)
                    #parent
                    tempParent = edge_relation[node_pick]
                    if tempParent not in cant_list and tempParent != root:
                        cant_list.append(tempParent)
                    #parent's child_list
                    tempChildren = edge_relation[node_pick]
                    for tempCheck in children[tempChildren]:
                        if tempCheck not in cant_list:
                            cant_list.append(tempCheck)

                    #record sheduled information
                    result.append([node_pick,tempParent,slotOffset,channelOffset])

                    #calculate lq & gq
                    local_q[node_pick]-=1
                    global_q[node_pick]-=1
                    #parent's local plus 1 and global is same
                    if edge_relation[node_pick] != root:
                        calParentNode = edge_relation[node_pick]
                        local_q[calParentNode]+=1

                    break # one cell only one, temporally

            if (node_pick == ''):
                temp = channelOffset-1
                break

        endSlot[slotOffset] = temp

        #clear  schedule_list & cant_list
        del cant_list[:]

        #clean sorted_x and reSorted sorted_x and delete if gq = 0
        del sorted_x[:]
        sorted_temp = sorted(global_q.items(), key=operator.itemgetter(1), reverse=True)
        for prepareIn in sorted_temp:
            if prepareIn[1] != 0:
                sorted_x.append(prepareIn)

        if not sorted_x:#empty means all scheduled
            break;

    print "=============================="
    resultFormat =[]
    print "endSlot is ",endSlot,endSlot.__len__()
    print "level is ",level,level.__len__()
    print "result is ",result

    print "=============================="

    if sorted_x:
        return False,result
    else:
        return  True,result





motes_o = ["0001", "0002", "0003", "0004", "0005"]    #list
local_o = {'0002':1,'0003':1,'0004':1,'0005':1}
edge_o = [{"u": "0002", "v": "0001"},  #dic in list        u_from  v_to
         {"u": "0003", "v": "0002"},
          {"u": "0005", "v": "0004"},
          {"u": "0004", "v": "0001"}, ]          #RPL data information

motes_type01 = ["0000","0001","0002","0003","0004","0005","0006","0007","0008"]
local_type01 = {
                '0000':1,
                '0001':1,
                '0002':1,
                '0003':1,
                '0004':1,
                '0005':1,
                '0006':1,
                '0007':1,
                '0008':1,
                }
edge_type01 = [
            {"u": "0008", "v": "0004"},
            {"u": "0007", "v": "0003"},
            {"u": "0006", "v": "0003"},
            {"u": "0005", "v": "0002"},
            {"u": "0004", "v": "0001"},
            {"u": "0003", "v": "0001"},
            {"u": "0002", "v": "0000"},
            {"u": "0001", "v": "0000"},]


max_assignable_slot_o = 30
max_assignable_channel_o = 30
start_offset_o = 4    #4-8

#can_scheduled,results_type01 = _tasaSimpleAlgorithms(motes_type01,local_type01, edge_type01, max_assignable_slot_o, start_offset_o, max_assignable_channel_o)
can_scheduled,results_type02 = _tasaSimpleAlgorithms(motes_type01,local_type01, edge_type01, max_assignable_slot_o, start_offset_o, max_assignable_channel_o)


print "=============================="
if can_scheduled:
    print "enough"
else:
    print "not enough"

print "=============================="
print "| From |  To  | Slot | Chan |"
for item in results_type02:
    print "| {0:4} | {1:4} | {2:4} | {3:4} |".format(item[0][-4:], item[1][-4:], item[2], item[3])  #--4_string last 4 char
print "=============================="

asd = []
for i in range(0,60):
    new = []
    for j in range(0,60):
        new.append(0)
    asd.append(new)

for nn in results_type02:
    c = nn[0][-2:] +"-"+ nn[1][-2:]
    asd[nn[3]][nn[2]] = c

print "|   ",
for ss in range (start_offset_o,start_offset_o+max_assignable_slot_o):
    print "| {0:5}".format(ss),
print "|"

for ii in range(0,6):#max_assignable_channel_o
    print "| {0:2}".format(ii),  #--4_string last 4 char
    for ss in range (start_offset_o,start_offset_o+max_assignable_slot_o):
        print "| {0:5}".format(asd[ii][ss]),
    print "|"
