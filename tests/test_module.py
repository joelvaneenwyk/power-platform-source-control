import pytest
from pyexpect import expect


class TestLib:
    """ "import pbivcs"""

    @pytest.mark.skip(reason="not implemented yet")
    def test_extract():
        expect(1).equals(0)

    @pytest.mark.skip(reason="not implemented yet")
    def test_compress():
        pass


class TestMainModule:
    """python -m pbivcs [--something]"""

    @pytest.mark.skip(reason="not implemented yet")
    def test_extract():
        pass

    @pytest.mark.skip(reason="not implemented yet")
    def test_compress():
        pass


class TestExecutable:
    """pbivcs [--something]"""

    @pytest.mark.skip(reason="not implemented yet")
    def test_extract():
        pass

    @pytest.mark.skip(reason="not implemented yet")
    def test_compress():
        pass
