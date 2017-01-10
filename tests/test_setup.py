
from impactlab_user.cli import cli
from click.testing import CliRunner


def test_run_all_commands():

    runner = CliRunner()

    result = runner.invoke(cli, ['setup'])

    assert 'setting up ssh keys' in result.output
    assert 'setting up osdc-comupte' in result.output
    assert 'setting up brc' in result.output
    assert 'setting up osdc-data' in result.output
    assert 'setting up aws' in result.output
    assert 'setting up datafs' in result.output