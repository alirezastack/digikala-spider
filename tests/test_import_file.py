from build.lib.swagkar.import_swagger_file import import_file
import pytest


def test_import_invalid_file_path():
    with pytest.raises(ValueError):
        import_file('/path/does/not/exist')


def test_import_valid_file_path():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        import_file('./test_sample_file.yaml')

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code is None
