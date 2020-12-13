import json


class Object:
    def __init__(self, name):
        self.name = name
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


class GlobalRepository:
    def __init__(self):
        self.objects = []
    
    def add_object(self, element):
        self.objects.append(element)
    
    def get_object(self, element_name):
        for element in self.objects:
            if element.name == element_name:
                return element

# Sample usage
# def main():
#     gr = GlobalRepository()
#     elem = Object(name="Tomato Soup")
#     elem.add_property("vision", "color", "red")
#     elem.add_property("tactile", "temperature", "hot")
#     elem.add_property("tactile", "texture", "smooth")
#     elem.add_property("gustatory", "taste", "savoury")
#     elem.add_property("gustatory", "taste", "spicy")
#     elem.add_property("olfaction", "smell", "tangy_smell")
#     gr.add_object(elem)
#     print(json.dumps(gr.get_object("Tomato Soup").__dict__, indent=2))


# if __name__ == "__main__":
#     main()
