import pandas as pd
import matplotlib.pyplot as plt

def prep_data():
    #read datasets
    account = pd.read_csv('../data/account.csv',na_values = ['NA'],delimiter=";")
    card_train = pd.read_csv('../data\card_train.csv',na_values = ['NA'],delimiter=";")
    client = pd.read_csv('../data\client.csv',na_values = ['NA'],delimiter=";")
    disp = pd.read_csv('../data\disp.csv',na_values = ['NA'],delimiter=";")
    district = pd.read_csv('../data\district.csv',na_values = ['NA'],delimiter=";")
    loan_train = pd.read_csv('../data\loan_train.csv',na_values = ['NA'],delimiter=";")
    trans_train = pd.read_csv('../data/trans_train.csv', dtype={'bank' : 'str'}, na_values = ['NA'],delimiter=";")
    
    #join together loan_train and account and rename the columns with the same name
    account.rename(columns={'date': 'account_date'}, inplace=True)
    loan_train.rename(columns={'date': 'loan_date'}, inplace=True)
    loan_account = pd.merge(loan_train, account, on="account_id")

    #rename columns
    district.rename(columns={'no. of inhabitants': 'inhabitants','no. of municipalities with inhabitants < 499 ':'inhabitants < 499' ,'no. of municipalities with inhabitants 500-1999':'inhabitants 500-1999', 'no. of municipalities with inhabitants 2000-9999 ':'inhabitants 2000-9999','no. of municipalities with inhabitants >10000 ': 'inhabitants >10000', "unemploymant rate '95 ":'unemploymant 95', "unemploymant rate '96 ":'unemploymant 96', 'no. of enterpreneurs per 1000 inhabitants ':'enterpreneurs',"no. of commited crimes '95 ":'crimes 95', "no. of commited crimes '96 ":'crimes 96'}, inplace=True)
    #replace question marks by mean value of column
    replace_dict = {'unemploymant 95': {'?': pd.to_numeric(district['unemploymant 95'], errors="coerce").mean()},
                    'crimes 95': {'?': pd.to_numeric(district['crimes 95'], errors="coerce").mean()}}
    district.replace(replace_dict, inplace = True)
    
    #join loan_account with district
    loan_account_district = pd.merge(loan_account, district, left_on="district_id", right_on="code ")
    #remove unuseful columns
    loan_account_district.drop(['loan_id', 'district_id', 'code ', 'name '], axis=1, inplace=True)
    #replace string values with numerical values for analysis
    freq = {'monthly issuance': 1, "weekly issuance": 2, "issuance after transaction": 3}
    loan_account_district.frequency = [freq[i] for i in loan_account_district.frequency]
    reg ={"south Moravia": 1, "north Moravia": 2, "Prague": 3, "central Bohemia": 4, "east Bohemia": 5,"west Bohemia": 6, "south Bohemia": 7, "north Bohemia": 8}
    loan_account_district.region = [reg[i] for i in loan_account_district.region]
    
    return loan_account_district

print(prep_data().columns)
#join disp and card_train
#card_train.drop(['card_id', 'issued'], axis = 1, inplace=True)
#ard_train.rename(columns={'type': 'card_type'}, inplace=True)
#disp.rename(columns={'type': 'disp_type'}, inplace=True)
#disp_card = pd.merge(disp, card_train, on="disp_id")
#disp_card.drop('disp_id', axis = 1, inplace=True)
#print(disp_card.columns)
#disp_card.groupby('account_id')