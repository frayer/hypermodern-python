import click.testing
import pytest

from hypermodern_python import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: click.testing.CliRunner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: click.testing.CliRunner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_fails_on_request_error(
    runner: click.testing.CliRunner, mock_requests_get
):
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code != 0
