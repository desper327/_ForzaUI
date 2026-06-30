# -*- coding: utf-8 -*-
"""Per-row background task runner with throttled progress signals."""

from __future__ import annotations

import time
from dataclasses import dataclass

from Qt import QtCore


class ExportWorker(QtCore.QObject):
    progress_changed = QtCore.Signal(int)
    finished = QtCore.Signal()
    cancelled = QtCore.Signal()

    def __init__(self, row_name: str, parent=None):
        super().__init__(parent)
        self._row_name = row_name
        self._cancelled = False

    @property
    def row_name(self) -> str:
        return self._row_name

    def cancel(self) -> None:
        self._cancelled = True

    @QtCore.Slot()
    def run(self) -> None:
        for step in range(101):
            if self._cancelled:
                self.cancelled.emit()
                return
            self.progress_changed.emit(step)
            QtCore.QThread.msleep(30)
        self.finished.emit()


@dataclass
class _ActiveTask:
    thread: QtCore.QThread
    worker: ExportWorker


class RowTaskManager(QtCore.QObject):
    """Runs one simulated export task per row; emits throttled progress updates."""

    progress_updated = QtCore.Signal(str, int)
    task_finished = QtCore.Signal(str)
    task_cancelled = QtCore.Signal(str)

    THROTTLE_MS = 100
    MIN_DELTA = 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tasks: dict[str, _ActiveTask] = {}
        self._last_emit: dict[str, tuple[float, int]] = {}

    def is_running(self, row_name: str) -> bool:
        return row_name in self._tasks

    def start(self, row_name: str) -> None:
        self.stop(row_name)
        thread = QtCore.QThread()
        worker = ExportWorker(row_name)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.progress_changed.connect(
            lambda value, name=row_name: self._on_progress(name, value)
        )
        worker.finished.connect(lambda name=row_name: self._on_finished(name))
        worker.cancelled.connect(lambda name=row_name: self._on_cancelled(name))
        worker.finished.connect(thread.quit)
        worker.cancelled.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.cancelled.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(lambda name=row_name: self._tasks.pop(name, None))
        self._tasks[row_name] = _ActiveTask(thread=thread, worker=worker)
        thread.start()

    def cancel(self, row_name: str) -> None:
        task = self._tasks.get(row_name)
        if task is not None:
            task.worker.cancel()

    def stop(self, row_name: str) -> None:
        task = self._tasks.pop(row_name, None)
        if task is None:
            return
        task.worker.cancel()
        task.thread.quit()
        task.thread.wait(500)
        self._last_emit.pop(row_name, None)

    def stop_all(self) -> None:
        for row_name in list(self._tasks):
            self.stop(row_name)

    def _should_emit(self, row_name: str, value: int) -> bool:
        now = time.monotonic()
        last = self._last_emit.get(row_name)
        if last is None:
            return True
        last_time, last_value = last
        if value in (0, 100):
            return True
        if abs(value - last_value) < self.MIN_DELTA:
            return False
        return (now - last_time) * 1000 >= self.THROTTLE_MS

    def _on_progress(self, row_name: str, value: int) -> None:
        if self._should_emit(row_name, value):
            self._last_emit[row_name] = (time.monotonic(), value)
            self.progress_updated.emit(row_name, value)

    def _on_finished(self, row_name: str) -> None:
        self._last_emit.pop(row_name, None)
        self.task_finished.emit(row_name)

    def _on_cancelled(self, row_name: str) -> None:
        self._last_emit.pop(row_name, None)
        self.task_cancelled.emit(row_name)
