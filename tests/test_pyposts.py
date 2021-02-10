from click.testing import CliRunner

from pynews import __version__
from pynews.cli import cli


def test_version():
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


