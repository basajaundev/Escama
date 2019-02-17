__author__ = 'David Román <gallaz@gmx.com>'

DEBUG = True

dict_exp = {}


def search_name_set(set_ab):
    if set_ab in dict_exp:
        return dict_exp[set_ab]
