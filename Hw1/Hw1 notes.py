import math
import numpy
import string

'''
1) 10 features to distinguish a junk email
    1) Some sort of hyper link - extract it though the email by looking for a hyperlink/website URL
    2) Capitialization of common words - use a parser to go through the text and count the common words which are normally mis-spelled, like "i" being "I". 
        this informtion can be used in tandem with others to point out a robot type text.
    3) Email Address - Get this information from the metadata/email. This information can be used to compare it with recent email addresses of people you have been talking with
    4) Type of Email/Subject - Read the beginning of the email/Subject line to see what the inqury is about. With this information you can determine if it is a job offer/credit card sale/ deal of some sort
    5) Phone Number - Parse through information and look for requesting phone number or listing one to call. This information can be used to look for a phishing typw email that is just trying to get your number
    6) Spelling - Parse through the email and look at the spelling of the organizations/Key words - Common junk/spam emails will mis-spell a key word like "Washington State Universtiy"
    7) Ownership - Parse through the email and look for words/phrases that contain things like "your site/ your Company". This paried with an unfamiliar email is a clear sign of spam
    8) Greeting - Parse through the email and check the greeting statement. Normal emais will tend to address you by name or by some name, if its not then could be a sign of spam/junk
    9) Signature - Parse through the email and look for the signature at the end if its from some company and check for a phone number/email/contact information. Paried with other attributes this could be a signifying attribute of spam/junk
    10) Mass Email - Check the cc/recipients of the email. If there is a large amount of people recieving this email it could be junk/spam.
    
2) 10 feature to distinguish fraudulent or legitimate charges

    1) Recurring charges
    2) Location of charge
    3) Company charging the card
    4) frequency of charges of card
    5) Location relative to past purchases 
    6) Currency Charged
    7) Amount charged
    8) Type of transaction used
    9) Was there a signature
    10) Receipt
    
    
3) Error over training set provides what type of estimate?
optismistically-biased estimate, because as you use the training set more and more the error you get will decrease in the true error


'''

#x = -((p+)log2(p+)) - ((p-)log2(p-))           <------- ENTROPY equation


#target value y/n = 5/10

#color (for yes, p+)y/n = red(5) = 3/10 yellow(5) = 2/10
#type (p+) y/n = sports(6) = 4/10 SUV(4) = 1/10
#origin (p+)y/n = domestic(5) = 2/10 Imported (5) = 3/10



 #math.log2(p)   <-- how to call log for entropy equation
# - ( (9/14)*math.log2(9/14) ) - ( (5/14)*math.log2(5/14) ) = .94  E(9/14,5/14)
#a = - ( (5/10)*math.log2(5/10) ) - ( (5/10)*math.log2(5/10) )          <---- Entropy of data = 1.0
#               E               E(red)                              +               E(yellow)
#Gain(color) = 1.0 - [(5/10)*( (- ( (3/5)*log2(3/5) ) - ( (2/5)*log2(2/5) ) ] + [ (5/10)*( (- ( (2/5)*log2(2/5) ) - ( (3/5)*log2(3/5) ) ]

#b = 1.0 - ((5/10) * (-(3/5) * math.log2(3/5)) - ((2/5) * math.log2(2/5)) + (5/10) * (-(2/5)*math.log2(2/5)) - ((3/5)* math.log2(3/5) ))

red = - ( (3/5)*math.log2(3/5) ) - ( (2/5)*math.log2(2/5) )
yellow = - ( (2/5)*math.log2(2/5) ) - ( (3/5)*math.log2(3/5) )

red_yellow = (5/10) * red + (5/10) * yellow

sports = - ( (4/6)*math.log2(4/6) ) - ( (2/6)*math.log2(2/6) )

SUV = - ( (1/4)*math.log2(1/4) ) - ( (3/4)*math.log2(3/4) )

sports_SUV = (6/10) * sports + (4/10) * SUV

domestic = - ( (2/5)*math.log2(2/5) ) - ( (3/5)*math.log2(3/5) )

imported = - ( (3/5)*math.log2(3/5) ) - ( (2/5)*math.log2(2/5) )

domestic_imported = (5/10) * domestic + (5/10) * imported

s_red = - ( (3/4)*math.log2(3/4) ) - ( (1/4)*math.log2(1/4) )

s_yellow = - ( (1/2)*math.log2(1/2) ) - ( (1/2)*math.log2(1/2) )

s_color = (4/6) * s_red + (2/6) * s_yellow
s_origin = (4/6) * s_yellow + (2/6) * 0


'''
                            type                        L/R => Sports/SUV
                origin                  Color       L/R => Domestic/Imported... => yellow/red
        Color       yes         Origin          no      L/R => Red/Yellow... Imported/Domestic
    yes     no                yes     no
    
    
Red Domestic SUV: Based off training data would be classified as NOT stolen... NO  
    
'''



ID = [1,2,3,4,5,6,7,8,9,10]
Color = ["red","red","red","yellow","yellow","yellow","yellow","yellow","red","red"]
Type = ["Sports","Sports","Sports","Sports","Sports","SUV","SUV","SUV","SUV","Sports"]
Origin = ["Domestic","Domestic","Domestic","Domestic","Imported","Imported","Imported","Domestic","Imported","Imported"]
Stolen = [1,0,1,0,1,0,1,0,0,1]

def Entropy(f1,f2):
    if(f1 == 0 or f2 == 0):
        return 0
    else:
        ent = - ((f1) * math.log2(f1)) - ((f2) * math.log2(f2))
        return ent
def Gain(en,f1,f2,f3,f4,f5,f6):
    gain = en - (f1 * Entropy(f2,f3) + f4 * Entropy(f5,f6))
    #print(gain)
    return gain

class node:
    def __init__(self):
        self.left = None
        self.right = None
        self.cars = []
        self.attribute = None
        self.entropy = None
        self.used = []
        self.leaf = None
        self.left_attribute = None
        self.right_attribute = None

    def getyes(self):
        yes = 0
        for number in self.cars:
            if (automobile[number][3] == 1):  # The car is stolen if it equals 1
                yes = yes + 1
        #if (yes == self.cars.__sizeof__()):  # there is 100%% yes
         #   return 1

        return yes / len(self.cars)

    def gain(self, index): #retrieves f1(fraction of attribute), f2(yes ratio from first attribute), f4(fraction of attribute),f5(yes ratio from second attribute)
        atr1 = '' #feature1
        atr2 = '' #feature2
        a1 = 0 #count of attribute1
        a2 = 0 #count of attribute2
        yes1 = 0 #stores yes for feature1
        yes2 = 0 #stores yes for feature2
        car_count = 0;

        print('self.cars = ', self.cars)
        for car in self.cars:
            car_count = car_count + 1
            #print('1)looking at', automobile[car][0], automobile[car][1], automobile[car][2], automobile[car][3])
            if(atr1 == ''): #set attribute1
                atr1 = automobile[car][index]  # setting first attribute value and recording stolen
                #print('atr1' , atr1)
                #self.left_attribute = atr1
                a1 = a1 + 1
                #print('set first attribute', atr1)
                if automobile[car][3] == 1: #car is stolen and record for attribute1
                    yes1 = yes1 + 1
            elif(atr1 != '' and atr1 != automobile[car][index] and atr2 == ''): #setting attribute2 to and recording value
                atr2 = automobile[car][index] #set attribute2
               # print('atr2', atr2)
                #self.right_attribute = atr2
                a2 = a2 + 1
                #print('set second attribute', atr2)
                if automobile[car][3] == 1: #attribute2 car is stolen
                    yes2 = yes2 + 1
            #run through rest of array
            else:
                if automobile[car][index] == atr1: #its the first feature
                    #print('first feature')
                    a1 = a1 + 1
                    if automobile[car][3] == 1: #check if stolen
                        yes1 = yes1 + 1
                else: #its attribute2
                    #print('second feature')
                    a2 = a2 + 1
                    if automobile[car][3] == 1: #checking for stolen
                        yes2 = yes2 + 1
            #yes1,yes2 hold the total yes for each feature. return yes/len(self.cars)
        print('yes1=',yes1,'a1=',a1,'yes2=',yes2,'a2=',a2,'self.entropy',self.entropy,'car_count',car_count)
        f11 = a1 / car_count#attribute1 chance,
        f12 = yes1 / a1 #setting yes chance for attribute1
        f13 = 1 - f12 #setting the no chance for attribute1
        f14 = a2 / car_count #attribute2 chance
        f15 = yes2 / a2  # setting yes chance for attribute2
        f16 = 1 - f15  # setting the no chance for attribute2
        print(f11,f12,f13,f14,f15,f16)
        if f16 == 0 or f15 == 0:
            return self.entropy - (f11 * Entropy(f12, f13) + f14 * 0)
        if f13 == 0 or f12 == 0:
            return self.entropy - (f11 * 0 + f14 * Entropy(f15,f16))
        print('total entropy = ' ,f11 * Entropy(f12,f13) + f14 * Entropy(f15,f16))
        return self.entropy - (f11 * Entropy(f12,f13) + f14 * Entropy(f15,f16))


automobile = []

def main():
    gainmax = []
    print("starting main")
    for id in ID:  # for loop to go through the training data// reading the cars information into an arrary of cars
        automobile.append((Color[id - 1], Type[id - 1], Origin[id - 1], Stolen[id - 1]))
    root = node()
    print("created root node")
    print("setting root node cars to all of them")
    for x in range(0,10): #setting roots cars to 0-9 so it can access all the cars
        root.cars.append(x)
    print(root.cars)
    if(root.getyes() < 1 and root.getyes() > 0): #the current node has entropy
        print("setting entropy of current node")
        f1 = root.getyes()
        f2 = 1 - f1
        print('f1 = ', f1, 'f2 = ', f2)
        e = Entropy(f1,f2) #e = entropy of the current node
        root.entropy = e #setting node's entropy
        print(root.entropy)
        length = len(automobile[0]) - 1 #lenngth of tuple -1 to get ride of target feature
        for x in range(length): #running through all attributes to determine max gain and thus attribute to label this node
            print('root.gain()',x)
            print(root.gain(x))
            gainmax.append(root.gain(x)) #passing in gain(x) where x is an integer that will eb used to index into a tuple to read values
    print('done with setting gainmax')
    print(gainmax)
    Max = gainmax[0]
    used_index = 0
    for x in range(len(gainmax)):
        if gainmax[x] > Max:
            Max = gainmax[x]
            used_index = x
    print('0 = color, 1 = type, 2 = origin, used_index =',used_index)
    #set the attribute of the node, and update the used attribute of the node
    root.attribute = used_index
    root.used.append(used_index)
    dim1 = ''
    dim2 = ''
    for x in root.cars:
        if dim1 == '':
            dim1 = automobile[x][used_index]
        elif automobile[x][used_index] != dim1:
            dim2 = automobile[x][used_index]
    root.left_attribute = dim1
    root.right_attribute = dim2
    #root is created at this point. time to create the rest of the tree.

    pcur = root

    leftnode = node()  # create node for the cars sorted
    pcur.left = leftnode  # assign parnent node to child here
    rightnode = node()
    pcur.right = rightnode
    leftnode.used.append(pcur.attribute)  # passing attribute to new node
    rightnode.used.append(pcur.attribute)  # passing attribute to new node
    for x in pcur.cars:  # sorting cars into new nodes based off attribute assigned
        print(pcur.left_attribute, pcur.right_attribute)
        print(automobile[x][pcur.attribute])
        if automobile[x][pcur.attribute] == pcur.left_attribute:  # put into left tree
            print('put left tree')
            leftnode.cars.append(x)  # adding a sorted car based off pnode.left_attribute

        else:  # put into right tree
            print('put right tree')
            rightnode.cars.append(x)
    root = pcur #Reassign root to pcur to apply the changes to root.
    #FIRST NODE COMPLETED AND PASSED ALL INFORMATION TO CHILDREN LEFT AND RIGHT

    #working with the left node
    pcur = root.left
    gainmax = []
    f1 = pcur.getyes()
    f2 = 1 - f1
    print('f1 = ', f1, 'f2 = ', f2)
    e = Entropy(f1, f2)  # e = entropy of the current node
    pcur.entropy = e  # setting node's entropy
    gainmax.append(pcur.gain(0)) #gain of color
    gainmax.append(0)
    gainmax.append(pcur.gain(2))  # gain of origin

    print('done with setting gainmax of pL node')
    print(gainmax)
    Max = gainmax[0]
    used_index = 0
    for x in range(len(gainmax)):
        if gainmax[x] > Max:
            Max = gainmax[x]
            used_index = x
    print('0 = color, 1 = type, 2 = origin, used_index =', used_index)
    pcur.attribute = used_index
    pcur.used.append(used_index)
    dim1 = ''
    dim2 = ''
    for x in root.cars:
        if dim1 == '':
            dim1 = automobile[x][used_index]
        elif automobile[x][used_index] != dim1:
            dim2 = automobile[x][used_index]
    pcur.left_attribute = dim1
    pcur.right_attribute = dim2
    print(pcur.left_attribute, pcur.right_attribute,pcur.used)

    #pnode = pL

    leftnode = node()  # create node for the cars sorted
    pcur.left = leftnode  # assign parnent node to child here
    rightnode = node()
    pcur.right = rightnode
    leftnode.used.append(pcur.attribute)  # passing attribute to new node
    rightnode.used.append(pcur.attribute)  # passing attribute to new node
    for x in pcur.cars:  # sorting cars into new nodes based off attribute assigned
        print(pcur.left_attribute, pcur.right_attribute)
        print(automobile[x][pcur.attribute])
        if automobile[x][pcur.attribute] == pcur.left_attribute:  # put into left tree
            print('put left tree')
            leftnode.cars.append(x)  # adding a sorted car based off pnode.left_attribute

        else:  # put into right tree
            print('put right tree')
            rightnode.cars.append(x)

    #pcur is created and passed through ROOT2 completed
    print(pcur.attribute,pcur.used,pcur.cars)
    root2 = pcur

#finishing left most attribute... root 3
    pcur = root2.left
    gainmax = []
    f1 = pcur.getyes()
    f2 = 1 - f1
    print('f1 = ', f1, 'f2 = ', f2)
    e = Entropy(f1, f2)  # e = entropy of the current node
    pcur.entropy = e  # setting node's entropy
    gainmax.append(pcur.gain(0))  # gain of color
    gainmax.append(0)
    gainmax.append(0)  # gain of origin

    print('done with setting gainmax of pL node')
    print(gainmax)
    Max = gainmax[0]
    used_index = 0
    for x in range(len(gainmax)):
        if gainmax[x] > Max:
            Max = gainmax[x]
            used_index = x
    print('0 = color, 1 = type, 2 = origin, used_index =', used_index)
    pcur.attribute = used_index
    pcur.used.append(used_index)
    dim1 = ''
    dim2 = ''
    for x in root.cars:
        if dim1 == '':
            dim1 = automobile[x][used_index]
        elif automobile[x][used_index] != dim1:
            dim2 = automobile[x][used_index]
    pcur.left_attribute = dim1
    pcur.right_attribute = dim2
    print(pcur.left_attribute, pcur.right_attribute, pcur.used)

    leftnode = node()  # create node for the cars sorted
    pcur.left = leftnode  # assign parnent node to child here
    rightnode = node()
    pcur.right = rightnode
    leftnode.used.append(pcur.attribute)  # passing attribute to new node
    rightnode.used.append(pcur.attribute)  # passing attribute to new node
    for x in pcur.cars:  # sorting cars into new nodes based off attribute assigned
        print(pcur.left_attribute, pcur.right_attribute)
        print(automobile[x][pcur.attribute])
        if automobile[x][pcur.attribute] == pcur.left_attribute:  # put into left tree
            print('put left tree')
            leftnode.cars.append(x)  # adding a sorted car based off pnode.left_attribute

        else:  # put into right tree
            print('put right tree')
            rightnode.cars.append(x)

    #pcur is created and passed through ROOT2 completed
    print(pcur.attribute,pcur.used,pcur.cars)
    print(pcur.left.cars, pcur.right.cars)
    root3 = pcur

#building right side of the tree now
    print('building root 4')
    pcur = root.right
    gainmax = []
    f1 = pcur.getyes()
    f2 = 1 - f1
    print('f1 = ', f1, 'f2 = ', f2)
    e = Entropy(f1, f2)  # e = entropy of the current node
    pcur.entropy = e  # setting node's entropy
    gainmax.append(pcur.gain(0))  # gain of color
    gainmax.append(0)
    gainmax.append(pcur.gain(2))  # gain of origin

    print('done with setting gainmax of pL node')
    print(gainmax)
    Max = gainmax[0]
    used_index = 0
    for x in range(len(gainmax)):
        if gainmax[x] > Max:
            Max = gainmax[x]
            used_index = x
    print('0 = color, 1 = type, 2 = origin, used_index =', used_index)
    pcur.attribute = used_index
    pcur.used.append(used_index)
    dim1 = ''
    dim2 = ''
    for x in root.cars:
        if dim1 == '':
            dim1 = automobile[x][used_index]
        elif automobile[x][used_index] != dim1:
            dim2 = automobile[x][used_index]
    pcur.left_attribute = dim1
    pcur.right_attribute = dim2
    print(pcur.left_attribute, pcur.right_attribute, pcur.used)

    # pnode = pL

    leftnode = node()  # create node for the cars sorted
    pcur.left = leftnode  # assign parnent node to child here
    rightnode = node()
    pcur.right = rightnode
    leftnode.used.append(pcur.attribute)  # passing attribute to new node
    rightnode.used.append(pcur.attribute)  # passing attribute to new node
    for x in pcur.cars:  # sorting cars into new nodes based off attribute assigned
        print(pcur.left_attribute, pcur.right_attribute)
        print(automobile[x][pcur.attribute])
        if automobile[x][pcur.attribute] == pcur.left_attribute:  # put into left tree
            print('put left tree')
            leftnode.cars.append(x)  # adding a sorted car based off pnode.left_attribute

        else:  # put into right tree
            print('put right tree')
            rightnode.cars.append(x)
    print(pcur.left.cars, pcur.right.cars)
    root4 = pcur
#finishing the tree creation last root section
    print('root 5 is being created here')
    pcur = root4.right
    print(pcur.cars)
    gainmax = []
    f1 = pcur.getyes()
    f2 = 1 - f1
    print('f1 = ', f1, 'f2 = ', f2)
    e = Entropy(f1, f2)  # e = entropy of the current node
    pcur.entropy = e  # setting node's entropy
    gainmax.append(0)  # gain of color
    gainmax.append(0)
    gainmax.append(pcur.gain(2))  # gain of origin

    print('done with setting gainmax of pL node')
    print(gainmax)
    Max = gainmax[0]
    used_index = 0
    for x in range(len(gainmax)):
        if gainmax[x] > Max:
            Max = gainmax[x]
            used_index = x
    print('0 = color, 1 = type, 2 = origin, used_index =', used_index)
    pcur.attribute = used_index
    pcur.used.append(used_index)
    dim1 = ''
    dim2 = ''
    for x in root.cars:
        if dim1 == '':
            dim1 = automobile[x][used_index]
        elif automobile[x][used_index] != dim1:
            dim2 = automobile[x][used_index]
    pcur.left_attribute = dim1
    pcur.right_attribute = dim2
    print(pcur.left_attribute, pcur.right_attribute, pcur.used)

    # pnode = pL

    leftnode = node()  # create node for the cars sorted
    pcur.left = leftnode  # assign parnent node to child here
    rightnode = node()
    pcur.right = rightnode
    leftnode.used.append(pcur.attribute)  # passing attribute to new node
    rightnode.used.append(pcur.attribute)  # passing attribute to new node
    for x in pcur.cars:  # sorting cars into new nodes based off attribute assigned
        print(pcur.left_attribute, pcur.right_attribute)
        print(automobile[x][pcur.attribute])
        if automobile[x][pcur.attribute] == pcur.left_attribute:  # put into left tree
            print('put left tree')
            leftnode.cars.append(x)  # adding a sorted car based off pnode.left_attribute

        else:  # put into right tree
            print('put right tree')
            rightnode.cars.append(x)
    root5 = pcur
    print(root.left.cars, root.right.cars)
    print(root2.left.cars, root2.right.cars)
    print(root3.left.cars, root3.right.cars)
    print(root4.left.cars, root4.right.cars)
    print(root5.left.cars, root5.right.cars)
    root2.left = root3
    root4.right = root5
    root.left = root2
    root.right = root4
    print(root.left.left.left.cars)
    print(root.right.right.cars)

    test = input()

    print(test)
    featur = test.split()
    for x in featur:
        print(x)

    pcur = root
    if(featur[2] == pcur.left_attribute):
        pcur = pcur.left
        if featur[1] == pcur.left_attribute:
            pcur = pcur.left
            if(featur[0] == pcur.left_attribute):
                pcur = pcur.left
                return automobile[pcur.cars.pop()][3]
            else:
                pcur = pcur.right
                return automobile[pcur.cars.pop()][3]


        else: #going right
            pcur = pcur.right
            return automobile[pcur.cars.pop()][3]

    else: #going right
        pcur = pcur.right
        if featur[0] == pcur.left_attribute:
            pcur = pcur.left
            return automobile[pcur.cars.pop()][3]

        else:
            pcur = pcur.right
            if featur[1] == pcur.left_attribute:
                pcur = pcur.left
                return automobile[pcur.cars.pop()][3]
            else:
                pcur = pcur.right
                return automobile[pcur.cars.pop()][3]

    print('1 = stolen 0 = not stolen')
#Tree is created at this point!!!!!









