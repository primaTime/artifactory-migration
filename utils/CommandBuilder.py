
class CommandBuilder:
    __command_list: list[str] = []

    def add_argument(self, argument: str):
        self.__command_list.append(argument)
        return self

    def add_mvn_argument(self, argument: str, value: str):
        self.add_argument(f"-D{argument}={value}")
        return self

    def build(self):
        return self.__command_list