"""
Reads a dataset of a family tree and finds how people are related along with
their parent and spouse connections.
"""

from argparse import ArgumentParser
import json
import sys
import relationships

class Person:
    """
    A class for connecting people with their relatives in a few ways, 
    including adding parents, spouses, and finding connections or relationships
    with other people.
    
    Attributes:
        name (str): the name of a person.
        gender (str): the gender of a person
        parents (list of Person): a list containing all parents of the person
        spouse (Person): a person object representing the person's spouse.
    """
    
    def __init__(self, name, gender):
        """
        Creates the name, gender, parents, and spouse attributes of the Person class.
        
        Args:
            name (str): the name of the person.
            gender (str): the gender of the person.
            
        Side effects:
            Creates parents and spouse attributes.
        """
        self.name = name
        self.gender = gender
        self.parents = []
        self.spouse = None
        
    def add_parent(self, parent):
        """
        Takes a Person object as an argument and adds it to self's list of parents.
        
        Args:
            parent (Person): parent of self.
        """
        self.parents.append(parent)
    
    def set_spouse(self, spouse):
        """
        Takes a Person object as an argument and sets it to self's spouse attribute.
        
        Args:
            spouse (Person): spouse of self.
        """
        self.spouse = spouse
        
    def connections(self):
        """
        Finds people that self is related to and returns a dictionary of people
        and paths to those people.
        
        Returns:
            cdict (dict): dictionary containing people's names as keys and paths
            to those people as the values.
        """
        cdict = {}
        cdict[self] = ""
        queue = [self]
        while len(queue) != 0:
            person = queue.pop(0)
            personpath = cdict[person]
            for parent in person.parents:
                if parent in cdict:
                    pass
                else:
                    cdict[parent] = f"{personpath}P"
                    queue.append(parent)
            if not("S" in personpath) and (person.spouse != None) and not(person.spouse in cdict):
                cdict[person.spouse] = f"{personpath}S"
                queue.append(person.spouse)
        return cdict
            
    def relation_to(self, other):
        """
        Finds the relationship between self and the Person object taken as an argument.
        
        Args:
            other (Person): person to compare self to, to see if they are related.
            
        Returns:
            str: either the path between person and self, or none if there is none 
            or distant relative if there is no kinship term.
        """
        selfconnections = self.connections()
        personconnections = other.connections()
        sharedkeys = []
        lcr = {}
        lcrpath = ""
        for key in selfconnections.keys():
            if key in personconnections:
                sharedkeys.append(key)
        if sharedkeys.__len__ == 0:
            return None
        for key in sharedkeys:
            lcr[key] = f"{selfconnections[key]}:{personconnections[key]}"
        if len(lcr) == 0:
            return None
        lcrpath = min(lcr.values(), key = len)
        if lcrpath in relationships.relationships:
            return relationships.relationships[lcrpath][self.gender]
        else:
            return "distant relative"
             
class Family:
    """
    Class for keeping track of all the instances of Person while also
    providing ways to lookup relationships between people, and add parents
    and spouses.
    
    Attributes:
        people (dict): a dictionary of people where the key is the person's name
        and the value is the person's Person object.
    """
    def __init__(self, dict):
        """
        Creates the people dictionary attribute of the Family class, and takes
        a dictionary as an argument that has three keys. In the people dictionary
        will be all the people from the individuals dictionary key, and this
        method also adds parents and spouses to individuals.
        
        Args:
            dict (dict of (dict, dict, list)): dictionary with three keys of individuals, parents,
            and couples.
            
        Side effects:
            Creates people dictionary, and fills it with people from the dict argument.
        """
        self.people = {}
        self.dict = dict
        for key in dict["individuals"]:
            newperson = Person(key, dict["individuals"][key])
            self.people[newperson.name] = newperson
        for person in dict["parents"]:
            personobj = self.people[person]
            for parent in dict["parents"][person]:
                parentobj = self.people[parent]
                personobj.add_parent(parentobj)
        for pair in dict["couples"]:
            if len(pair) != 0:
                personone = pair[0]
                persononeobj = self.people[personone]
                persontwo = pair[1]
                persontwoobj = self.people[persontwo]
                persononeobj.set_spouse(persontwoobj)
                persontwoobj.set_spouse(persononeobj)
                       
    def relation(self, name_one, name_two):
        """
        Takes the names of two different people as arguments and returns the relationship
        between the two if there is one as a string.
        
        Args:
            name_one (str): the first person's name.
            name_two (str): the second person's name.
            
        Returns:
            str: relationship path between person one and two if there is one.
        
        """
        persononeobj = self.people[name_one]
        persontwoobj = self.people[name_two]
        return persononeobj.relation_to(persontwoobj)
        
def main(path, person, person_two):
    """
    Takes a filepath and two people as arguments. Opens the file and loads its contents,
    and finds the relation between the two people.
    
    Args:
        path (str): the filepath to open.
        person (str): name of person one.
        person_two (str): name of person two.
        
    Side effects:
        Creates Family instance with data from file, and checks if two people
        from the arguments are related or not.
    """
    with open(path, "r", encoding="utf-8") as f:
        familydata = json.load(f)
    family = Family(familydata)
    relation = family.relation(person, person_two)
    if relation == None:
        print(f"{person} is not related to {person_two}")
    else:
        print(f"{person} is {person_two}'s {relation}")
    
def parse_args(arglist):
    """ 
    Process command line arguments.
    
    Expect three mandatory arguments in a file and two names.
    
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument('filepath', help="the path to the JSON file")
    parser.add_argument('name1', help="the name of the first person")
    parser.add_argument('name2', help="the name of the second person")
    args = parser.parse_args(arglist)
    return args

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.filepath, args.name1, args.name2)
         
            
            
        
        
        
    
        
    