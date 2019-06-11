from collections import OrderedDict

from tabulate import tabulate


class JobContext(object):
    """
    A shared context that will be available to all jobs.
    Common use cases would be to store broadcast variables, counters,
    parameters received from the command line etc.
    """
    def __init__(self, sc):
        self.counters = OrderedDict()
        self._init_accumulators(sc)
        self._init_shared_data(sc)

    def _init_accumulators(self, sc):
        pass

    def _init_shared_data(self, sc):
        pass

    def initalize_counter(self, sc, name):
        self.counters[name] = sc.accumulator(0)

    def inc_counter(self, name, value=1):
        if name not in self.counters:
            msg = f'{name} counter was not initialized. ({self.counters.keys()})'
            raise ValueError(msg)

        self.counters[name] += value

    def print_accumulators(self):
        msg = tabulate(
            self.counters.items(), self.counters.keys(), tablefmt="simple")
        print(msg)

    def logger(self, sc):
        component = "{}.{}".format(type(self).__module__, type(self).__name__)
        log4jLogger = sc._jvm.org.apache.log4j
        return log4jLogger.LogManager.getLogger(component)
