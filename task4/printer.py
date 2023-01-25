from typing import Union

from content import tariff_info

sentinel = "children"
tab = '  '


def print_dict(dict_: dict):
    def recurse(element: Union[dict, list, str], tab_num: int = 0):
        if isinstance(element, dict):
            for key, value in element.items():
                if key != sentinel:
                    recurse(key, tab_num - 1)  # Вообще говоря, тут можно и принт
                recurse(value, tab_num + 1)
        elif isinstance(element, list):
            for sub_element in element:
                if isinstance(sub_element, str):
                    # Тут тоже можно и принт, но пусть принт будет в одном месте
                    recurse(sub_element, tab_num)
                else:
                    recurse(sub_element, tab_num + 1)
        elif isinstance(element, str):  # В принципе, можно просто else.
            # По сути, база рекурсии, сюда все и будет стекаться
            print(tab_num * tab + element)

    recurse(dict_)


print_dict(tariff_info)
