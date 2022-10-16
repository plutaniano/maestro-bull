class CPF(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.check_len
        yield cls.pad
        yield cls.run_algorithm

    @classmethod
    def check_len(cls, v):
        assert len(v) <= 11
        return v

    @classmethod
    def pad(cls, v):
        v = v.rjust(11, "0")
        if len(v) != 11:
            raise ValueError("CPF must have 11 digits")
        return v

    @classmethod
    def run_algorithm(cls, v):
        # https://dicasdeprogramacao.com.br/algoritmo-para-validar-cpf/
        try:
            for i in range(2):
                sum = 0
                for digit, multiplier in zip(v, range(10 + i, 1, -1)):
                    sum += int(digit) * multiplier
                assert int(sum * 10 % 11 % 10) == int(v[-2 + i])
            return v
        except AssertionError:
            raise ValueError("Invalid CPF")


class CNPJ(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.check_len
        yield cls.pad
        yield cls.run_algorithm

    @classmethod
    def check_len(cls, v):
        assert len(v) >= 12
        return v

    @classmethod
    def pad(cls, v):
        v = v.rjust(14, "0")
        if len(v) != 14:
            raise ValueError("CNPJ must have 14 digits")
        return v

    @classmethod
    def run_algorithm(cls, v):
        # https://souforce.cloud/regra-de-validacao-para-cpf-e-cnpj/
        magic = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        try:
            for i in range(2):
                sum = 0
                for digit, multiplier in zip(v, magic[1 - i :]):
                    sum += int(digit) * multiplier
                remainder = int(sum % 11)
                if remainder < 2:
                    assert v[-2 + i] == "0"
                else:
                    assert v[-2 + i] == str(11 - remainder)
            return v
        except AssertionError:
            raise ValueError("Invalid CNPJ")
