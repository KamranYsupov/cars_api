from typing import Any


def update_serializer_data(
        new_key: str,
        new_values: dict[str: Any, int: int],
        serializer_data: dict,
        not_found_value: Any,
):
    """
    Метод для обновления данных новыми полями

    args:
    new_key: str,
    new_values: dict[new_key: Any, id: int],
    serializer_data: dict,
    not_found_value: Any
    """
    count = 0
    updated_data = []
    for obj_data in serializer_data:
        try:
            updated_data_obj = new_values[count]
        except IndexError:
            obj_data.update({new_key: not_found_value})
            updated_data.append(obj_data)
            continue

        if obj_data.get('id') != updated_data_obj.get('id'):

            obj_data.update({new_key: not_found_value})
            updated_data.append(obj_data)
            continue

        obj_data.update({new_key: updated_data_obj.get(new_key)})
        updated_data.append(obj_data)

        count += 1

    return updated_data
