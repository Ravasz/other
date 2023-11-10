# character builder for DnD5


# test commit

# create classes for characters, feats, skills, races, and spells

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
    and specific racial traits or bonuses.
    """

    def __init__(self, name, description, racial_traits):
        self.name = name
        self.description = description
        self.racial_traits = racial_traits

    def __str__(self):
        traits_str = ', '.join(self.racial_traits)
        return (
            f"Race: {self.name}\n"
            f"Description: {self.description}\n"
            f"Racial Traits: {traits_str}"
        )


class Character:
    """
    This class represents a character in Dungeons & Dragons 5E.
    It includes attributes such as name, race, class, attributes (strength, dexterity, etc.),
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
        return (f"Name: {self.name}, Race: {self.race}, Class: {self.char_class}\n"
                f"Attributes: {self.attributes}\n"
                f"Skills: {skills_str}\n"
                f"Feats: {feats_str}\n"
                f"Spells: {spells_str}")


