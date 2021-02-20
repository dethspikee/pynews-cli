from click.testing import CliRunner

from pynews import __version__
from pynews.pynews import cli


def test_version():
    """
    Test correct version is used
    """
    assert __version__ == '0.1.0'


def test_pynews_cli():
    """
    Test if main menu contains 'hnews' option and signals
    correct exit code
    """

    runner = CliRunner()
    result = runner.invoke(cli)

    assert "hnews" in result.output
    assert result.exit_code == 0


def test_hnews_not_verbose():
    """
    Test hnews in standard not verbose mode
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["hnews"])

    assert "1:" in result.output
    assert result.exit_code == 0


def test_hnews_verbose():
    """
    Test hnews in verbose mode
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["hnews", "-v"])

    assert "URL:" in result.output
    assert result.exit_code == 0


def test_hnews_help():
    """
    Test help menu for hnews command
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["hnews", "--help"])

    assert "Fetch the latest" in result.output
    assert result.exit_code == 0
