import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score



def total_waste():
    df = pd.read_csv("DSNY_Monthly_Tonnage_Data.csv")
    columns_to_drop = ["BOROUGH_ID"]
    df = df.drop(columns = columns_to_drop)
    waste_cols = ["REFUSETONSCOLLECTED", "PAPERTONSCOLLECTED", "MGPTONSCOLLECTED",
                              "RESORGANICSTONS", "SCHOOLORGANICTONS", "LEAVESORGANICTONS",
                              "XMASTREETONS"]
    '''
    create new col called Total_waste, which is the sum of all the waste_col value in each row.
    '''
    df['Total_waste'] = df[waste_cols].sum(axis=1)


    return df

def agg_by_month_boro():
    '''
    group the MONTH and BOROUGH and sum the Total_waste col so we can get total waste for the whole BOROUGH including all the different
    '''
    df = total_waste()
    grouped_df = df.groupby(["MONTH", "BOROUGH"])["Total_waste"].sum().reset_index()
    grouped_df['MONTH'] = pd.to_datetime(grouped_df['MONTH'], format='%Y / %m')
    return grouped_df



def rat_report():
    '''
    update the dataframe to only contain the listed columns
    '''
    selected_cols = ['Created Date', 'Closed Date', 'Incident Address', 'Borough', "Descriptor"]
    df = pd.read_csv("Rat_Sightings.csv", usecols = selected_cols)
    return df

def filter_rat_report():
    '''
    drop all the rows where the key word "Rat Sighting" does not appear in the descriptor col. This is because
    we just reports for rat sighting nothing else.
    '''
    rat_df = rat_report()

    #update df to only rows where Rat Sighting appear in Descriptor col
    rat_df = rat_df[rat_df["Descriptor"].str.contains("Rat Sighting")]


    rat_df['Created Date'] = pd.to_datetime(rat_df['Created Date'], format='%m/%d/%Y %I:%M:%S %p')

    # Extract only the date portion
    rat_df['Created Date'] = rat_df['Created Date'].dt.date

    # delete duplicated row is the values matches in both Created Date and Borough, if the ticket is create
    # on the same day at same address might be same rat so we just delete the duplicate to improve accuracy.
    rat_df.drop_duplicates(subset=['Created Date', 'Incident Address'], inplace=True)

    return rat_df


# def rat_total():
#     '''

#     '''
#     df = filter_rat_report()
#     df = df.drop_duplicates(subset=['Created Date', 'Borough'])

#     # Convert 'Created_Date' to datetime format
#     df['Created Date'] = pd.to_datetime(df['Created Date'])


#     return df





def main():
    df = total_waste()
    df = rat_report()
    df = filter_rat_report()
    # df = rat_total()



    #-------------------------------------------------------------------------------------------------
    # # Plotting
    # '''
    # Figure 1. Shows the total_waste each borough collected each year. Conclusion: There has not been an great increase in waste over each year,relatively
    # the same amount of waste in each borough each year.
    # '''
    # grouped_df = agg_by_month_boro()

    # plt.figure(figsize=(10, 6))
    # for borough, group in grouped_df.groupby('BOROUGH'):
    #     plt.plot(group['MONTH'].values, group['Total_waste'].values, label=borough)

    # plt.title('Total Waste by Borough Over Time')
    # plt.xlabel('Month')
    # plt.ylabel('Total Waste')
    # plt.legend()
    # plt.grid(True)
    # plt.show()


if __name__ == "__main__":
    main()
