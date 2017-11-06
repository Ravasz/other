'''
Created on Jan 31, 2016

@author: mate
generate character sheets for lvl3 goblin PCs for pathfinder
Goblins racial characteristics:
- +4 Dex, -2Char, -2Str
- Darkvision, 60 feet
- small size
- base speed is 30 feet
- weapon familiarity: dogslicer, horsechopper, and anything with goblin in it
- skill (one of these):
  - Skilled: +4 bonus on Ride and stealth
  - Cave crawler: climb speed of 10 feet, +8 Climb
  - City scavenger: +2 perception, +2 survival
  - Eat anything: +4 survival, +4 on saves against nauseated and sickened
  - Hard head, big teeth: bite natural atack 1d4
  - Junk tinker: +2 craft on mechanical stuff, +2 driving
  - Over-sized ears: +4 perception
  - Tree runner: +4 climb, +4 acrobatics
'''

class featC:
  """hold a feat, its description, and its dependencies"""
  
  def __init__(self, nameS, desc, abdep, featdep, special, babDep = 0, isfighter = False, iscraft = False, ismagic = False):
    self.nameS = nameS # name of feat
    self.desc = desc # short description
    self.abDep = abdep # ability dependency
    self.featDep = featdep # feat dependency
    self.babDep = babDep # minimum Base Attack Bonus
    self.isFighterBonus = isfighter # is it a fighter bonus feat
    self.isCraft = iscraft # is it a craft feat
    self.isMagic = ismagic # is it a feat concerning magic
    self.specialS = special # other odd dependencies as string
    
    
  
  def __str__(self):
    return (str(self.nameS) + ": " + str(self.desc) + ". " + str(self.abDep) + " " + str(self.featDep) +
             " BAB +" + str(self.babDep) + " " + str(self.isFighterBonus)) + " " + str(self.specialS)
  
  def __repr__(self):
    return str(self.desc)

    
class skillC:
  """hold a skill, a dict containing which classes have each skill as class skill,
   the governing attribute, armor check penalty, and whether usable untrained"""
   
  def __init__(self,nameS = "",untrainedB = True,armorCheckB = False,abilityS = ""):
    self.nameS = nameS
    self.untrainedB = untrainedB
    self.armorCheckB = armorCheckB
    self.abilityS = abilityS
    
  def __str__(self):
    if self.armorCheckB:
      return (str(self.nameS) + ": " + " untrained: " + 
            str(self.untrainedB) + " ability: " + str(self.abilityS) + "*")
    else:
      return (str(self.nameS) + ": " + " untrained: " + 
            str(self.untrainedB) + " ability: " + str(self.abilityS))  
    
   

def featGenerator():
  """read in all feats from feats.txt and parse them into featC type classes"""
  featDict = {}
  
  def featDepCollector(featObject):
    """take a full object with feats and extend feat dependenices of each feat to include all subdependencies.
    This function is only to be used within featGenerator, and there, recursively
    Not written yet."""
    return None
  
  def specializer(depS, specS):
    """handle adding special dependencies to feats. Not written yet."""
    
    if depS == "Light": depS = "Armor Proficiency, Light"
    elif depS == "Medium": depS = "Armor Proficiency, Medium"

    if specS == "":
      specS = depS
    else:
      specS = specialDep + "," + depS
      
    return specS
  
  with open("feats.txt","r") as inpF:

    headerflag = True
    for inpLine in inpF:
      fighterBonus = False
      craftFeat = False
      magicFeat = False
      specialDep = ""
      babDep = 0
      abDepD = {}
      featDepL = []
      
      if headerflag: 
        headerflag = False
        continue
      inpList = inpLine.rstrip("\n").lstrip(" ").split("\t")
      # print inpList
      if inpList[0][-1] == "*": # handle fighter bonus feats
        fighterBonus = True
        inpList[0] = inpList[0][:-1]
      if " Spell" in inpList[0] or "Spell " in inpList[0] or "Counterspell" in inpList[0] \
      or inpList[0] == "Eschew Materials" or inpList[0] == "Combat Casting":
        magicFeat = True
      featDepNew = inpList[1].split(",")
      featDepList = []
      for featDepI in featDepNew:
        featDepList.append(featDepI.lstrip(" "))
      
      ####################################################
      #                                                  #
      # This bit here handles all the feat dependencies  #
      #                                                  #
      ####################################################  
      
      if featDepList == ["\xe2\x80\x94"]:
        pass
      else:
        # print featDepList
        armorFlag = False
        for fDep in featDepList:
          if armorFlag:
            armorFlag = False
            # add armor dependency
            specialDep = specializer(fDep,specialDep)
            continue
          curAbDep = {}
          if "Str " == fDep[:4] or "Dex " == fDep[:4] or "Con " == fDep[:4] or "Int " == fDep[:4] or "Wis " == fDep[:4] or "Cha " == fDep[:4]:
            curAbDep[fDep[:3]] = int(fDep[fDep.index(" ") + 1:])
            abDepD.update(curAbDep)
          elif "ase attack bonus" in fDep:
            babDep = int(fDep[fDep.index("+") + 1:])
          elif "aster level" in fDep:
            magicFeat = True
            # handle caster level dependency
          elif "class feature" in fDep:
            specialDep = specializer(fDep,specialDep)
            # handle weird class feature dependencies
          elif "Armor Proficiency" == fDep:
            armorFlag = True
          elif "-level" in fDep:
            specialDep = specializer(fDep,specialDep)
            # handle fighter and wizard level dependencies
          elif "Ability" in fDep:
            specialDep = specializer(fDep,specialDep)
            # weird abilites. should be just dropped really as it is a very manual thing
          elif "(conjuration)" in fDep:
            specialDep = specializer(fDep,specialDep)
            magicFeat = True
            # yet another weird feat
          elif "Any two critical feats" in fDep:
            specialDep = specializer(fDep,specialDep)
            # srsly
          elif "see feat" in fDep:
            specialDep = specializer(fDep,specialDep)
            # improved familiar feat only
          elif "Catch Off-Guard or Throw Anything" in fDep:
            specialDep = specializer(fDep,specialDep)
            #...
          elif "Character level" in fDep:
            specialDep = specializer(fDep,specialDep)
            #...
          elif "5 ranks in any Craft or Profession skill" == fDep:
            specialDep = specializer(fDep,specialDep)
            #...
          elif "Ride 1 rank" == fDep:
            specialDep = specializer(fDep,specialDep)
            #...
          elif "Weapon proficiency (crossbow)" == fDep:
            specialDep = specializer(fDep,specialDep)
            #...
          elif "Proficiency with weapon" == fDep:
            specialDep = specializer(fDep,specialDep)
            #...
          else:
            featDepL.append(fDep) 
            # if neither BAB nor ability dependence nor level dependence, nor other oddity,
            # then add it as a feat dependence
         

      featDict[inpList[0]] = featC(inpList[0], inpList[2],abDepD,featDepL, specialDep, babDep, fighterBonus, craftFeat, magicFeat)
      # write out processed feat to the dict with feat name as key and feat object as value
      #print featDict[inpList[0]]
  # for featItem in featDict: print featDict[featItem]
  inpF.close()
  return featDict


def abilityGenerator():
  """generate a set of ability scores using the point-buy system"""
  from random import randint
  def scoreCounter(abScore):
    """count the score of any ability and return its point value"""
    if type(abScore) != type(15): raise TypeError
    
    if abScore == 7: 
      abPoint = -4
      if abScore < 1: raise ValueError
    elif 7 < abScore < 14: abPoint = abScore - 10
    elif 13 < abScore < 16: abPoint = 2 * abScore - 23
    elif 15 < abScore < 18: abPoint = 3 * abScore - 38
    elif abScore == 18: abPoint = 17
    else: raise ValueError
    
    return abPoint
  
  def pointCounter(abPoint):
    """count the corresponding ability score to a given point value. Return the ability score.
    For points above 17, just return the attribute score of 18. For points below -4, just return 7."""
    if type(abPoint) != type(15): raise TypeError
    
    if abPoint <= -3: abScore = 7
    elif abPoint < 4: abScore = 10 + abPoint
    elif abPoint < 8: abScore = 13 + ((abPoint - 3)/2)
    elif abPoint < 11: abScore = 16
    elif abPoint < 17: abScore = 17
    else: abScore = 18
    
    return abScore
  oneMoreRound = True
  while oneMoreRound:
    abL = [] # this holds the ability scores
    pointsLeft = 15 # use 15 here for standard fantasy setting
    for i in range(1,6): # generate 5 ability scores
      minPoint = pointsLeft - ((6 - i) * 17) 
      maxPoint = pointsLeft - ((6 - i) * -4)
      minScore = pointCounter(minPoint)
      maxScore = pointCounter(maxPoint)     
      currNum = randint(minScore,maxScore)
      pointsLeft -= scoreCounter(currNum)
      abL.append(currNum)
    abL.append(pointCounter(pointsLeft))
    pointsLeft -= scoreCounter(abL[-1])
  
    abL.sort(reverse = True)
    if pointsLeft == 0: oneMoreRound = False
    else: 
      pass
      # print pointsLeft
      # print abL
      # print "caught an unfortunate error! Attempting to fix it by doing a loop."
  return abL

def classGenerator():
  """Choose a class randomly for our Goblin. Return it as a text."""
  from random import choice
  classL = ["Barbarian","Fighter","Shaman","Rogue"]
  return choice(classL)

def nameGenerator():
  """pick a name from the list (copied from the pfSRD)"""
  from random import choice
  nameL = ["Dogchewer", "Firesinger", "Gutwad", "Hogparts", "Horsebiter", "Mancooker", "Moonslaver", "Pokestick", "Ripnugget", "Stabsnacker", "Stumpbumper", "Swampstomper", "Toechopper", "Boorgub", "Chuffy", "Churkus", "Drubbus", "Gawg", "Ghorg", "Gogmurch", "Irnk", "Kavak", "Lunthus", "Mogmurch", "Mogawg", "Murch", "Nurpus", "Pogus", "Poog", "Ronk", "Rotfoot", "Unk", "Vogun", "Zobmaggle", "Zord", "Aka", "Chee", "Fevva", "Geedra", "Goomluga", "Gretcha", "Hoglob", "Janka", "Klongy", "Luckums", "Lupi", "Medge", "Namby", "Olba", "Rempy", "Reta", "Ruxi", "Vruta", "Yalla", "Ziku"]
  return choice(nameL)

def babGenerator(classSt, lvlN = 3):
  """calcualte base attack bonus of character based on class and level. 
  return base attack bonus as int"""
  
  if lvlN > 10:
    print "I can only do up to lvl 10"
    raise ValueError

  babD = {1:0,2:1,3:2,4:3,5:3,6:4,7:5,8:6,9:6,10:7} # this is the base attack bonus list for most non-fighter classes
  if classSt == "Barbarian" or classSt == "Fighter": return lvlN
  elif classSt == "Shaman" or classSt == "Rogue": return babD[lvlN]
  else: 
    print "class not found"
    raise ValueError
  
def saveGenerator():
  """generate appropriate saves for the character. Not written yet."""
  
def skillGenerator():
  """generate Skill dict from file. Not written yet."""
  
  skillD = {}
  
  with open("skills.txt","r") as inpF:
    headerFlag = True
    for inpLine in inpF:
      if headerFlag: 
        headerFlag = False
        continue
      inpList = inpLine.rstrip("\n").split("\t")
      
      curSkillN = inpList[0]
      
      if len(inpList[-1]) == 4:
        curArmorCheck = True
        curAb = inpList[-1][:-1]
      elif len(inpList[-1]) == 3:
        curArmorCheck = False
        curAb = inpList[-1]
      else:
        print "something wrong with skill governing attribute:"
        print inpList[-1]
        raise ValueError
      
      if inpList[-2] == "Yes":
        curUnt = True
      elif inpList[-2] == "No":
        curUnt = False
      else: 
        print "something wrong with the untrained ability marker"
        print inpList[-2]
        raise ValueError
      
      # I have decided to put class skills into a class class, rather than a skill class
      
      
      skillD[curSkillN] = skillC(curSkillN, curUnt, curArmorCheck, curAb)
      
      
        
      
  
  

def abilityAssigner(ClassStr, abL):
  """take a class name and a list of ability scores, and assign then to the six basic abilities to fit the chosen class.
  Also apply racial modifiers (only does goblins for the time being). Return abilities as dict."""
  abD = {}
  if len(abL) != 6: raise ValueError # this bit tests if the ability scores are okay
  for listItem in abL:
    if type(listItem) != type(15): raise TypeError
    if 6 < listItem < 19:
      pass
    else: raise ValueError
    
  if ClassStr == "Fighter": # assign ability scores for each class and add modifiers
    abD["Str"] = abL[2] - 2
    abD["Con"] = abL[1]
    abD["Dex"] = abL[0] + 4
    abD["Wis"] = abL[3]
    abD["Int"] = abL[4]
    abD["Cha"] = abL[5] - 2
    
  elif ClassStr == "Barbarian":
    abD["Str"] = abL[0] - 2
    abD["Con"] = abL[1]
    abD["Dex"] = abL[2] + 4
    abD["Wis"] = abL[3]
    abD["Int"] = abL[4]
    abD["Cha"] = abL[5] - 2    
    
  elif ClassStr == "Rogue":
    abD["Str"] = abL[2] - 2
    abD["Con"] = abL[1]
    abD["Dex"] = abL[0] + 4
    abD["Wis"] = abL[3]
    abD["Int"] = abL[4]
    abD["Cha"] = abL[5] - 2    
  
  elif ClassStr == "Shaman":
    abD["Str"] = abL[2] - 2
    abD["Con"] = abL[1]
    abD["Dex"] = abL[3] + 4
    abD["Wis"] = abL[0]
    abD["Int"] = abL[4]
    abD["Cha"] = abL[5] - 2        
    
  else: 
    print "unexpected class: " + ClassStr
    raise ValueError
  
  return abD

def featAssigner(cS, abD, fD, babN):
  """generate appropriate feats for the goblin based on ability dependencies and chosen class.
  Normal lvl3 characters get 2 feats, fighters get 4.
  this is not done yet. Now trying to make feats into classes"""
  
  from random import choice
  
  if cS not in ["Fighter","Rogue","Shaman","Barbarian"]:
    raise ValueError("class not recognized")
  
  if type(abD) != type({'Dex': 19}):
    raise TypeError("ability scores need to be in a dict")
  
  if len(abD) != 6:
    raise ValueError("wrong number of abilities")
  
  for dKey in abD:
    if dKey not in {'Dex': 21, 'Cha': 5, 'Int': 9, 'Wis': 10, 'Str': 8, 'Con': 15}:
      raise ValueError("some ability scores are messed up")
    
  featD = {} # this is the output dict of feats
  
  currD = {} # build dict with elements that would fit this character only
  for keyS in fD:
    depFlag = True 
    for depI in fD[keyS].abDep: # test for appropriate abilites first
      if abD[depI] < fD[keyS].abDep[depI]:
        depFlag = False
    if "Craft" in keyS or "Brew" in keyS or "Forge" in keyS or "Scribe" in keyS:
      depFlag = False # filter out craft spells. we won't need them
    if cS != "Shaman" and fD[keyS].isMagic:
      depFlag = False # filter out nonmagic feats for non casters
    if depFlag and babN >= fD[keyS].babDep: # then for BAB
      currD[keyS] = fD[keyS]
      #print fD[keyS]
      
  # pick feats here
  
  totFeats = 2

  if cS == "Fighter":
    featD["Weapon Finesse"] = fD["Weapon Finesse"] # as fighter bonues feat
    featD["Simple Weapon Proficiency"] = fD["Simple Weapon Proficiency"]
    featD["Martial Weapon Proficiency"] = fD["Martial Weapon Proficiency"]
    featD["Armor Proficiency, Light"] = fD["Armor Proficiency, Light"]
    featD["Armor Proficiency, Medium"] = fD["Armor Proficiency, Medium"]
    featD["Armor Proficiency, Heavy"] = fD["Armor Proficiency, Heavy"]
    featD["Shield Proficiency"] = fD["Shield Proficiency"]
    featD["Dodge"] = fD["Dodge"] # as fighter bonus feat
    
  if cS == "Rogue":
    featD["Weapon Finesse"] = fD["Weapon Finesse"]  
    featD["Simple Weapon Proficiency"] = fD["Simple Weapon Proficiency"]
    featD["Armor Proficiency, Light"] = fD["Armor Proficiency, Light"]
    
    totFeats -= 1
  
  if cS == "Barbarian":
    featD["Simple Weapon Proficiency"] = fD["Simple Weapon Proficiency"]
    featD["Martial Weapon Proficiency"] = fD["Martial Weapon Proficiency"]
    featD["Armor Proficiency, Light"] = fD["Armor Proficiency, Light"]
    featD["Armor Proficiency, Medium"] = fD["Armor Proficiency, Medium"]
    featD["Shield Proficiency"] = fD["Shield Proficiency"]
  
  if cS == "Shaman":
    featD["Simple Weapon Proficiency"] = fD["Simple Weapon Proficiency"]
    featD["Armor Proficiency, Light"] = fD["Armor Proficiency, Light"]
    featD["Armor Proficiency, Medium"] = fD["Armor Proficiency, Medium"]
  
  curLoop = 0
  loopCount = 0
  while curLoop < totFeats and loopCount < 100:
    loopCount += 1
    randEntry = choice(currD.keys())
    if randEntry in featD: continue
    featDepFlag = True
    if currD[randEntry].specialS != "":
      # print "not doing special feats"
      # print currD[randEntry].specialS
      continue
    #print currD[randEntry]
    #print currD[randEntry].featDep
    for featI in currD[randEntry].featDep:
      if featI not in featD:
        featDepFlag = False
        #print "nope"
        #print randEntry
    
    if featDepFlag: 
      featD[randEntry] = currD[randEntry] # pick a random feat from the dict above
      #print "got one"
      #print currD[randEntry]
      curLoop += 1
  
  return featD
  
def skillAssigner():
  """pick relevant skills for character. Not written yet."""

def equipmentGenerator():
  """generate weapons, armor, and any gear for the character. Not written yet"""


fD = featGenerator() # build dict of feats as fD from separate file
sD = skillGenerator() # build dict of feats as sD from separate file

# actually I should do classes and races the same way too, instead of hard-coding them into the program.

lvlInt = 3
stasL = abilityGenerator()
classS = classGenerator()
nameS = nameGenerator()

abilityD = abilityAssigner(classS, stasL)

featD = featAssigner(classS, abilityD, fD, babGenerator(classS, lvlInt))

print "name: ", nameS
print "class: ", classS
print "abilities:", abilityD
print "feats:"
for featName in featD:
  print featD[featName]
