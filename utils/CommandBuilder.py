
class CommandBuilder:
    MAVEN_ARGUMENT_PREFIX: str = "-D"

    def __init__(self):
        self.__command_list: list[str] = []

    def add_argument(self, argument: str):
        self.__command_list.append(argument)
        return self

    def add_mvn_argument(self, argument: str, value: str):
        self.add_argument(f"{self.MAVEN_ARGUMENT_PREFIX}{argument}={value}")
        return self

    def remove_mvn_argument(self, argument: str):
        self.__command_list = [x for x in self.__command_list if not x.startswith(f"{self.MAVEN_ARGUMENT_PREFIX}{argument}=")]
        return self

    def build(self):
        return self.__command_list