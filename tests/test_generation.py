from data_gen import GeneratorVariable, NormalVariable, VariableRelation
from pytest import fixture, approx, raises
import numpy as np


@fixture
def static_var():
    return NormalVariable(lower_base=5, upper_base=5, weight=1, std=0, noise=0)


@fixture
def unit_var():
    return NormalVariable(lower_base=0, upper_base=0, weight=1, std=1, noise=0)


def test_fail_on_not_implemented():
    with raises(TypeError):
        rel = GeneratorVariable().generate()


def test_get_one_base(static_var):
    assert static_var.get_bases() == 5


def test_get_five_bases(static_var):
    assert np.array_equal(static_var.get_bases(5), [5, 5, 5, 5, 5])


def test_generate_one(static_var):
    assert static_var.generate([5]) == 5


def test_generate_five(static_var):
    assert np.array_equal(static_var.generate(np.array([5, 5, 5, 5, 5])), [5, 5, 5, 5, 5])


def test_generate_std(unit_var):
    result = unit_var.generate(unit_var.get_bases(1000))
    assert not np.array_equal(result, np.zeros(1000))
    assert result.mean() == approx(0, abs=0.1)


def test_generate_noise():
    var = NormalVariable(lower_base=0, upper_base=0, weight=1, std=0, noise=1)
    result = var.generate(var.get_bases(1000))
    assert not np.array_equal(result, np.zeros(1000))
    assert np.mean(result) == approx(0, abs=0.1)


def test_direct_relation():
    var1 = NormalVariable(lower_base=3, upper_base=3, weight=2, std=0, noise=0)
    var2 = NormalVariable(lower_base=3, upper_base=3, std=0, noise=0)

    rel = VariableRelation([var1], var2)
    assert np.array_equal(rel.get(), [[3], [6]])
    assert np.array_equal(rel.get(5), [[3, 3, 3, 3, 3], [6, 6, 6, 6, 6]])


def test_multi_relation():
    var1 = NormalVariable(lower_base=3, upper_base=3, weight=2, std=0, noise=0)
    var2 = NormalVariable(lower_base=4, upper_base=4, weight=1, std=0, noise=0)
    var3 = NormalVariable(lower_base=3, upper_base=3, std=0, noise=0)

    rel = VariableRelation([var1, var2], var3)
    assert np.array_equal(rel.get(), [[3], [4], [10]])
    assert np.array_equal(rel.get(3), [[3, 3, 3], [4, 4, 4], [10, 10, 10]])


def test_multi_relation_std():
    var1 = NormalVariable(lower_base=3, upper_base=3, weight=2, std=1, noise=0)
    var2 = NormalVariable(lower_base=3, upper_base=3, weight=-1, std=0, noise=0)
    var3 = NormalVariable(lower_base=3, upper_base=3, std=0, noise=0)

    rel = VariableRelation([var1, var2], var3)
    result = rel.get(1000)
    assert not np.array_equal(result, np.full((3, 1000), fill_value=3))

    closeness = np.isclose(result.mean(axis=1), np.full(3, fill_value=3), atol=0.1)
    assert closeness.all()
