import sys
from os import system

class Person:
    def __init__(self,name,gndr):
        self.name=name
        self.gender=gndr

class Male(Person):
    def __init__(self,name):
        Person.__init__(self,name,"Male")
        self.husbandOf=None
        self.sonOf=None             
    
class Female(Person):
    def __init__(self,name):
        Person.__init__(self,name,"Female")
        self.wifeOf=None
        self.daughterOf=None        
        self.children=list()        

#initiating Queen Anga and King Shan as root
def initiateRoot(root,husbandName,wifeName):
    husband=Male(husbandName)
    wife=Female(wifeName)
    husband.husbandOf = wife
    wife.wifeOf = husband
    return wife

#returns pointer of the node corresponding to personName
def findPerson(root,personName):
    if root == None:
        return None
    else:
        if root.name == personName:
            return root
        else:
            if root.gender == "Female":
                if root.wifeOf != None:
                    if root.wifeOf.name==personName:
                        return root.wifeOf
            else:
                if root.husbandOf == None:
                    return None
                else:
                    root = root.husbandOf
                    if root.name == personName:
                        return root
            
            if len(root.children)==0:
                    return None
            else:
                for x in root.children:
                    reciever=findPerson(x,personName)
                    if reciever != None:
                        return reciever
                return None
            
def addHusband(root,brideName,groomName):
    target=findPerson(root,brideName)
    if target==None:
        return root
    else:
        groom=Male(groomName)
        groom.husbandOf=target
        target.wifeOf=groom
    
    return root

def addWife(root,groomName,brideName):
    target=findPerson(root,groomName)
    if target == None:
        return root
    else:
        bride=Female(brideName)
        bride.wifeOf=target
        target.husbandOf=bride
    return root

#if noPrint is True then no message will be printed. This is required for the buildTree method where messages are not required
def printer(str,noPrint):
    if noPrint == False:
        print(str)

def addChild(root,motherName,childName,gender,noPrint):
    if gender != "Male" and gender != "Female":
        printer("CHILD_ADDITION_FAILED",noPrint)
    else:
        target=findPerson(root,motherName)
        if target==None:
            printer("PERSON_NOT_FOUND",noPrint)
        else:
            if target.gender == "Male":
                printer("CHILD_ADDITION_FAILED",noPrint)
            elif target.wifeOf==None:
                printer("CHILD_ADDITION_FAILED",noPrint)
            else:
                if gender == "Male":
                    son=Male(childName)
                    son.sonOf=target
                    target.children.append(son)
                else:
                    daughter=Female(childName)
                    daughter.daughterOf=target
                    target.children.append(daughter)
                printer("CHILD_ADDITION_SUCCEEDED",noPrint)
    return root

#when a list is passed , it will print the list if not empty, otherwise NONE will be printed
def printList(lst):
    if len(lst) == 0:
        print("NONE",end=" ")
    else:
        for items in lst:
            print(items,end=" ")

def getMother(target):
    if target.gender == "Male":
        mother = target.sonOf
    else:
        mother = target.daughterOf
    return mother

def getPaternalUncle(root,target):
    paternalUncleList=list()
    mother=getMother(target)
    if mother != None:
        father=mother.wifeOf
        grandmom=father.sonOf
        if grandmom != None and len(grandmom.children) > 1:
            for x in grandmom.children:
                if x.gender == "Male" and x.name != father.name:  
                    paternalUncleList.append(x.name)
    printList(paternalUncleList)
    
def getMaternalUncle(root,target):
    maternalUncleList=list()
    mother=getMother(target)
    if mother != None:
        grandmom=mother.daughterOf
        if grandmom != None and len(grandmom.children) > 1:
            for x in grandmom.children:
                if x.gender == "Male":
                    maternalUncleList.append(x.name)
    printList(maternalUncleList)
    
def getPaternalAunt(root,target):
    paternalAuntList=list()
    mother=getMother(target)
    if mother != None and mother.wifeOf != None:
        father = mother.wifeOf
        grandmom=father.sonOf
        if grandmom != None and len(grandmom.children) > 1:
            for childs in grandmom.children:
                if childs.gender == "Female":
                    paternalAuntList.append(childs.name)
    printList(paternalAuntList)
    
def getMaternalAunt(root,target):
    maternalAuntList=list()
    mother=getMother(target)
    if mother != None:
        grandmom=mother.daughterOf
        if grandmom != None and len(grandmom.children) > 1:
            for childs in grandmom.children:
                if childs.gender == "Female" and childs.name != mother.name:
                    maternalAuntList.append(childs.name)
    printList(maternalAuntList)
    
def getSisterInLaw(root,target):
    sisterInLawList=list()
    mother=getMother(target)
    if mother != None and len(mother.children) > 1:
        for child in mother.children:
            if child.name != target.name and child.gender == "Male" and child.husbandOf != None:
                sisterInLawList.append(child.husbandOf.name)
    if target.gender == "Male":
        spouse = target.husbandOf
        if spouse != None:
            spouseMother = spouse.daughterOf
            if spouseMother != None and len(spouseMother.children > 1):
                for child in spouseMother.children:
                    if child.name != spouse.name and child.gender == "Female":
                        sisterInLawList.append(child.name)
    else:
        spouse = target.wifeOf
        if spouse != None:
            spouseMother = spouse.sonOf
            if spouseMother != None and len(spouseMother.children) > 1:
                for child in spouseMother.children:
                    if child.gender == "Female":
                        sisterInLawList.append(child.name)
    printList(sisterInLawList)
    
def getBrotherInLaw(root,target):
    brotherInLawList=list()
    mother=getMother(target)
    if mother != None and len(mother.children) > 1:
        for child in mother.children:
            if child.name != target.name and child.gender == "Female" and child.wifeOf != None:            
                brotherInLawList.append(child.wifeOf.name)
    if target.gender == "Male":
        spouse=target.husbandOf
        if spouse != None:
            spouseMother = spouse.daughterOf
            if spouseMother != None and len(spouseMother.children) > 1:
                for child in spouseMother.children:
                    if child.gender == "Male":
                        brotherInLawList.append(child.name)
    else:
        spouse = target.wifeOf
        if spouse != None:
            spouseMother = spouse.sonOf
            if spouseMother != None and len(spouseMother.children) > 1:
                for child in spouseMother.children:
                    if child.name != spouse.name and child.gender == "Male":
                        brotherInLawList.append(child.name)
    printList(brotherInLawList)
    
def getSon(root,target):
    sonList=list()
    if target.gender == "Male":
        wife = target.husbandOf
        if wife != None and len(wife.children) > 0:
            for x in wife.children:
                if x.gender == "Male":
                    sonList.append(x.name)
    else:
        if len(target.children) > 0:
            for x in target.children:
                if x.gender == "Male":
                    sonList.append(x.name)
    printList(sonList)
    
def getDaughter(root,target):
    daughterList=list()
    if target.gender == "Male":
        wife = target.wifeOf
        if wife != None and len(wife.children) > 0:
            for x in wife.children:
                if x.gender == "Female":
                    daughterList.append(x.name)
    else:
        if len(target.children) > 0:
            for x in target.children:
                if x.gender == "Female":
                    daughterList.append(x.name)
    printList(daughterList)
    
def getSiblings(root,target):
    siblingsList=list()
    mother=getMother(target)
    if mother != None and len(mother.children) > 1: 
        for x in mother.children:
            if x.name != target.name:
                siblingsList.append(x.name)
    printList(siblingsList)
    
def getRelationShip(root,name,relationName):
    target=findPerson(root,name)
    if target == None:
        print("PERSON_NOT_FOUND",end=" ")
    else:
        methodDict={"Paternal-Uncle":"getPaternalUncle(root,target)",
                    "Maternal-Uncle":"getMaternalUncle(root,target)",
                    "Paternal-Aunt":"getPaternalAunt(root,target)",
                    "Maternal-Aunt":"getMaternalAunt(root,target)",
                    "Sister-In-Law":"getSisterInLaw(root,target)",
                    "Brother-In-Law":"getBrotherInLaw(root,target)",
                    "Son":"getSon(root,target)",
                    "Daughter":"getDaughter(root,target)",
                    "Siblings":"getSiblings(root,target)"}
        eval(methodDict[relationName])
        
def addChildBulk(root,motherName,childDict):
    kidsKeys=childDict.keys()
    for x in kidsKeys:
        root=addChild(root,motherName,x.strip(),childDict[x],True)
    return root

def addWifeBulk(root,CoupleDict):
    wifeKeys=CoupleDict.keys()
    for x in wifeKeys:
        root=addWife(root,x,CoupleDict[x])
    return root

def buildtree(root):
    kids={"Chit":"Male","Ish":"Male","Vich":"Male","Aras":"Male","Satya":"Female"}
    root=addChildBulk(root,"Queen Anga",kids)
    Couples={"Chit":"Amba","Vich":"Lika","Aras":"Chitra"}
    root=addWifeBulk(root,Couples)
    root=addHusband(root,"Satya","Vyan")
    kids={}
    kids={"Dritha":"Female","Tritha":"Female","Vritha":"Male"}
    root=addChildBulk(root,"Amba",kids)
    root=addHusband(root,"Dritha","Jaya")
    kids={}
    kids={"Vila":"Female","Chika":"Female"}
    root=addChildBulk(root,"Lika",kids)
    kids={}
    kids={"Jnki":"Female","Ahit":"Male"}
    root=addChildBulk(root,"Chitra",kids)
    root=addHusband(root,"Jnki","Arit")
    kids={}
    kids={"Asva":"Male","Vyas":"Male","Atya":"Female"}
    root=addChildBulk(root,"Satya",kids)
    Couples={}
    Couples={"Asva":"Satvy","Vyas":"Krpi"}
    root=addWifeBulk(root,Couples)
    root=addChild(root,"Dritha","Yodhan","Male",True)
    kids={}
    kids={"Laki":"Male","Lavnya":"Female"}
    root=addChildBulk(root,"Jnki",kids)
    root=addChild(root,"Satvy","Vasa","Male",True)
    kids={}
    kids={"Kriya":"Male","Krithi":"Female"}
    root=addChildBulk(root,"Krpi",kids)
    return root

if __name__=="__main__":
    root=None
    root=initiateRoot(root,"King Shan","Queen Anga")
    root=buildtree(root)
    input_file = sys.argv[1]
    file=open(input_file)
    for x in file:
        gaps=0
        lst=x.strip().split(' ')
        for i in lst:
            if i == '':
                gaps=gaps + 1
        for y in range(1,gaps + 1):
            lst.remove('')
        if lst[0] == "ADD_CHILD":
            root=addChild(root,lst[1],lst[2],lst[3],False)
        elif lst[0] == "GET_RELATIONSHIP":
            getRelationShip(root,lst[1],lst[2])
            print("")
    
    