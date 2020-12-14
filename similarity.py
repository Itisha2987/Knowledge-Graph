from global_repository import get_all_objects
from global_repository import get_object_data_through_name

data = get_all_objects()


def get_similarity_index(old_object, new_object):
	return 0.8


def get_most_similar_element(new_object_name):
    objects = data['objects']
    new_object = get_object_data_through_name(new_object_name)
    similar_elements = []
    for element in objects:
        similarity = get_similarity_index(element, new_object)
        if similarity >= 0.75 and similarity!=1:
            similar_elements.append((similarity, element))

    return similar_elements
