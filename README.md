# Python asyncio FFmpeg

[![Actions Status](https://github.com/scivision/asyncio-subprocess-ffmpeg/workflows/ci/badge.svg)](https://github.com/scivision/asyncio-subprocess-ffmpeg/actions)

Examples of Python asyncio.subprocess with FFmpeg and also traditional synchronous processes.
We use `src/` Python layout to demonstrate general good packaging practice, so to use the scripts:

```sh
pip install -e .
```

Hint the location of FFMPEG executable if necessary by setting the location in environment variable `FFMPEG_ROOT`.

All examples are under the [examples/](./examples) directory.

## Coroutine vs Threads vs processes

For computationally bound programs, multiple processes is often a good choice. Try:

```sh
python examples/benchmark.py -h
```

## FFprobe

Both synchronous (traditional for loop) and asynchronous pipeline are demonstrated.
They call FFprobe executable to return JSON formatted metadata.

* probe_sync.py: retrieve file metadata synchronously.
* probe_coroutine.py: retrieve file metadata in asynchronous pipeline or list using Python `asyncio` coroutines.

## FFplay

Testing asynchronous techniques with video playback makes some effects obvious.
The FFplay asyncio example is more advanced than the FFprobe example.
In the FFprobe example, the lazy asyncio generator produces metadata concurrently as fast as it's requested.
There is no resource throttling in the FFprobe example, so the CPU could become overwhelmed with context switching.

The FFplay example in contrast is an example of a task using resource throttling via asyncio.Queue.
The queuing could also be implemented for FFprobe style task if desired.
However, the rationale employed is that the FFprobe task is overall lightweight, and thus other parts of the pipeline inherently limit resource utilization.
If the FFprobe task was in an asyncio.gather() algorithm, resource utilization could get too high.
Thus we have a "win-win" by using asyncio generator for FFprobe--the throttling comes implicitly from other parts of the pipeline.

### Threading

Even though coroutines are more efficient in many applications, the syntax of `concurrent.futures.ThreadPoolExecutor` is perhaps the simplest possible way to spawn independent processes in a controlled fashion.

* play_thread.py: use ThreadPoolExecutor without queue
* play_thread_queue.py: use ThreadPoolExecutor with queue

### Coroutine

* play_coroutine.py: `asyncio` coroutine event loop to spawn processes.
