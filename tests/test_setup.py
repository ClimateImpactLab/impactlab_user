
from impactlab_user import __version__
from impactlab_user.cli import cli
from click.testing import CliRunner
from contextlib import contextmanager
import click
import tempfile
import shutil
import os
import pytest


def get_user_input(*args, **kwargs):
    return "my_response"


@contextmanager
def tmp_getter_getter():

    tmp = tempfile.mkdtemp()

    try:

        def get_tmp_dir(*args, **kwargs):
            return tmp

        yield get_tmp_dir

    finally:
        shutil.rmtree(tmp)


@contextmanager
def tmp_usrgetter_getter():

    tmp = tempfile.mkdtemp()

    try:

        def get_tmp_dir(*args, **kwargs):

            return os.path.join(tmp, 'datafs')

        yield get_tmp_dir

    finally:
        shutil.rmtree(tmp)


def test_setup_ssh_keys():
    runner = CliRunner()
    result = runner.invoke(cli, ['setup', 'ssh_keys'])
    assert result.exit_code == 0, result.output
    assert 'setting up ssh keys' in result.output


def test_setup_osdc():
    runner = CliRunner()
    result = runner.invoke(cli, ['setup', 'osdc'])
    assert result.exit_code == 0, result.output
    assert 'setting up osdc-comupte' in result.output


def test_setup_brc():
    runner = CliRunner()
    result = runner.invoke(cli, ['setup', 'brc'])
    assert result.exit_code == 0, result.output
    assert 'setting up brc' in result.output


def test_setup_osdc_data(monkeypatch):

    with tmp_usrgetter_getter() as get_tmp_usr:

        monkeypatch.setattr('click.prompt', get_user_input)
        monkeypatch.setattr('os.path.expanduser', get_tmp_usr)

        runner = CliRunner()
        result = runner.invoke(cli, ['setup', 'osdc_data'])
        assert result.exit_code == 0, result.output
        assert 'setting up osdc-data' in result.output


def test_setup_aws(monkeypatch):

    with tmp_usrgetter_getter() as get_tmp_usr:

        monkeypatch.setattr('click.prompt', get_user_input)
        monkeypatch.setattr('os.path.expanduser', get_tmp_usr)

        runner = CliRunner()
        result = runner.invoke(cli, ['setup', 'aws'])
        assert result.exit_code == 0, result.output
        assert 'setting up aws' in result.output


def test_setup_datafs(monkeypatch):
    runner = CliRunner()

    with tmp_getter_getter() as get_tmp_file:

        monkeypatch.setattr('click.get_app_dir', get_tmp_file)

        result = runner.invoke(cli, [
            'setup',
            'datafs',
            '--name',
            'My Name',
            '--contact',
            'my_email@hostname.com',
            '--team',
            'MyTeam',
            '--institution',
            'Institute'])

        assert result.exit_code == 0, result.output
        assert 'setting up datafs' in result.output


@pytest.mark.parametrize("hostname", ["sacagawea", "ln000.brc", "mymachine"])
def test_setup_shared_servers(hostname, monkeypatch):
    runner = CliRunner()

    def gethostname():
        return hostname

    with tmp_getter_getter() as get_tmp_file:

        monkeypatch.setattr('click.get_app_dir', get_tmp_file)
        monkeypatch.setattr('socket.gethostname', gethostname)

        result = runner.invoke(cli, [
            'setup',
            'datafs',
            '--name',
            'My Name',
            '--contact',
            'my_email@hostname.com',
            '--team',
            'MyTeam',
            '--institution',
            'Institute'])

        assert 'config.yml' in os.listdir(get_tmp_file())

        with open(os.path.join(get_tmp_file(), 'config.yml')) as f:
            tested_config = f.read()

        if hostname == 'sacagawea':
            assert '/shares/gcp/.datafs/cache' in tested_config
        elif hostname.endswith('brc'):
            assert '/global/scratch/mdelgado/.datafs/cache' in tested_config
        else:
            assert 'cache' not in tested_config

        assert result.exit_code == 0, result.output
        assert 'setting up datafs' in result.output


def test_setup_all(monkeypatch):
    runner = CliRunner()

    # override click.prompt, click.get_app_dir

    monkeypatch.setattr('click.prompt', get_user_input)

    with tmp_getter_getter() as get_tmp_file:

        monkeypatch.setattr('click.get_app_dir', get_tmp_file)

        with tmp_usrgetter_getter() as get_tmp_usr:

            monkeypatch.setattr('os.path.expanduser', get_tmp_usr)

            result = runner.invoke(cli, ['setup', 'datafs', 'all'])
            assert result.exit_code == 0, result.output

            assert 'setting up datafs' in result.output


def test_setup_datafs_interactive(monkeypatch):
    runner = CliRunner()

    # override click.prompt, click.get_app_dir

    monkeypatch.setattr('click.prompt', get_user_input)

    with tmp_getter_getter() as get_tmp_file:

        monkeypatch.setattr('click.get_app_dir', get_tmp_file)

        result = runner.invoke(cli, ['setup', 'datafs'])

    assert result.exit_code == 0, result.output
    assert 'setting up datafs' in result.output


def test_setup_datafs_interactive_badconfig(monkeypatch):
    runner = CliRunner()

    # override click.prompt, click.get_app_dir

    monkeypatch.setattr('click.prompt', get_user_input)

    with tmp_getter_getter() as get_tmp_file:

        monkeypatch.setattr('click.get_app_dir', get_tmp_file)

        config_file = os.path.join(click.get_app_dir('datafs'), 'config.yml')

        with open(config_file, 'w+') as cnf:
            cnf.write('this is not ::}}}valid yaml!')

        result = runner.invoke(cli, ['setup', 'datafs'])

    assert result.exit_code == 0, result.output
    assert 'setting up datafs' in result.output


def test_version():
    runner = CliRunner()

    result = runner.invoke(cli, ['--version'])

    assert result.exit_code == 0, result.output
    assert __version__ in result.output
