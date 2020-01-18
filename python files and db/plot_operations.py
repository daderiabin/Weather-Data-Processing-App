"""Plot Building For The Project by Danylo Deriabin."""

import matplotlib.pyplot as plt


class PlotOperations():
    """Build a plot."""

    def builder(self, dict, y1, y2):
        """Build a Plot."""
        data = []
        for v in dict.values():
            data.append(v)

        fig1, ax1 = plt.subplots()
        ax1.set_title('Monthly Temperature Distribution from ' + y1 + " to " + y2)
        ax1.set_ylabel('Temperature (Celsius)')
        ax1.set_xlabel('Months')
        plt.boxplot(data, showfliers=False)

        plt.show()


if __name__ == '__main__':
    plot = PlotOperations()
