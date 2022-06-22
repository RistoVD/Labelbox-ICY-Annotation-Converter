from labelb_import import labels
from labelToObject import LabelToObject
from icy_xml_printer import XmlDoc

for i in labels:
    a = LabelToObject(i)
    a.find_rois()
    my_print = XmlDoc(a)
    with open('OUTPUT/{}.xml'.format(a.name), 'w') as test_doc:
        my_print.display(file=test_doc)
