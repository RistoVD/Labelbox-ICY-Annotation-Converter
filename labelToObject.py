class LabelToObject:

    def __init__(self, label):
        self.label = label
        self.name = label['External ID'].strip('.jpg')
        self.rectangles = []
        self.polylines = []
        self.polygons = []

    def find_rois(self):
        for i, annotation in enumerate(self.label['Label']['objects']):
            try:
                rect_name = annotation['classifications'][2]['answer']['title']
            except:
                try:
                    rect_name = annotation['classifications'][1]['answer']['title']
                except:
                    try:
                        rect_name = annotation['classifications'][0]['answer']['title']
                    except:
                        rect_name = 'unnamed'
            print(rect_name)
            if annotation['value'] == 'rectangle':
                coordinate_dict = annotation['bbox']
                self.rectangles.append({'{}'.format(rect_name): coordinate_dict})
            if annotation['value'] == 'poly_line':
                self.polylines.append(annotation['line'])
