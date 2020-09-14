import datetime as time


class LogData:

    def __init__(self, file_name):
        """
        Creates a log file for logging purpose. The
        filename contains the file_name parameter and
        a timestamp.

        :param file_name: filename
        """
        today = time.datetime.now()
        date = today.strftime("%d%m%Y-%H%M%S")

        self.__name = file_name + date
        self.__file = open(self.__name + '.txt', 'w')

        print("Created file: ", self.__name + '.txt')

    def write_date(self, input_data):
        """
        Writes a string to the created log file. Every line contains
        a timestap of the current time.

        :param input_data: string for the current line of text
        """
        current_time = time.datetime.now().time().strftime('%H:%M:%S')
        str_input = str(input_data)
        self.__file.write('[' + str(current_time) + ']:' + str_input + '\n')

    def close_file(self):
        """
        Closes the created log file.
        """
        print("Closing file: ", self.__name + '.txt')
        self.__file.close()

