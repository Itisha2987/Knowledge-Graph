import json


class Object:
    def __init__(self, name, state):
        self.name = name
        self.state = state
        self.vision = {}
        self.tactile = {}
        self.gustatory = {}
        self.auditory = {}
        self.olfaction = {}
        

    def add_property(self, sense, attribute, value):
        properties = self.__getattribute__(sense)
        properties.update({attribute: value})
    
    def __str__(self):
        return self.name


def get_all_objects():
    with open('global_repo.json') as json_file: 
        data = json.load(json_file) 
        return data


def add_object_in_global_repo(elem):
    data = get_all_objects() 
    object_array = data['objects']
    object_array.append(elem.__dict__) 

    with open('global_repo.json','w') as json_file: 
        json.dump(data, json_file, indent=2)


def get_object_data_through_name(object_name):
    data = get_all_objects()
    for element in data["objects"]:
        if element["name"] == object_name
        return element


def get_element_attributes():
    element_name = input("Enter the name of object: ")
    element_state = input("Enter the state of object: ")
    elem = Object(element_name, element_state)

    senses = ["tactile", "gustatory", "olfaction", "auditory", "vision"]

    for sense in senses:
        object_properties = input("Enter the " + sense + "properties of the object (space seperated attribut:value): ")
        if object_properties=="":
            continue
        properties = object_properties.strip().split(' ')
        for p in properties:
            attribute, value = p.split(':')
            elem.add_property(sense, attribute, value)

    return elem


def main():

    element = get_element_attributes()
    add_object_in_global_repo(element)


if __name__ == "__main__":
    main()
