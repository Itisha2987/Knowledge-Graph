from global_repository import get_all_objects


data = get_all_objects()


def get_similarity_index(old_object, new_object):
	return 0.8


def get_most_similar_element(new_object):
    objects = data['objects']
    similar_elements = []
    for element in objects:
        similarity = get_similarity_index(element, new_object)
        if similarity > 0.75:
            similar_elements.append((similarity, element))

    return similar_elements
