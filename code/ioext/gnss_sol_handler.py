from config.configutil import getpath
import pandas as pd
import matplotlib.pyplot as plt


def loadsol(name):
    solpath = getpath("rtksolpath")
    df = pd.read_csv(solpath + name,
                     names=['week', 'tow', 'north', 'east', 'up', 'q', 'ns', 'sdn', 'sde', 'sdu', 'sdene', 'sdeu',
                            'sdun', 'age', 'ratio'], engine='python')
    return df


if __name__ == '__main__':
    df = loadsol('rover_bd9_3_enu.pos')
    plt.subplot(3, 1, 1)
    plt.plot(df.loc[:, 'tow'], df.loc[:, 'north'])
    plt.subplot(3, 1, 2)
    plt.plot(df.loc[:, 'tow'], df.loc[:, 'east'])
    plt.subplot(3, 1, 3)
    plt.plot(df.loc[:, 'tow'], df.loc[:, 'up'])
    plt.show()
