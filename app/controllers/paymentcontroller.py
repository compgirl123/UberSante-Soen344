import abc


class Context:
    """
    Define the interface of interest to clients.
    Maintain a reference to a Strategy object.
    """

    def __init__(self, strategy):
        self._strategy = strategy

    def context_interface(self):
        return self._strategy.getStrategy()


class Strategy(metaclass=abc.ABCMeta):
    """
    Declare an interface common to all supported algorithms. Context
    uses this interface to call the algorithm defined by a
    ConcreteStrategy.
    """

    @abc.abstractmethod
    def getStrategy(self):
        pass


class CreditOrDebit(Strategy):
    """
    Implement the algorithm using the Strategy interface.
    """

    def getStrategy(self):
        return "CreditOrDebit"


class Paypall(Strategy):
    """
    Implement the algorithm using the Strategy interface.
    """

    def getStrategy(self):
        return "Paypall"
        
