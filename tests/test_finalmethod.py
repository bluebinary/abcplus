import pytest
import six

import abcplus


@six.add_metaclass(abcplus.ABCMeta)
class Abstract(object):
    @abcplus.finalmethod
    def final(self):
        pass


class WorkingChild(Abstract):
    pass


class WorkingGrandChild(WorkingChild):
    pass


class WorkingGreatGrandChild(WorkingChild):
    pass


class AddFinalChild(Abstract):
    @abcplus.finalmethod
    def other_final(self):
        pass


class AddFinalGrandChild(AddFinalChild):
    pass


@pytest.mark.parametrize('working_class', [
    Abstract,
    WorkingChild,
    WorkingGrandChild,
    WorkingGreatGrandChild,
])
def test_inheriting_final_methods(working_class):
    working_class().final()
    assert True


@pytest.mark.parametrize('working_class', [
    AddFinalChild,
    AddFinalGrandChild,
])
def test_adding_final_methods_in_subclass(working_class):
    working_class().other_final()
    assert True


def test_overriding_final_methods():
    with pytest.raises(TypeError):
        class BrokenChild(Abstract):
            def final(self):
                pass

    with pytest.raises(TypeError):
        class BrokenGrandChild(WorkingChild):
            def final(self):
                pass

    with pytest.raises(TypeError):
        class BrokenGreatGrandChild(WorkingGrandChild):
            def final(self):
                pass

    with pytest.raises(TypeError):
        class BrokenChildOfAddFinalChild(AddFinalChild):
            def other_final(self):
                pass
