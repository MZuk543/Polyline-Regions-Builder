# from project import Point
from dcll import DCLLNode, DCLL


def test_node_init():
    node = DCLLNode()
    assert node.data is None

    node = DCLLNode(data=3)
    assert node.data == 3


def test_node_str():
    node = DCLLNode()
    s = str(node)
    assert s == "Doubly Circular Linked List's Node (None)"
    node = DCLLNode(data="test")
    assert str(node) == "Doubly Circular Linked List's Node (test)"


def test_dcll_append():
    dcll = DCLL()
    for i in range(5):
        r = dcll.append(data=i)
        assert r == i


def test_dcll_remove():
    dcll = DCLL()
    for i in range(0, 5):
        dcll.append(data=i)
    for i in reversed(range(1, dcll.count)):
        r = dcll.remove(i)
        assert r == i - 1
    r = dcll.remove(0)
    assert (r is None)


def test_dcll_iter():
    dcll = DCLL()
    for i in range(5):
        dcll.append(i + 1)

    for i, it in enumerate(dcll):
        assert it.data == i + 1


def test_dcll_getitem():
    dcll = DCLL()
    for i in range(5):
        dcll.append(i + 1)

    for i in range(5):
        assert dcll[i].data == i + 1


def test_dcll_setitem():
    dcll = DCLL()
    for i in range(5):
        dcll.append(i + 1)
    dcll[0] = DCLLNode(100)
    assert dcll[0].data == 100

    dcll[len(dcll)] = DCLLNode(200)
    assert dcll[len(dcll) - 1].data == 200
