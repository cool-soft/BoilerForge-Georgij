import pandas as pd
from dateutil.tz import gettz


if __name__ == '__main__':
    df = pd.DataFrame(
        columns=["a", "b", "c"],
        data=[
            {"a": pd.Timestamp.now(tz=gettz("Asia/Yekaterinburg")), "b": 1, "c": 2},
            {"a": pd.Timestamp.now(tz=gettz("Asia/Yekaterinburg")), "b": 3, "c": 4},
            {"a": pd.Timestamp.now(tz=gettz("Asia/Yekaterinburg")), "b": 5, "c": 6}
        ]
    )

    df2 = pd.DataFrame(
        columns=df.columns,
        data=[
            {"a": pd.Timestamp.now(tz=gettz("Asia/Yekaterinburg"))},
        ]
    )
    df = df.append(df2, ignore_index=True)
    print()
