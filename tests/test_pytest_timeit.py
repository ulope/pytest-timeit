# -*- coding: utf-8 -*-
import pytest


def test_timeit_plain(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.timeit(n=10)
        def test_something():
            assert 1 == 1
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=30)
    assert result.ret == 0


def test_timeit_plain_rep_one(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.timeit(n=10, r=1)
        def test_something():
            assert 1 == 1
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=10)
    assert result.ret == 0


def test_timeit_fast(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.timeit(n=10000, mode='fast')
        def test_something():
            assert 1 == 1
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=3)
    assert result.ret == 0


def test_timeit_fast_rep_one(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.timeit(n=10000, r=1, mode='fast')
        def test_something():
            assert 1 == 1
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)
    assert result.ret == 0


def test_timeit_no_tests(testdir):
    testdir.makepyfile("""
        import pytest

        def test_something():
            assert 1 == 1
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)
    assert result.ret == 0


def test_timeit_w_fixture(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.timeit(n=10)
        def test_something(tmpdir):
            f = tmpdir.join('test')
            assert not f.check()
            f.write('test')
            assert f.check()
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=30)
    assert result.ret == 0


def test_timeit_method(testdir):
    testdir.makepyfile("""
        import pytest

        class TestCls(object):
            @pytest.mark.timeit(n=10)
            def test_something(self):
                assert 1 == 1
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=30)
    assert result.ret == 0


def test_timeit_class_marker(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.timeit(n=10)
        class TestCls(object):
            def test_something(self):
                assert 1 == 1
    """)
    result = testdir.runpytest()

    result.stdout.fnmatch_lines([
        '*TestCls::test_something[[]n=10, r=3[]]*[1234567890].*'
    ])
    result.assert_outcomes(passed=30)
    assert result.ret == 0


def test_timeit_output(testdir):
    testdir.makepyfile("""
        import time
        import pytest

        @pytest.mark.timeit(n=40)
        def test_something():
            time.sleep(.001)
            assert 1 == 1
    """)
    result = testdir.runpytest('-v', '-s')

    result.stdout.fnmatch_lines([
        '*output.py::test_something[[]n=40, r=3[]]*[0123456789].*'
    ])
    assert 'TimeIt results' in result.stdout.str()
    result.assert_outcomes(passed=120)
    assert result.ret == 0


def test_timeit_no_kwarg(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.timeit()
        def test_something():
            assert 1 == 1
    """)
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        "*'timeit' mark on 'test_timeit_no_kwarg.py::test_something' needs 'n'/'number' kwarg*"
    ])
    assert result.ret > 0


def test_timeit_args_present(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.timeit(10)
        def test_something():
            assert 1 == 1
    """)
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        "*'timeit' mark doesn't accept positional arguments (on 'test_timeit_args_present.py::test_something')*"
    ])
    assert result.ret > 0


@pytest.mark.parametrize(
    ('mode', 'exception'),
    (
        ('fast', None),
        ('safe', None),
        ('doesntexist', "*'timeit' mark 'mode' may only be one of 'safe' or 'fast'*")
    )
)
def test_timeit_invalid_mode(testdir, mode, exception):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.timeit(n=10, mode="{}")
        def test_something():
            assert 1 == 1
    """.format(mode))
    result = testdir.runpytest('-v')
    if mode == 'fast':
        result.assert_outcomes(passed=3)
    elif mode == 'safe':
        result.assert_outcomes(passed=30)
    if exception:
        result.stdout.fnmatch_lines([exception])
        assert result.ret > 0
    else:
        assert result.ret == 0


def test_timeit_disabled(testdir):
    """Ensure """
    testdir.makepyfile("""
        import pytest

        @pytest.mark.timeit(n=10)
        def test_something():
            assert 1 == 1
    """)
    result = testdir.runpytest('-p', 'no:timeit')
    assert 'TimeIt results' not in result.stdout.str()
    result.assert_outcomes(passed=1)
    assert result.ret == 0


def test_timeit_selected_mark(testdir):
    """Ensure """
    testdir.makepyfile("""
        import pytest

        def test_other():
            assert 1

        @pytest.mark.timeit(n=10)
        def test_something():
            assert 1 == 1
    """)
    result = testdir.runpytest('-m', 'timeit')
    result.assert_outcomes(passed=30)
    assert result.ret == 0


@pytest.mark.timeit(n=100000, r=4, mode='fast')
def test_timeit_self_fast():
    assert 1 == 1


@pytest.mark.timeit(n=2, r=5, mode='safe')
def test_timeit_self_safe():
    assert 1 == 1
