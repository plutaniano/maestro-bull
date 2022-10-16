class Force:
    def __new__(self, forced_type):
        class ForcedClass:
            @classmethod
            def __get_validators__(cls):
                yield lambda _: forced_type

        return ForcedClass
