from global_repository import get_all_objects
from global_repository import get_object_data_through_name

data = get_all_objects()
senses = ["tactile","vision","olfaction","auditory","gustatory"]

def get_number_of_common_attributes(dict1, dict2):
    count = 0
    for key in dict1:
        if (key in dict2) and (dict1[key] == dict2[key]):
            count += 1
    return count

def get_similarity_index(old_object, new_object):
    if old_object["state"] != new_object["state"]:
        return 0

    total_attributes = 0
    common_attributes = 0
    for sense in senses:
        common_attributes += get_number_of_common_attributes(old_object[sense],new_object[sense])
        total_attributes += len(new_object[sense])
    similarity_index = float(common_attributes/total_attributes)
    return similarity_index

def get_most_similar_element(new_object_name):
    data = get_all_objects()
    objects = data['objects']
    new_object = get_object_data_through_name(new_object_name)
    similar_elements = []
    for element in objects:
        similarity = get_similarity_index(element, new_object)
        if similarity >= 0.75 and similarity!=1:
            similar_elements.append((similarity, element))

    return similar_elements

#Sample Usage
# def main():
#    new_object_name = input("Enter new object name: ")
#    print(get_most_similar_element(new_object_name))

#if __name__ == "__main__":
#    main()
