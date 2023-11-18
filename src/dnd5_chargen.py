# character builder for DnD5

class Feat:
    """Class to store feats"""
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"

class Skill:
    """Class to store skills"""
    def __init__(self, name, proficiency_level=0):
        self.name = name
        self.proficiency_level = proficiency_level
    
    def __str__(self):
        return f"{self.name} (Proficiency Level: {self.proficiency_level})"
    
    def increase_proficiency(self):
        self.proficiency_level += 1
    
    def set_proficiency(self, level):
        self.proficiency_level = level

class Spell:
    """
    This class represents a spell in Dungeons & Dragons 5E. 
    It stores details about the spell such as its name, level, school, 
    casting time, and a brief description.
    """
    
    def __init__(self, name, level, school, casting_time, description):
        self.name = name
        self.level = level
        self.school = school
        self.casting_time = casting_time
        self.description = description
    
    def __str__(self):
        return (
            f"{self.name} (Level {self.level} {self.school}) - "
            f"Casting Time: {self.casting_time}\n"
            f"Description: {self.description}"
        )

class Race:
    """
    This class represents a race in Dungeons & Dragons 5E.
    It includes attributes such as the race name, a brief description,
    racial traits, and ability score modifiers.
    """
    
    def __init__(self, name, description, racial_traits, ability_score_modifiers):
        self.name = name
        self.description = description
        self.racial_traits = racial_traits
        self.ability_score_modifiers = ability_score_modifiers
    
    def __str__(self):
        traits_str = ', '.join(self.racial_traits)
        modifiers_str = ', '.join(self.ability_score_modifiers)
        return (f"Race: {self.name}\n"
                f"Description: {self.description}\n"
                f"Racial Traits: {traits_str}\n"
                f"Ability Score Modifiers: {modifiers_str}")

class DnDClass:
    """
    This class represents a character class in Dungeons & Dragons 5E.
    It includes the class name and a brief description.
    """
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __str__(self):
        return f"Class: {self.name}\nDescription: {self.description}"

class Character:
    """
    This class represents a character in Dungeons & Dragons 5E.
    It includes attributes such as name, race, class, attributes 
    (strength, dexterity, etc.),
    skills, feats, and spells.
    """
    
    def __init__(self, name, race, char_class, strength, dexterity, 
                 constitution, intelligence, wisdom, charisma):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.attributes = {
            'strength': strength,
            'dexterity': dexterity,
            'constitution': constitution,
            'intelligence': intelligence,
            'wisdom': wisdom,
            'charisma': charisma
        }
        self.skills = []
        self.feats = []
        self.spells = []
    
    def add_skill(self, skill):
        self.skills.append(skill)
    
    def add_feat(self, feat):
        self.feats.append(feat)
    
    def add_spell(self, spell):
        self.spells.append(spell)
    
    def __str__(self):
        skills_str = ', '.join(str(skill) for skill in self.skills)
        feats_str = ', '.join(str(feat) for feat in self.feats)
        spells_str = ', '.join(str(spell) for spell in self.spells)
        
        attr_str = ""
        for key, value in self.attributes.items(): 
            if len(attr_str) > 0: attr_str += ", "
            attr_str += key + ": " + str(value)
        
        return (
            f"Name: {self.name}, Race: {self.race.name}, Class: {self.char_class.name}\n"
            f"Attributes: {attr_str}\n"
            f"Skills: {skills_str}\n"
            f"Feats: {feats_str}\n"
            f"Spells: {spells_str}"
        )

def generate_ability_scores(total_points=27, min_score=8, max_score=15):
    """
    Generate ability scores using a point buy system.
    :param total_points: Total points available for distribution.
    :param min_score: Minimum value for any ability score.
    :param max_score: Maximum value for any ability score before racial bonuses.
    :return: Dictionary with allocated ability scores.
    """
    ability_scores = {
        'Strength': min_score,
        'Dexterity': min_score,
        'Constitution': min_score,
        'Intelligence': min_score,
        'Wisdom': min_score,
        'Charisma': min_score
    }
    
    remaining_points = total_points
    
    for ability in ability_scores:
        while True:
            print(f"\nCurrent Ability Scores: {ability_scores}")
            print(f"Remaining Points: {remaining_points}")
            try:
                score = int(input(f"Enter score for {ability} (min {min_score}, max {max_score}): "))
                cost = calculate_point_cost(score, min_score)
                
                if min_score <= score <= max_score and cost <= remaining_points:
                    ability_scores[ability] = score
                    remaining_points -= cost
                    break
                else:
                    print(f"Invalid score or not enough points. Please try again.")
            except ValueError:
                print("Please enter a valid integer.")
    
    print(f"Remaining Points: {remaining_points}")
    print(ability_scores)
    return ability_scores

def calculate_point_cost(score, base_score=8):
    """
    Calculate the point cost for a given score in the point buy system.
    :param score: The ability score to calculate the cost for.
    :param base_score: The base score from which the point cost is calculated.
    :return: The point cost for the given score.
    """
    point_costs = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
    return point_costs.get(score, 0) - point_costs.get(base_score, 0)

def create_character(race_list, class_list):
    """
    Create a new character through a series of user prompts.
    
    :return: Character object with user-defined attributes.
    """
    # Prompt for basic character information
    name = input("Enter your character's name: ")
    print("Choose your race from the available options")
    for i in range(len(race_list)): print(str(i + 1) + ": " + race_list[i].name)
    race_in = input("")
    race = race_list[int(race_in) - 1]
    
    print("Choose your class from the available options")
    for i in range(len(class_list)): print(str(i + 1) + ": " + class_list[i].name)
    class_in = input("")
    char_class = class_list[int(class_in) - 1]
        
    # Generate ability scores using the point buy system
    while True:
        print("\nLet's determine your character's ability scores using a point buy system.")
        ability_scores = generate_ability_scores()
        break_val = input("ready to move on (y/n)?")
        if break_val == "y": break
    
    
    
    # Create the character object with the provided information
    character = Character(name, race, char_class, 
                          strength=ability_scores['Strength'],
                          dexterity=ability_scores['Dexterity'],
                          constitution=ability_scores['Constitution'],
                          intelligence=ability_scores['Intelligence'],
                          wisdom=ability_scores['Wisdom'],
                          charisma=ability_scores['Charisma'])
    
    return character

def read_races_from_file(file_path):
    """
    Read race details from a text file and create a list of Race objects.
    
    :param file_path: Path to the file containing race details.
    :return: A list of Race objects based on the details in the file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    races = []
    race_info = {
        "Race": "", 
        "Description": "", 
        "Racial Traits": "", 
        "Ability Score Modifier": ""
    }
    
    for line in lines:
        if line.strip() == '':
            # Create a Race object when a blank line is encountered
            if race_info:
                race = Race(
                    race_info['Race'], 
                    race_info['Description'], 
                    race_info['Racial Traits'], 
                    race_info['Ability Score Modifier']
                )
                races.append(race)
                race_info = {}
        else:
            key, value = line.split(':')
            key = key.strip()
            if key in ["Racial Traits", "Ability Score Modifier"]:
                value = [sub[1:] if sub[0] == " " else sub 
                        for sub in value.strip().split(",")]
            else: 
                value = value.strip()
            race_info[key] = value
    
    return races

def read_classes_from_file(file_path):
    """
    Read class details from a text file and create a list of DnDClass objects.
    
    :param file_path: Path to the file containing class details.
    :return: A list of DnDClass objects based on the details in the file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    classes = []
    class_name = ''
    description = ''
    
    for line in lines:
        if line.startswith('Class:'):
            class_name = line.split(':', 1)[1].strip()
        elif line.startswith('Description:'):
            description = line.split(':', 1)[1].strip()
            dnd_class = DnDClass(class_name, description)
            classes.append(dnd_class)
    
    return classes


core_races = read_races_from_file("other/src/race_5e.txt")
core_classes = read_classes_from_file("other/src/core_classes.txt")

test_character = create_character(core_races, core_classes)

print(test_character)

test_dict = {
    "foo": 2,
    "bar": 4,
    "baz": 3
}

