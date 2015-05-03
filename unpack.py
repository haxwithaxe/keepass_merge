
from lxml import etree


def load_xml(xml_filename):
    xml_file = open(xml_filename, "rb")
    tree = etree.parse(xml_file)
    xml_file.close()
    return tree


def print_elem(element):
    tag = element.tag
    title = element.find("title").text
    print(tag, title)


def parse_kdb_xml(kdb_xml):
    elements = []
    root = kdb_xml.getroot()
    db_iter = iter(root)
    return dict((x, y) for x, y in parse_elements(db_iter))


def parse_elements(elements):
    for element in elements:
        yield parse_element(element)


def parse_element(element):
    parsed_element = parse_element_by_tag[element.tag](element)
    return parsed_element


def parse_group(group):
    title = group.find("title").text
    icon = group.find("icon").text
    children = parse_elements(tuple(x for x in iter(group) if x.tag in ["group", "entry"]))
    children_dict = dict((x, y) for x, y in children)
    return (title, {"tag": "group", "title": title, "icon": icon, "children": children_dict})


def parse_entry(entry):
    """ 

    <entry>
        <title>title text</title>
        <username>username</username>
        <password>password</password>
        <url>url</url>
        <comment>comment</comment>
        <icon>1</icon>
        <creation>date</creation>
        <lastaccess>date</lastaccess>
        <lastmod>date</lastmod>
        <expire>Never</expire>
    </entry>
    
    ("title text", (
            ("title", title text),
            ("username", username),
            ("password", password),
            ("url", url),
            ("comment", comment),
            ("icon", 1),
            ("creation", date),
            ("lastaccess", date),
            ("lastmod", date),
            ("expire", Never)
        )
    )

    """
    title = entry.find("title").text
    properties = dict((node.tag, node.text) for node in entry)
    properties.update({"tag": "entry"})
    return (title, properties)


parse_element_by_tag = {"group": parse_group, "entry": parse_entry}


if __name__ == "__main__":
    import sys
    db = parse_kdb_xml(load_xml(sys.argv[1]))
    print(db)

