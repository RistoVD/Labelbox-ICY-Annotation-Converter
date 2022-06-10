class Tag(object):

    def __init__(self, name, contents):
        self.start_tag = '<{}>'.format(name)
        self.end_tag = '</{}>\n'.format(name)
        self.contents = contents

    def __str__(self):
        return "{0.start_tag}{0.contents}{0.end_tag}".format(self)

    def display(self, file=None):
        print(self, file=file, end='')


class FileName(Tag):

    def __init__(self, label):
        super().__init__('name', label.name)


class Meta(Tag):

    def __init__(self):
        posit_list = ["positionX", "PositionY", "PositionZ", "PositionT"]
        pixel_list = ["pixelSizeX", "pixelSizeY", "pixelSizeZ", "timeInterval"]
        channel_list = ["channelName0", "channelName1", "channelName2"]

        super().__init__('Meta', '')
        self._meta_contents = []
        # use list structure with tag class for printing of meta items
        for i in posit_list:
            new_tag = Tag(i, '0')
            self._meta_contents.append(new_tag)
        for i in pixel_list:
            new_tag = Tag(i, '1')
            self._meta_contents.append(new_tag)
        for index, value in enumerate(channel_list):
            new_tag = Tag(value, 'ch {}'.format(index))
            self._meta_contents.append(new_tag)
        self._meta_contents.append('<userName/>\n')

    def display(self, file=None):
        for tag in self._meta_contents:
            self.contents += str(tag)

        super().display(file=file)


class Rois(Tag):

    def __init__(self, label):

        super().__init__('rois', '')
        # self.roi_string = ''
        self._rectangle_contents = []
        self.rect_string = ''
        self.rect_tag = ''
        self.index = 0

        # variables used for polylines
        self._polyline_contents = []
        self.poly_string = ''

        for index, roi_object in enumerate(label.rectangles):
            key = list(roi_object)
            max_id = len(label.rectangles)
            print('rectangle count: {}'.format(max_id))

            coordinates = roi_object[key[0]]
            tlx, tly = coordinates['left'], coordinates['top']
            rbx, rby = coordinates['left'] + coordinates['width'], coordinates['top'] + coordinates['height']

            tlx_tag = Tag('pos_x', tlx)
            tly_tag = Tag('pos_y', tly)
            top_left_tag = str(tlx_tag)
            top_left_tag += str(tly_tag)

            rbx_tag = Tag('pos_x', rbx)
            rby_tag = Tag('pos_y', rby)
            bottom_right_tag = str(rbx_tag)
            bottom_right_tag += str(rby_tag)

            roi_settings = [Tag('classname', 'plugins.kernel.roi.roi2d.ROI2DRectangle'),
                            Tag('id', '{}'.format(self.index)),
                            Tag('name', '{}'.format(key[0])),
                            Tag('selected', 'false'),
                            Tag('readOnly', 'false'),
                            "<properties/>",
                            Tag('color', '-65281'),
                            Tag('stroke', '2'),
                            Tag('opacity', '0.3'),
                            Tag('showName', 'false'),
                            Tag('z', '-1'),
                            Tag('t', '-1'),
                            Tag('c', '-1'),
                            Tag('top_left', top_left_tag),
                            Tag('bottom_right', bottom_right_tag),
                            ]
            for tag in roi_settings:
                self.rect_string += str(tag)

            roi_tag = Tag('roi', self.rect_string)
            self.rect_string = ''
            self._rectangle_contents.append(str(roi_tag))
            self.index += 1

        for index, polyline in enumerate(label.polylines):
            points = ''
            print('polyline count: {}'.format(len(label.polylines)))

            for point in polyline:
                coordinates = ''
                x, y = point['x'], point['y']
                x_tag = Tag('pos_x', x)
                y_tag = Tag('pos_y', y)
                coordinates += str(x_tag)
                coordinates += str(y_tag)
                point_tag = Tag('point', coordinates)
                points += str(point_tag)

            line_settings = [Tag('classname', 'plugins.kernel.roi.roi2d.ROI2DPolyLine'),
                             Tag('id', '{}'.format(self.index)),
                             Tag('name', 'PolyLine2D'),
                             Tag('selected', 'false'),
                             Tag('readOnly', 'false'),
                             "<properties/>",
                             Tag('color', '-300100100'),
                             Tag('stroke', '2'),
                             Tag('opacity', '0.3'),
                             Tag('showName', 'false'),
                             Tag('z', '-1'),
                             Tag('t', '-1'),
                             Tag('c', '-1'),
                             Tag('points', points)
                             # Tag('bottom_right', bottom_right_tag),

                             ]
            for tag in line_settings:
                self.poly_string += str(tag)

            roi_tag = Tag('roi', self.poly_string)
            self.poly_string = ''
            self._polyline_contents.append(str(roi_tag))
            # self._rectangle_contents.append(str(roi_tag))
            self.index += 1

    def display(self, file=None):
        for bbox in self._rectangle_contents:
            self.contents += str(bbox)
        for line in self._polyline_contents:
            self.contents += str(line)
        super().display(file=file)


class XmlDoc(object):

    def __init__(self, label):
        self._name = FileName(label)
        self._meta = Meta()
        self._rois = Rois(label)

    def display(self, file=None):
        print('<root>', file=file)
        self._name.display(file=file)
        self._meta.display(file=file)
        self._rois.display(file=file)
        print('</root>', file=file)
