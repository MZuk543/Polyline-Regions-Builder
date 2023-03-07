# import argparse
# from csv import reader
# from io import StringIO
# import unittest
from unittest.mock import patch, mock_open
# import pdb
from project import prepare_polyline, read_data, fill_poly_with_data, Polyline, Point
import pytest
# import sys


@pytest.fixture
def test_file_content_mock():
    return """173,349
210,406
191.5,486
267,558
401,531
374,470
422,414
497,349"""


@pytest.fixture
def test_file_content_with_xy_mock(test_file_content_mock):
    return "X,Y\n" + test_file_content_mock


@pytest.fixture
def test_file_empty():
    return ''


@pytest.fixture
def test_polyline_instance(test_file_content_mock):
    polyline = Polyline(id=1)
    pts_list = [[float(x) for x in ss.split(',')] for ss in test_file_content_mock.split('\n')]
    for i, pt_list in enumerate(pts_list):
        pt = Point(nr=i, x=pt_list[0], y=pt_list[1])
        polyline.add_point(pt)
    return polyline


@pytest.fixture
def test_polyline_empty():
    return Polyline(id=1)


@pytest.fixture
def test_csv_reader(test_file_content_with_xy_mock):
    return [[s for s in ss.split(',')] for ss in test_file_content_with_xy_mock.split('\n')]


@pytest.fixture
def test_csv_reader_empty():
    return ['']


def test_fill_poly_with_data(test_csv_reader, test_csv_reader_empty, test_polyline_instance, test_polyline_empty):
    expected = test_polyline_instance
    actual = fill_poly_with_data(test_csv_reader)
    assert expected == actual

    expected_empty = test_polyline_empty
    actual_empty = fill_poly_with_data(test_csv_reader_empty)
    assert expected_empty == actual_empty


def test_read_data(test_file_content_with_xy_mock, test_polyline_instance):
    expected = (test_polyline_instance, 'data.csv')
    mock_1 = mock_open(read_data=test_file_content_with_xy_mock)
    mock_1.return_value.__iter__ = lambda self: self
    mock_1.return_value.__next__ = lambda self: next(iter(self.readline, ''))
    with patch('project.open', mock_1):
        actual = read_data(['-f', 'data.csv'])
    # pdb.set_trace()
    assert expected == actual

    # next two tests are doing the same thing, just syntax is different
    # testing for both errors without checking the error message
    with patch('project.open') as mock_2:
        mock_2.side_effect = FileNotFoundError
        # !!! below the order of errors is crucial
        with pytest.raises(SystemExit), pytest.raises(FileNotFoundError):
            assert read_data(['-f', ''])

        with pytest.raises(SystemExit):
            with pytest.raises(FileNotFoundError):
                assert read_data(['-f', 'cos'])

    # next two tests are doing the same thing, just syntax is different
    # testing for errors and error message
    with patch('project.open') as mock_3:
        mock_3.side_effect = FileNotFoundError
        with pytest.raises(SystemExit, match='Invalid input file'):
            assert read_data(['-f', ''])

        with pytest.raises(SystemExit) as e:
            assert read_data(['-f', ''])
        assert 'Invalid input file' in str(e.value)


def test_prepare_polyline(test_polyline_instance, test_polyline_empty):
    expected = True
    actual = prepare_polyline(test_polyline_instance)
    assert expected == actual

    expected_empty = False
    actual_empty = prepare_polyline(test_polyline_empty)
    assert expected_empty == actual_empty
    