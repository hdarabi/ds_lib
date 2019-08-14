import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig, text, subplots, style
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, roc_curve


def get_quantile_by_another_column(df, col_to_quantile, col_to_sort_by, q=0.5):
    """
    Finds the corresponding quantile of a column and returns the corresponding value of another column.
    Is valuable for creating charts, which the quantile column is the y axis and sort_by column is x axis.
    :param df: input dataframe
    :param col_to_quantile: column to calculate quantiles by
    :param col_to_sort_by: column to sort values by
    :param q: the target quantile
    :return: value of the quantile
    """

    df.sort_values(by=[col_to_sort_by], inplace=True)
    df['quantile'] = df[col_to_quantile].cumsum() / df[col_to_quantile].sum()
    q_val = df[df['quantile'] > q].iloc[0][col_to_sort_by]
    df.drop('quantile', axis=1, inplace=True)
    return q_val


def plot_save_xy_barchart_with_quantiles(df, xcol, ycol, xlabel, ylabel, title, filename=None, q=None):
    """
    Plots a barchart with additional lines to show percentile of the values.
    :param df:
    :param xcol:
    :param ycol:
    :param xlabel:
    :param ylabel:
    :param title:
    :param filename:
    :param q:
    :return:
    """
    df.sort_values(by=[xcol], inplace=True)
    fig, ax = subplots()
    plt.style.use('ggplot')
    ax.bar(x=df[xcol].values, height=df[ycol].values, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    max_y = df[ycol].max() * 0.90
    if q:
        for next_q in q:
            q_val = get_quantile_by_another_column(df=df, col_to_quantile=ycol, col_to_sort_by=xcol, q=next_q)
            ax.axvline(x=q_val, c='red', ls='dashed')
            text(x=q_val + 0.5, y=max_y, s=str(round(100 * next_q, 1)) + " %", rotation=90, verticalalignment='center')
    if filename:
        savefig(filename)
    plt.close()


def list_to_multiple_rows(data, list_col):
    """
    Splits the contents of a column that has lists in python pandas to multiple rows. Puts it in the same column name.
    :param data:
    :param list_col:
    :return:
    """
    temp = pd.DataFrame({
        col: np.repeat(data[col].values, data[list_col].str.len())
        for col in data.columns.difference([list_col])
    }).assign(**{list_col: np.concatenate(data[list_col].values)})[data.columns.tolist()]
    return temp


def report_binary_classification_performance(data, actual_col, prob_col, threshold=0.5):
    """
    Gets is data frame and actual and prediction columns and reports Accuracy, AUC, and Confusion matrix.
    :param data:
    :param actual_col:
    :param prob_col:
    :param threshold:
    :return:
    """
    prob = data[prob_col].values
    actual = data[actual_col].values
    print("Accuracy at %0.2f threshold is %0.2f" % (100 * threshold, 100 * accuracy_score(actual, (prob > threshold).astype(int))))
    print("AUC is %.2f" % (100 * roc_auc_score(actual, prob)))
    print("Here is the confusion matrix")
    print(confusion_matrix(actual, (prob > threshold).astype(int)))
    return roc_auc_score(actual, prob)


def plot_save_roc(input, model_col, actual_col, prob_col, file_name, colors):
    """
    Creates ROC plot of multiple models.
    :param input: the input data frame.
    :param model_col: the column name that specifies model.
    :param actual_col:
    :param prob_col:
    :param file_name:
    :param colors: ad data dictionary with models as the keys and colors and the values.
    :return:
    """

    style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 10))
    for model in input['model'].unique():
        input_subset = input[input[model_col] == model]
        fpr, tpr, _ = roc_curve(input_subset[actual_col], input_subset[prob_col])
        ax.plot(fpr, tpr, lw=1, color=colors[model], linestyle='-', label=model)
    ax.set_title('ROC Curves')
    ax.legend(loc='upper left', facecolor='w')
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.plot([0, 1], [0, 1], color='navy', lw=1, linestyle='--')
    plt.show()
    fig.savefig(file_name, width=300, height=300, dpi=300)


def save_to_pickle_data_path(**kwargs):
    for key, value in kwargs.items():
        pickle.dump(value, open(DATA_PATH + key + ".pkl", "wb"))
    return None


def read_from_pickle_data_path(file_name, DATA_PATH):
    return pickle.load(open(DATA_PATH + file_name + ".pkl", "rb"))


def plot_save_xy_barchart_with_quantiles(df, xcol, ycol, xlabel, ylabel, title, filename=None, q=None):
    """
    Plots a barchart with additional lines to show percentile of the values.
    :param df:
    :param xcol:
    :param ycol:
    :param xlabel:
    :param ylabel:
    :param title:
    :param filename:
    :param q:
    :return:
    """
    df.sort_values(by=[xcol], inplace=True)
    fig, ax = subplots()
    plt.style.use('ggplot')
    ax.bar(x=df[xcol].values, height=df[ycol].values, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    max_y = df[ycol].max() * 0.90
    if q:
        for next_q in q:
            q_val = get_quantile_by_another_column(df=df, col_to_quantile=ycol, col_to_sort_by=xcol, q=next_q)
            ax.axvline(x=q_val, c='red', ls='dashed')
            text(x=q_val + 0.5, y=max_y, s=str(round(100 * next_q, 1)) + " %", rotation=90, verticalalignment='center')
    if filename:
        savefig(filename)
    plt.close()


class MacOSFile(object):

    def __init__(self, f):
        self.f = f

    def __getattr__(self, item):
        return getattr(self.f, item)

    def read(self, n):
        # print("reading total_bytes=%s" % n, flush=True)
        if n >= (1 << 31):
            buffer = bytearray(n)
            idx = 0
            while idx < n:
                batch_size = min(n - idx, 1 << 31 - 1)
                # print("reading bytes [%s,%s)..." % (idx, idx + batch_size), end="", flush=True)
                buffer[idx:idx + batch_size] = self.f.read(batch_size)
                # print("done.", flush=True)
                idx += batch_size
            return buffer
        return self.f.read(n)

    def write(self, buffer):
        n = len(buffer)
        print("writing total_bytes=%s..." % n)
        idx = 0
        while idx < n:
            batch_size = min(n - idx, 1 << 31 - 1)
            print("writing bytes [%s, %s)... " % (idx, idx + batch_size))
            self.f.write(buffer[idx:idx + batch_size])
            print("done.")
            idx += batch_size


def pickle_dump_large(obj, file_path):
    with open(file_path, "wb") as f:
        return pickle.dump(obj, MacOSFile(f), protocol=pickle.HIGHEST_PROTOCOL)


def pickle_load_large(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(MacOSFile(f))
