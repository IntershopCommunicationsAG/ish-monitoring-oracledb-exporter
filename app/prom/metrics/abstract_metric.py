from abc import ABCMeta, abstractmethod


class AbstractMetric:
    """
    Abstract class for prom.
    This class defines the API interface for various types of prom.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """
        Empty constructor for now. Every derived class would be forced to create one.
        Should initialize query and metric
        """
    @abstractmethod
    def collect(self, app, rows):
        """
        Collect prom from Oracle and set prometheus
        :param rows: sql result
        :return:
        """
        pass

    def cleanName(self, original_name):
        s = original_name.replace(" ", "_", -1)  # Remove spaces
        s = s.replace("*", "_", -1)  # Remove star
        s = s.replace("(", "", -1)  # Remove open parenthesis
        s = s.replace(")", "", -1)  # Remove close parenthesis
        s = s.replace("/", "", -1)  # Remove forward addslashes
        s = s.lower()
        return s
