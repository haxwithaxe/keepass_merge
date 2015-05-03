

from smart_dict.mergable import MergableDict

def merge_kdb(master, copy):
    master_dict = MergableDict(parse_kdb_xml(master))
    copy_dict = MergableDict(parse_kdb_xml(copy))
    master_dict.update(copy_dict)
    master_dict
