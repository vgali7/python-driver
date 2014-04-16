# Copyright 2013-2014 DataStax, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import Queue

from base import benchmark, BenchmarkThread

log = logging.getLogger(__name__)

class Runner(BenchmarkThread):

    def run(self):
        futures = Queue.Queue(maxsize=121)

        self.start_profile()

        for i in range(self.num_queries):
            if i >= 120:
                old_future = futures.get_nowait()
                old_future.result()

            future = self.session.execute_async(self.query, self.values)
            futures.put_nowait(future)

        while True:
            try:
                futures.get_nowait().result()
            except Queue.Empty:
                break

        self.finish_profile


if __name__ == "__main__":
    benchmark(Runner)
