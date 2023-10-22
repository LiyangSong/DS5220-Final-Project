from IPython.core.display_functions import display
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import pandas as pd
import numpy as np


def check_out_general_info(df):
    print("\nGeneral information of DataFrame:")
    print(f"df.shape:\n{df.shape}")
    print("df.head():")
    display(df.head())
    print("df.info:")
    display(df.info())
    print("df.describe: ")
    display(df.describe())


def check_out_missing_target(df, target):
    print("\nCheck out observations with missing target:")
    drop_miss_tar_df = df.dropna(subset=target)
    print("df.shape: ", df.shape)
    print("drop_miss_tar_df.shape: ", drop_miss_tar_df.shape)
    if drop_miss_tar_df.shape[0] < df.shape[0]:
        print("Caution: data set contains observations with missing target!!!")
    else:
        print("No missing-target observations observed in data set.")


def check_out_duplicate_obs(df):
    print("\nCheck out duplicate observations:")
    drop_dup_df = df.drop_duplicates()
    print("df.shape: ", df.shape)
    print("drop_dup_df.shape: ", drop_dup_df.shape)
    if drop_dup_df.shape[0] < df.shape[0]:
        print("Caution: data set contains duplicate observations!!!")
    else:
        print("No duplicate observations observed in data set.")


def check_out_missingness(df, sample_size_threshold=250):
    print("\nCheck out missingness:")
    if df.isna().sum().sum() > 0:
        print("Caution: found missing values in data set!!!")
        print("Use missingno to understand pattern of missingness:")

        sample_size = df.shape[0] if df.shape[0] < sample_size_threshold else sample_size_threshold
        print(f"df.shape[0]: {df.shape[0]}")
        print(f"missingno sample_size: {sample_size}")

        msno.matrix(df.sample(sample_size, random_state=42))
        plt.title("Matrix visualizing nullity of DataFrame")
        plt.show()
        msno.heatmap(df.sample(sample_size, random_state=42))
        plt.title("Heatmap visualizing nullity of DataFrame")
        plt.show()
    else:
        print("No missing values in data set.")


def split_numerical_nominal_attr(df, target):
    print("\nSplit nominal and numerical attr:")

    cap_x_df = df.drop(target, axis=1)
    numerical_attr_list = cap_x_df.select_dtypes(include=['number']).columns.tolist()
    nominal_attr_list = cap_x_df.select_dtypes(exclude=['number']).columns.tolist()

    print(f"numerical_attr_list: \n{numerical_attr_list}")
    print(f"nominal_attr_list: \n{nominal_attr_list}")

    return numerical_attr_list, nominal_attr_list


def box_plot_for_numerical(df, numerical_attr_list, plot_col_num=4):
    attr_num = len(numerical_attr_list)
    plot_row_num = (attr_num // plot_col_num) + (attr_num % plot_col_num > 0)
    fig, axes = plt.subplots(plot_row_num, plot_col_num, figsize=(16, 5 * plot_row_num))
    for i, attr in enumerate(numerical_attr_list):
        row = i // plot_col_num
        col = i % plot_col_num
        df.boxplot(column=attr, ax=axes[row, col])
        axes[row, col].set_title(attr)
    plt.tight_layout()
    plt.show()


def tukeys_method(df, attr):
    q1 = df[attr].quantile(0.25)
    q3 = df[attr].quantile(0.75)
    iqr = q3 - q1
    inner_fence = 1.5 * iqr
    outer_fence = 3 * iqr

    # inner fence lower and upper end
    inner_fence_le = q1 - inner_fence
    inner_fence_ue = q3 + inner_fence

    # outer fence lower and upper end
    outer_fence_le = q1 - outer_fence
    outer_fence_ue = q3 + outer_fence

    outliers_prob = df[(df[attr] <= outer_fence_le) | (df[attr] >= outer_fence_ue)].index.tolist()
    outliers_poss = df[(df[attr] <= inner_fence_le) | (df[attr] >= inner_fence_ue)].index.tolist()

    return outliers_prob, outliers_poss


def tukeys_method_for_numerical(df, numerical_attr_list):
    print(f"\nImplement Tukey\'s fences to identify outliers based on the Inter Quartile Range (IQR) method:")
    results = []
    for attr in numerical_attr_list:
        outliers_prob, outliers_poss = tukeys_method(df, attr)
        results.append({
            'Attribute': attr,
            'Outliers Prob Count': len(outliers_prob),
            'Outliers Prob Fraction': len(outliers_prob) / len(df[attr]),
            'Outliers Poss Count': len(outliers_poss),
            'Outliers Poss Fraction': len(outliers_poss) / len(df[attr])
        })
    results_df = pd.DataFrame(results)
    display(results_df)


def hist_plot_for_numerical(df, numerical_attr_list):
    df[numerical_attr_list].hist(figsize=(16, 16))
    plt.tight_layout()
    plt.show()

def basic_stats(df, numerical_attr_list):
    basic_info = df[numerical_attr_list].describe().astype(int)
    display(basic_info)

def corr_attr(df, numerical_attr_list):
    result = df[numerical_attr_list].corr()
    corr_df = (
        result.where(
            np.triu(np.ones(result.shape), k=1)
            .astype(bool)
        )
        .stack()
        .to_frame(name='correlation')
    )

    new_index = [i + ' with ' + j for i, j in corr_df.index]
    corr_df.index = new_index
    corr_df = corr_df.sort_values('correlation', ascending=False)
    sns.heatmap(result)
    plt.show()
    return corr_df

def cardinality_nominal(df, nominal_attr_list):
    return 0

def outlier_nominal(df, nominal_attr_list):
    return 0
    
def corr_target(df, target, numerical_attr_list):
    corr_tar = df[numerical_attr_list].corrwith(df[target])
    var_attr = np.var(df[numerical_attr_list]).astype(int)
    result_df = pd.concat([corr_tar, var_attr], axis = 1)
    result_df = result_df.rename(columns={0: "Correlation", 1: "Variance"})
    return result_df