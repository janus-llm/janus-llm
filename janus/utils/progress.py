from typing import Iterable

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from janus.utils.logger import create_logger

log = create_logger(__name__)


def track(
    iterable: Iterable, description: None | str = None, total: None | int = None
) -> Iterable:
    """Track progress of an iterable.

    Arguments:
        iterable: The iterable to track.
        description: The description to show for the progress bar.
        total: The total number of items in the iterable.
    """
    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            log.debug("Could not determine total number of items in iterable.")
            total = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}", justify="right"),
        BarColumn(),
        MofNCompleteColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        "[yellow]Time Elapsed:",
        TimeElapsedColumn(),
        "[cyan]Time Remaining:",
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task(description, total=total)
        for item in iterable:
            progress.update(task, advance=1)
            yield item


if __name__ == "__main__":
    from time import sleep

    for i in track(range(100), description="Processing:"):
        sleep(0.5)
