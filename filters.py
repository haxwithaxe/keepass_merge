
from smart_dict.filters import KeyValueFilter

def mangler_append_to_entry_comment(parent, key, value):
    parent["comment"] = "%s:\n%s\n\n"
    return key, value

class Password(KeyValueFilter):

    def __init__(self, matches, mangles=None):
        KeyValueFilter.__init__(self, KeyValueFilter.matches_key, mangles, "password")


class Comment(KeyValueFilter):

    def __init__(self, matches, mangles=None):
        KeyValueFilter.__init__(self, KeyValueFilter.matches_key, mangles, "comment")


class UserName(KeyValueFilter):

    def __init__(self, matches, mangles=None):
        KeyValueFilter.__init__(self, KeyValueFilter.matches_key, mangles, "username")


class URL(KeyValueFilter):

    def __init__(self, matches, mangles=None):
        KeyValueFilter.__init__(self, KeyValueFilter.matches_key, mangles, "url")


class Expire(KeyValueFilter):

    def __init__(self, matches, mangles=None):
        KeyValueFilter.__init__(self, KeyValueFilter.matches_key, mangles, "expire")



ENTRY_FILTERS = [Password(), Comment(), UserName(), URL(), Expire()]
