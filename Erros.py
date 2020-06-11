
class NotFittedError(Exception):

    def __init__(self):
        self.message = 'The model need to be fitted first!!'

    def __str__(self):
        return 'Fitted Error: {0}'.format(self.message)
