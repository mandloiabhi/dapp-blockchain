import matplotlib.pyplot as plt


def draw_graph(noOfTxn,ratioOfTxn):
    plt.plot(noOfTxn, ratioOfTxn, color='red', linewidth = 3, marker='o', markerfacecolor='blue', markersize=12)
    plt.xlabel('Number of Transaction')
    plt.ylabel('Ratio of successful TXN by total TXN')
    plt.xlim(100,1000)
    plt.ylim(0.3,1.0)

    plt.show()