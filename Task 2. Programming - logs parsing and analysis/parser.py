import pandas as pd
import re


def reader(filename):
    with open(filename) as f:
        lines = f.readlines()
        result = []
        for line in lines:
            dd = line.split()
            url = dd[7]
            url = re.sub(r"\?(.*)", "?xxx", url)
            time = dd[4][1:-3]
            result.append([url, time])
        df = pd.DataFrame(result, columns=['Url', 'Time'])

    return df


def total_hits(dataframe):
    return dataframe.shape[0]


def total_hits_for_each_transaction(dataframe):
    return dataframe['Url'].value_counts()


def max_tpm_total(dataframe):
    return dataframe.groupby('Time').size().values.max()


def max_tpm_for_each_transaction(dataframe):
    max_tpm = {}
    dd = dataframe.groupby('Url')
    for i in dd.groups:
        grouped_by_minute = dd.get_group(i).groupby('Time')
        max_tpm[i] = grouped_by_minute.size().values.max()

    return max_tpm


def get_result(dataframe):
    resultframe = pd.DataFrame(total_hits_for_each_transaction(dataframe))
    resultframe['Percentage'] = resultframe['Url'] / total_hits(dataframe) * 100
    resultframe['Max_TPM'] = pd.Series(max_tpm_for_each_transaction(dataframe))
    resultframe.rename(columns={'Url': 'Hits'}, inplace=True)

    resultframe.loc['Total'] = [total_hits(dataframe), 100, max_tpm_total(dataframe)]
    resultframe.to_csv('myDataFrame.csv')

    print("Total hits = " + str(total_hits(dataframe)) + ", max_tpm_all_transactions = "
          + str(max_tpm_total(dataframe)))

    for index, row in resultframe.iterrows():
        print (index + " Total hits = " + str(row['Hits']) + " , percentage = " + "{0:.2f}% ".format(row['Percentage'])
               + "% , max_TPM = " + str(row['Max_TPM']))


if __name__ == '__main__':
    get_result(reader('test.log'))
