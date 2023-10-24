from IPython.core.display_functions import display
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import TargetEncoder
import pandas as pd


def sample_data(df, fraction, random_state=42):
    print(f"\nSample {fraction} fraction from DataFrame:")
    sample_df = df.groupby("label").apply(lambda x: x.sample(frac=fraction, random_state=random_state))
    print(f"sample_df.shape: {sample_df.shape}")
    return sample_df


def split_train_test_df(df, target, stratify=False, test_size=0.2, random_state=42):
    print("\nSplit DataFrame into train and test set:")

    cap_x_df, y_df = df.drop(target, axis=1), df[[target]]
    stratify = df[target] if stratify else None

    train_cap_x_df, test_cap_x_df, train_y_df, test_y_df = train_test_split(
        cap_x_df, y_df,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify)

    print("train set:")
    print(train_cap_x_df.shape, train_y_df.shape)
    print("test set:")
    print(test_cap_x_df.shape, test_y_df.shape)

    if stratify is not None:
        print(f"target distribution in train set: \n {train_y_df.value_counts(normalize=True)}")
        print(f"target distribution in test set: \n {test_y_df.value_counts(normalize=True)}")

    return train_cap_x_df, train_y_df, test_cap_x_df, test_y_df


def target_encode_categorical(df, categorical_attr_list, target):
    print("\nTarget encode categorical attributes:")

    cap_x = df[categorical_attr_list]
    y = df[target]
    encoder = TargetEncoder(random_state=42)
    cap_x_trans = encoder.fit_transform(cap_x, y)
    cap_x_trans_df = pd.DataFrame(cap_x_trans, columns=cap_x.columns, index=df.index)

    result = pd.concat([cap_x_trans_df, df.drop(columns=categorical_attr_list)], axis=1)
    print(f"encoded_df.head():")
    display(result.head())
    return result
