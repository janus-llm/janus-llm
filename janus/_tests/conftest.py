# from https://stackoverflow.com/a/76349078
# configure our tests by default not to run slow tests
#
# to run slow tests along with the other tests, use:
#   pytest -m slow

allowed_markers = (
    "filterwarnings",
    "parametrize",
    "skip",
    "skipif",
    "usefixtures",
    "xfail",
)


def pytest_collection_modifyitems(config, items):
    for item in items:
        if all(False for x in item.iter_markers() if x.name not in allowed_markers):
            item.add_marker("always_run")
    if markexpr := config.getoption("markexpr", "False"):
        config.option.markexpr = f"always_run or ({markexpr})"
        print("[Including tests marked as slow]")
    else:
        config.option.markexpr = "always_run"
        print("[Use -m slow to include tests marked as slow]")


def pytest_configure(config):
    config.addinivalue_line("markers", "always_run: mark test as always run")
    config.addinivalue_line("markers", "slow: mark test as slow")
