import pandas as pd
from pydantic import BaseModel
from bull.core.exceptions import ParseError


class Parser(BaseModel):
    @classmethod
    def clean_csv_dataframe(cls, df):
        return

    @classmethod
    def clean_dataframe(cls, df, origin):
        cleaner = getattr(cls, f"clean_{origin}_dataframe")
        return cleaner(df)

    @classmethod
    def get_excel_dataframe(cls, *args, **kwargs):
        return pd.read_excel(*args, **kwargs)

    @classmethod
    def get_csv_dataframe(cls, *args, **kwargs):
        return pd.read_csv(*args, **kwargs)

    @classmethod
    def get_dataframe(cls, *args, origin, **kwargs):
        getter = getattr(cls, f"get_{origin}_dataframe")
        return getter(*args, **kwargs)

    @classmethod
    def read_excel(cls, *args, **kwargs):
        return cls.process(*args, origin="excel", **kwargs)

    @classmethod
    def read_csv(cls, *args, **kwargs):
        return cls.process(*args, origin="csv", **kwargs)

    @classmethod
    def process(cls, *args, origin, **kwargs):
        df = cls.get_dataframe(*args, origin=origin, **kwargs)
        df = cls.clean_dataframe(df, origin)
        valid, errors = [], []
        for i, row in df.iterrows():
            try:
                valid.append(cls(**row))
                print(i, end="\r")
            except Exception as e:
                print("err")
                errors.append(
                    {
                        "excel_row_number": i + 1,
                        "row_data": row,
                        "error": e,
                    }
                )
        if errors:
            raise ParseError(errors)
        return valid
