from nose.tools import assert_equal, eq_, with_setup
from unittest import TestCase

answer = 42


class TestAnswer(TestCase):
    def setUp(self):
        print 'TC setup'

    def test(self):
        self.assertEquals(answer, 42)

    def tearDown(self):
        print 'TC teardown'


def setup_func():
    print 'setup'


def teardown_func():
    print 'teardown'


@with_setup(setup_func, teardown_func)
def test_answer():
    assert_equal(answer, 42)


def test_answer1():
    assert answer == 42


def test_answer2():
    eq_(answer, 42)


def test():
    '''
    >>> answer
    42
    '''
    assert False


def test_answer4():
    '''
    >>> assert_equal(answer, 42)
    >>> assert answer == 42
    >>> eq_(answer, 42)
    '''


def test_in():
    string = '43 test\n' * 1000
    assert 'test' in string

answer = 43


def test_answer_f():
    assert_equal(answer, 42)


def test_answer_f1():
    assert answer == 42, {'test': '''test,
test
test'''}


def test_answer_f2():
    eq_(answer, 42)
