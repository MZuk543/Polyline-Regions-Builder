"""
Polyline's Regions Builder

The final project for CS50's Introduction to Programming with Python, 2022

"""

import argparse
import csv
from collections import deque
from dcll import DCLL, DCLLNode
import os
import sys
from typing import List, Optional, Tuple

EPS = 10e-5


class Point:
    def __init__(self, nr=0, x=0.0, y=0.0):
        self._x: float = x
        self._y: float = y
        self._nr: int = nr
        self._hierarchy: Optional[int] = None
        self._is_left: int = 0      # 0 - pt is on the line
                                    # 1 - pt is on the left side of the line
                                    # -1 - pt is on the right side of the line
        self._nr_max: int = 0

    def __str__(self):
        return f"Point:{self._nr}({self._x},{self._y})"

    def __repr__(self):
        return super().__repr__()

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return abs(self.x - other.x) <= EPS and abs(self.y - other.y) <= EPS

    def __hash__(self):
        return hash((self.x, self.y))

    @property
    def hierarchy(self):
        return self._hierarchy

    @hierarchy.setter
    def hierarchy(self, h: int):
        self._hierarchy = h

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x: float):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y: float):
        self._y = y

    @property
    def nr(self):
        return self._nr

    @nr.setter
    def nr(self, nr: int):
        self._nr = nr

    @property
    def is_left(self):
        return self._is_left

    @is_left.setter
    def is_left(self, b: int):
        self._is_left = b

    @property
    def nr_max(self):
        return self._nr_max

    @nr_max.setter
    def nr_max(self, nr: int):
        self._nr_max = nr


class StarshapedNode:
    """
    Starshaped list node: stores a deque of points that define a starshaped part of a polyline
    """
    def __init__(self, id=0):
        self._id: int = id
        self._hierarchy: int = 0
        self._area: float = 0
        self._pts_list: Optional[DCLL] = None
        self._pts_count: int = 0

    def __str__(self):
        return (f"Starshaped Node ID: {self.id} (hierarchy number is {self.hierarchy}, polyline's starshaped part area "
                f"is {self.area}, number of points of polyline's starshaped part is {self.pts_count})")

    def __repr__(self):
        if self.id == 0 and not self.pts_list:
            return super().__repr__()
        else:
            return (f"Starshaped Node (ID={self.id}, hierarchy_nr={self.hierarchy}, area={self.area}, "
                    f"pts_count={self.pts_count})")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, i: int):
        self._id = i

    @property
    def hierarchy(self):
        return self._hierarchy

    @hierarchy.setter
    def hierarchy(self, h: int):
        self._hierarchy = h

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, a: float):
        self._area = a

    @property
    def pts_list(self):
        return self._pts_list

    @pts_list.setter
    def pts_list(self, queue: DCLL):
        self._pts_list = queue

    @property
    def pts_count(self):
        return self._pts_count

    @pts_count.setter
    def pts_count(self, c: int):
        self._pts_count = c

    def append_point(self, pt: Point) -> Point:
        self.pts_list.append(pt)
        self.pts_count += 1
        return self.pts_list[self.pts_count - 1]


class StarshapedList:
    """
    Starshaped list: stores a deque of points, that define a starshaped part of a polyline
    """
    def __init__(self):
        self._starshaped_nodes_list: Optional[deque[StarshapedNode]] = None

    def __str__(self):
        if self.starshaped_nodes_list is not None:
            if self.starshaped_nodes_list:
                head = self.starshaped_nodes_list
                rng = range(len(head))
                lst = [f'Starshaped Node ID: {str(head[i].id)} of {str(head[i].pts_count)} points' for i in rng]
                return f"Starshaped List of [{', '.join(lst)}]"
            else:
                return f"Starshaped List of [...empty...]"
        else:
            return f"Starshaped List (not used)"

    def __repr__(self):
        if self.starshaped_nodes_list is not None:
            if self.starshaped_nodes_list:
                head = self.starshaped_nodes_list
                bf = os.path.basename(__file__)
                lst = [f'{str(head[i])}' for i in range(len(head))]
                return f"<{bf.split('.')[0]}.StarshapedList object: [{', '.join(lst)}]>"
            else:
                return super().__repr__()
        else:
            return super().__repr__()

    @property
    def starshaped_nodes_list(self):
        return self._starshaped_nodes_list

    @starshaped_nodes_list.setter
    def starshaped_nodes_list(self, queue: deque[StarshapedNode]):
        self._starshaped_nodes_list = queue

    def append(self, sn: StarshapedNode) -> StarshapedNode:
        if self.starshaped_nodes_list is not None:
            self.starshaped_nodes_list.append(sn)
        else:
            raise ValueError(f"Starshaped List queue not initiated, no queue to append node to.")
        return self.starshaped_nodes_list[len(self.starshaped_nodes_list) - 1]


class RegionNode:
    """
    Regions list node: stores a deque of starshaped lists of a polyline,
    that define the polyline region to be further simplified
    """
    def __init__(self, id=0, area=0):
        self._id: int = id
        self._hierarchy: int = 0
        self._area_sum: float = area
        self._reg_pts_list: Optional[deque[Point]] = None
        self._reg_pts_count: int = 0
        self._starshaped_list: Optional[StarshapedList] = None

    def __str__(self):
        if self.starshaped_list is not None:
            if self.starshaped_list and self.starshaped_list.starshaped_nodes_list:
                snl = self.starshaped_list.starshaped_nodes_list
                lst = [f'{str(snl[i])}' for i in range(len(snl))]
                return f"Region Node ID: {self.id} with Starshaped List of [{', '.join(lst)}]"
            else:
                return f"Region Node ID: {self.id} with Starshaped List of [...empty...]"
        else:
            return f"Region Node ID: {self.id} (not used)"

    def __repr__(self):
        if self.starshaped_list is not None:
            if self.starshaped_list:
                snl = self.starshaped_list.starshaped_nodes_list
                bf = os.path.basename(__file__)
                jn = ', '.join([f'{str(snl[i])}' for i in range(len(snl))])
                return f"<{bf.split('.')[0]}.RegionNode object: ID: {self._id} with Starshaped List: [{jn}]>"
            else:
                return super().__repr__()
        else:
            return super().__repr__()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, i: int):
        self._id = i

    @property
    def hierarchy(self):
        return self._hierarchy

    @hierarchy.setter
    def hierarchy(self, h: int):
        self._hierarchy = h

    @property
    def area_sum(self):
        return self._area_sum

    @area_sum.setter
    def area_sum(self, a: float):
        self._area_sum = a

    @property
    def reg_pts_list(self):
        return self._reg_pts_list

    @reg_pts_list.setter
    def reg_pts_list(self, q: deque[Point]):
        self._reg_pts_list = q

    @property
    def reg_pts_count(self):
        return self._reg_pts_count

    @reg_pts_count.setter
    def reg_pts_count(self, n: int):
        self._reg_pts_count = n

    @property
    def starshaped_list(self):
        return self._starshaped_list

    @starshaped_list.setter
    def starshaped_list(self, sl: StarshapedList):
        self._starshaped_list = sl


class RegionList:
    """
    Regions list: stores a deque of starshaped lists of a polyline,
    that define the polyline region to be further simplified
    """
    def __init__(self):
        self._region_nodes_list: Optional[deque[RegionNode]] = None
        self._count: int = 0

    def __str__(self):
        if self.region_nodes_list is not None:
            if self.region_nodes_list:
                rnl = self.region_nodes_list
                return f"Region List of [{', '.join([f'{str(rnl[i])}' for i in range(len(rnl))])}]"
            else:
                return f"Region List of [...empty...]"
        else:
            return f"Region List (not used)"

    def __repr__(self):
        if self.region_nodes_list is not None:
            if self.region_nodes_list:
                bf = os.path.basename(__file__)
                jn = ', '.join([f'{str(self.region_nodes_list[i])}' for i in range(len(self.region_nodes_list))])
                return f"<{bf.split('.')[0]}.RegionList object: [{jn}]>"
            else:
                return super().__repr__()
        else:
            return super().__repr__()

    @property
    def region_nodes_list(self):
        return self._region_nodes_list

    @region_nodes_list.setter
    def region_nodes_list(self, queue: deque[RegionNode]):
        self._region_nodes_list = queue

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, n: int):
        self._count = n

    def append(self, rn: RegionNode) -> RegionNode:
        self.region_nodes_list.append(rn)
        return self.region_nodes_list[len(self.region_nodes_list) - 1]

    def prepend(self, rn: RegionNode) -> RegionNode:
        self.region_nodes_list.appendleft(rn)
        return self.region_nodes_list[0]

    def add_pt(self, pt: Point) -> None:
        self.region_nodes_list[0].reg_pts_count += 1
        self.region_nodes_list[0].reg_pts_list.append(pt)
        return None


class Polyline:
    def __init__(self, id=None):
        self._id: int = id
        self.pts_list: List[Point] = []  # arrPts in phD code
        self._pts_count: int = 0
        self._intersect_pts_list: Optional[DCLL] = None
        self._intersect_pts_count: int = 0
        self._region_list: Optional[RegionList] = None
        self._pts_list_nr_max: int = 0

    def __str__(self):
        if self._pts_count == 0:
            if self._id:
                return f"Empty Polyline {self._id}"
            else:
                return "Empty Polyline"
        else:
            pl = self.pts_list
            pc = self.pts_count
            return f"Polyline {self.id} from Point {pl[0].nr} to Point {pl[pc - 1].nr} of {pc} points"

    def __eq__(self, other):
        if isinstance(other, Polyline) and self.pts_list == other.pts_list:
            return True
        else:
            return False

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def pts_count(self):
        return self._pts_count

    @pts_count.setter
    def pts_count(self, c: int):
        self._pts_count = c

    @property
    def intersect_pts_list(self):
        return self._intersect_pts_list

    @intersect_pts_list.setter
    def intersect_pts_list(self, queue: DCLL):
        self._intersect_pts_list = queue

    @property
    def intersect_pts_count(self):
        return self._intersect_pts_count

    @intersect_pts_count.setter
    def intersect_pts_count(self, c: int):
        self._intersect_pts_count = c

    @property
    def region_list(self):
        return self._region_list

    @region_list.setter
    def region_list(self, r: RegionList):
        self._region_list = r

    @property
    def pts_list_nr_max(self):
        return self._pts_list_nr_max

    @pts_list_nr_max.setter
    def pts_list_nr_max(self, nr_max: int):
        self._pts_list_nr_max = nr_max

    def add_point(self, point: Point) -> Point:
        self.pts_list.append(point)
        self.pts_count += 1
        self._pts_list_nr_max = max(point.nr, self.pts_list_nr_max)
        return self.pts_list[self.pts_count - 1]

    @staticmethod
    def is_left(pt: Point, start: Point, end: Point) -> float:
        """
        Check if a point is on the left side of a line.

        Copyright 2002, softSurfer (www.softsurfer.com)
        This code may be freely used and modified for any purpose
        providing that this copyright notice is included with it.

        Input: three points:
                start - line starting point
                end - line ending point
                pt - point pt, being checked
        Return: float   > 0 for pt left of the line through start and end
                        = 0 for pt on the line
                        < 0 for pt right of the line
        """
        return (end.x - start.x)*(pt.y - start.y) - (pt.x - start.x)*(end.y - start.y)
    
    @staticmethod
    def is_left_value(lv: float) -> int:
        if lv < 0:
            return -1
        elif lv > 0:
            return 1
        else:
            return 0

    def build_intersect_pts_list(self) -> DCLLNode:
        if not self.intersect_pts_list:
            self.intersect_pts_list = DCLL()
        self.intersect_pts_list.append(self.pts_list[0])
        self.intersect_pts_count += 1
        return self.intersect_pts_list[0]

    def add_intersect_point(self, point: Point) -> DCLLNode:
        if not self.intersect_pts_list:
            self.build_intersect_pts_list()
        self.intersect_pts_list.append(point)
        self.intersect_pts_count += 1
        return self.intersect_pts_list[self.intersect_pts_count - 1]

    def line_intersection(self, p1: Point, p2: Point, p3: Point, p4: Point) -> Tuple[bool, Optional[Point]]:
        """
        Counts two lines (Line1 and Line2) intersection point.
        Input: four points. Line1 is defined by p1, p2, Line2 by p3, p4
        Return: True and intersection point if lines do intersect
        """
        # a1, a2, b1, b2, c1, c2	- coefficients of lines equations
        # denominator - fraction denominator, to count intersection point
        a1 = p2.y - p1.y
        b1 = p1.x - p2.x
        c1 = p2.x * p1.y - p1.x * p2.y   # a1*x + b1*y + c1 = 0 is Line1

        a2 = p4.y - p3.y
        b2 = p3.x - p4.x
        c2 = p4.x * p3.y - p3.x * p4.y   # a2*x + b2*y + c2 = 0 is Line2

        denominator = a1 * b2 - a2 * b1
        if denominator == 0:
            return False, None

        pt_int = Point()
        pt_int.x = (b1 * c2 - b2 * c1) / denominator
        pt_int.y = (a2 * c1 - a1 * c2) / denominator
        pt_int.is_left = 0

        self.pts_list_nr_max += 1
        pt_int.nr = self.pts_list_nr_max

        return True, pt_int

    def start_new_region(self, reg_id=0) -> int:
        if self.region_list is None:
            self.region_list = RegionList()
            self.region_list.region_nodes_list = deque()
        reg_node = RegionNode(id=reg_id)
        reg_node.starshaped_list = StarshapedList()
        reg_node.starshaped_list.starshaped_nodes_list = deque()
        reg_node.reg_pts_list = deque()
        self.region_list.prepend(reg_node)
        self.region_list.count += 1
        return reg_id + 1

    def build_regions(self) -> bool:
        """
        Divides a polyline into regions, to be further simplified
        """
        next_reg_id = self.start_new_region(1)

        if self.pts_count > 0:
            self.region_list.add_pt(self.pts_list[0])

            # current_is_left: Optional[int] = None
            prev_is_left: int = 0

            for i in range(1, self.pts_count - 1):
                current_is_left = self.is_left_value(self.is_left(self.pts_list[i], self.pts_list[0],
                                                                  self.pts_list[self.pts_count - 1]))
                self.pts_list[i].is_left = current_is_left

                if current_is_left == prev_is_left:
                    self.region_list.add_pt(self.pts_list[i])
                else:
                    if current_is_left == 0:
                        self.region_list.add_pt(self.pts_list[i])

                        next_reg_id = self.start_new_region(next_reg_id)
                        self.region_list.add_pt(self.pts_list[i])

                        prev_is_left = current_is_left
                    elif (prev_is_left == 1 and current_is_left == -1) or (prev_is_left == -1 and current_is_left == 1):
                        intersection_point = None
                        if current_is_left == 1:  # point is on the left side of intersection line
                            res, intersection_point = self.line_intersection(self.pts_list[0],
                                                                             self.pts_list[self.pts_count - 1],
                                                                             self.pts_list[i],
                                                                             self.pts_list[i-1])
                            if res:
                                self.add_intersect_point(intersection_point)
                                self.region_list.add_pt(intersection_point)
                        if current_is_left == -1:  # point is on the right side of intersection line
                            res, intersection_point = self.line_intersection(self.pts_list[0],
                                                                             self.pts_list[self.pts_count - 1],
                                                                             self.pts_list[i-1],
                                                                             self.pts_list[i])
                            if res:
                                self.add_intersect_point(intersection_point)
                                self.region_list.add_pt(intersection_point)

                        next_reg_id = self.start_new_region(next_reg_id)
                        if intersection_point:
                            self.region_list.add_pt(intersection_point)
                        self.region_list.add_pt(self.pts_list[i])

                        prev_is_left = current_is_left
                    elif prev_is_left == 0:
                        self.region_list.add_pt(self.pts_list[i])
                        prev_is_left = current_is_left

            # adding last polyline point to a region
            self.region_list.add_pt(self.pts_list[self.pts_count - 1])
            return True
        else:
            return False


def input_parsing() -> Tuple:
    parser = argparse.ArgumentParser(description="Breaks polyline into regions.")
    parser.add_argument("-f", default="data.csv", help="Input file", type=str)
    args = parser.parse_args()
    return parser, args


def input_parsing_1(args):
    parser = argparse.ArgumentParser(description="Breaks polyline into regions.")
    parser.add_argument("-f", default="data.csv", help="Input file", type=str)
    parser_args = parser.parse_args(args)
    return parser_args


def fill_poly_with_data(csv_reader) -> Polyline:
    polyline = Polyline(id=1)
    for i, row in enumerate(csv_reader):
        if i > 0:
            if len(row) == 2:
                pt = Point(nr=i, x=float(row[0]), y=float(row[1]))
                polyline.add_point(pt)
            elif len(row) == 3:
                pt = Point(nr=row[0], x=float(row[1]), y=float(row[2]))
                polyline.add_point(pt)
    return polyline


def read_data(args) -> Tuple[Polyline, str]:
    # parser, args = input_parsing()
    parsed_args = input_parsing_1(args)
    try:
        with open(parsed_args.f) as f_input:
            reader = csv.reader(f_input)
            polyline = fill_poly_with_data(reader)
    except FileNotFoundError as e:
        # parser.exit(message="Invalid input file \n")
        sys.exit('Invalid input file \n')
    else:
        return polyline, parsed_args.f


def prepare_polyline(polyline: Polyline) -> bool:
    return polyline.build_regions()


def write_to_file(output_name: str, current_region: RegionNode):
    with open(output_name, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['Nr', 'X', 'Y'])
        writer.writerow({'Nr': 'Nr', 'X': 'X', 'Y': 'Y'})
        while True:
            try:
                pt = current_region.reg_pts_list.pop()
            except IndexError:
                pt = None
                break
            else:
                writer.writerow({'Nr': pt.nr, 'X': pt.x, 'Y': pt.y})
    return current_region


def process_regions(current_region: RegionNode, polyline: Polyline, input_name: str, digits_number: int) -> int:
    i = 0
    while current_region:
        i += 1
        output_name = input_name.removesuffix('.csv')
        output_name += ('_reg' + str(i).zfill(digits_number) + '.csv')
        current_region = write_to_file(output_name, current_region)
        try:
            current_region = polyline.region_list.region_nodes_list.pop()
        except IndexError:
            current_region = None
            break
        else:
            continue
    return i


def write_regions(polyline: Polyline, input_name: str) -> Tuple[bool, int]:
    """
    Writes each polyline's region's points into a separate file.
    Return: True - if succeeded
            False - if no regions found
    """
    if polyline.region_list:
        file_count = 0
        digits_number = len(str(polyline.region_list.count))
        try:
            current_region = polyline.region_list.region_nodes_list.pop()
        except IndexError:
            current_region = None
            return False, file_count
        else:
            file_count = process_regions(current_region, polyline, input_name, digits_number)
        return True, file_count
    else:
        return False, 0


def main(args=None):
    polyline, file_name = read_data(args)
    res = prepare_polyline(polyline)
    if res:
        output, file_count = write_regions(polyline, file_name)
        if output:
            print('')
            if file_count == 1:
                print(f'---------- Building {file_count} region succeeded :-) ----------')
            else:
                print(f'---------- Building {file_count} regions succeeded :-) ----------')
            print('')
        else:
            print('')
            print('---------- Building regions failed :-( ----------')
            print('')
    else:
        print("---------- Unable to build polyline's regions ----------")
    input('Press Enter to continue...')


if __name__ == "__main__":
    sys.exit(main())
