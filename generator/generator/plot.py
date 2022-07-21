import matplotlib.pyplot as plt
import numpy as np


# plot bar chart
def plot_bar(data, labels, x_label, y_label, title, file_name):
    # set up plot
    fig, ax = plt.subplots()
    ax.bar(np.arange(len(data)), data)
    ax.set_xticks(np.arange(len(data)), labels)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    fig.tight_layout()

    # save plot
    fig.savefig(file_name)
    plt.show()
    plt.close(fig)
