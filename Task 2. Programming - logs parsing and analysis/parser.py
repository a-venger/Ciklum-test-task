import pandas as pd
import re
import argparse


def reader(filename):
    with open(filename) as f:
        lines = f.readlines()
        result = []
        for line in lines:
			# split log file lines to group by fields
            dd = line.split()
			# Get transaction url
            url = dd[7]
			# Replace dynamic parameters in url
            url = re.sub(r"\?(.*)", "?xxx", url)
			# Get transaction time exclude seconds
            time = dd[4][1:-3]
            result.append([url, time])
        df = pd.DataFrame(result, columns=['Url', 'Time'])

    return df

# Get total amount of transactions
def total_hits(dataframe):
    return dataframe.shape[0]

# Get total hits for each transaction
def total_hits_for_each_transaction(dataframe):
    return dataframe['Url'].value_counts()

# Get total transaction per minute
def max_tpm_total(dataframe):
    return dataframe.groupby('Time').size().values.max()

# Get transaction per minute for each transaction
def max_tpm_for_each_transaction(dataframe):
    max_tpm = {}
    dd = dataframe.groupby('Url')
    for i in dd.groups:
        grouped_by_minute = dd.get_group(i).groupby('Time')
        max_tpm[i] = grouped_by_minute.size().values.max()

    return max_tpm


def get_result(dataframe):
    resultframe = pd.DataFrame(total_hits_for_each_transaction(dataframe))
	# Add percentage column to dataframe
    resultframe['Percentage'] = resultframe['Url'] / total_hits(dataframe) * 100
	# Add max_tpm column to dataframe
    resultframe['Max_TPM'] = pd.Series(max_tpm_for_each_transaction(dataframe))
    resultframe.rename(columns={'Url': 'Hits'}, inplace=True)

	# Add Total row to result dataframe
    resultframe.loc['Total'] = [total_hits(dataframe), 100, max_tpm_total(dataframe)]
	# Write result dataframe to csv file
    resultframe.to_csv('myDataFrame.csv')

	# Write total result to console
    print("Total hits = " + str(total_hits(dataframe)) + ", max_tpm_all_transactions = "
          + str(max_tpm_total(dataframe)))

	# Write result for each transaction to console
    for index, row in resultframe.iterrows():
        print (index + " Total hits = " + str(row['Hits']) + " , percentage = " + "{0:.2f}% ".format(row['Percentage'])
               + "% , max_TPM = " + str(row['Max_TPM']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', type=str, help="path to log file to parse",
                        default='access.log')
    args = parser.parse_args()
    get_result(reader(args.filename))
