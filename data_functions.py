# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 15:30:21 2024

@author: Lukáš
"""
import pandas as pd
import numpy as np
import streamlit as st
from ions import *
from io import BytesIO

#function definitions

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def make_theoretical(theor_upload):
    """Reads uploaaded file with theoretical values and adds columns with ion name and and molecule ID"""
    try:
        theor_df = pd.read_excel(theor_upload)
    except ValueError:
        theor_df = pd.read_csv(theor_upload)
    orig_cols = list(theor_df.columns)
    new_cols = ['name', 'm/z']
    col_dict = dict(zip(orig_cols,new_cols))
    theor_df = theor_df.rename(columns=col_dict)
    theor_df['ID'] = theor_df.index+1
    theor_df['ion'] = 'orig_M'
    cols_list_reindex = ['name', 'm/z', 'ID','ion','charge','warning']
    cols_list_ordered = ['name','ID','ion','charge','m/z','warning']
    theor_df = theor_df.reindex(columns=cols_list_reindex)
    theor_df = theor_df[cols_list_ordered]
    return theor_df

def make_experimental(exp_upload):
    exp_dfs_table=pd.DataFrame()        # for storing additional data about dataframes (exp_err, abund_thrs,...)
    exp_dfs={}                          # for storing imported dataframes
    exp_dfs_names = {}                  # only needed for dropdown menu
    i=0                                 # to produce consecutive numbering for uploaded files
    for filename in exp_upload:
        i+=1
        nick = 'file'+str(i)
        try:
            exp_dfs[nick] = pd.read_excel(filename)
        except ValueError:
            exp_dfs[nick] = pd.read_csv(filename)
        orig_cols = list(exp_dfs[nick].columns)
        new_cols = ['exp_m/z', 'Abundance']
        col_dict = dict(zip(orig_cols,new_cols))
        exp_dfs[nick] = exp_dfs[nick].rename(columns=col_dict)
        exp_dfs_names[str(filename.name)]= nick 
        # fill the table
        exp_dfs_table.loc[len(exp_dfs_table.index),'nickname'] = nick
        exp_dfs_table.set_index('nickname', drop=False, inplace=True)
        exp_dfs_table.loc[nick,'orig_name'] = str(filename.name) 
    # these has to be added to have the columns in the dataframe. Otherwise it cannot be edited
    exp_dfs_table['exp_err']=np.nan
    exp_dfs_table['abund_thrs']=np.nan
    return (exp_dfs_table, exp_dfs, exp_dfs_names)




def add_ions(theor_df, ion_list, exp_err):
    """Prepares full table of theoretical masses by adding chosen ions to the table of theoretical m/z values"""
    # first make empty dataframe
    theor_df_full = pd.DataFrame()
    try:
        # add ions which are set by user as True (tick in a checkbox)
        for ion in ion_list:
            if ion['add_to_df']:
                ion_df = theor_df.copy()
                ion_df['charge'] = ion['charge']
                ion_df['m/z'] = ion_df['m/z']*ion['multiply_by']+ion['add_mass']
                ion_df['ion'] = ion['ion']
                theor_df_full = pd.concat([theor_df_full, ion_df], ignore_index=True)
            else:
                pass
        # sort the full theoretical mass table by m/z
        theor_df_full.sort_values(by='m/z', inplace = True,ignore_index=True)
        # calculate differences between lines and give warning where the difference is smaller 
        # than the double of the defined experimental error(exp_err)
        exp_err = 2*exp_err
        theor_df_full['diff'] = theor_df_full['m/z'].diff()
        theor_df_full['diff2'] = theor_df_full['m/z'].diff(periods=-1)
        theor_df_full['diff2'] = -theor_df_full['diff2']
        theor_df_full.loc[theor_df_full['diff']<exp_err, 'warning'] = 'Possibility of wrong matching! Difference from previous or following m/z in full theoretical table is lower than the largest mass accuracy value set by user'
        theor_df_full.loc[theor_df_full['diff2']<exp_err, 'warning'] = 'Possibility of wrong matching! Difference from previous or following m/z in full theoretical table is lower than the largest mass accuracy value set by user'
        # rearrange columns and keep only necessary ones
        theor_df_full = theor_df_full[['name','ID','ion','charge','m/z','warning']]
        return theor_df_full
    except:
        theor_df_full = theor_df_full.reindex(columns=['name','ID','ion','charge','m/z','warning'])
        return theor_df_full


    

def match_data(exp_dfs_table, exp_dfs, theor_df_full):
    """Will match experimental data with theoretical m/z values and return new matched dataframes and one dataframe with overal results""" 
    try:
        orig_cols_theor = list(theor_df_full.columns)
        new_cols_theor = ['name','ID','ion','charge','theor_m/z','warning']
        col_dict_theor = dict(zip(orig_cols_theor,new_cols_theor))
        theor_df_full = theor_df_full.rename(columns=col_dict_theor)
        all_in_one = pd.DataFrame()
        n = 1
        exp_dfs_matched = {}
        # loop through the files and do the matching
        for ind in exp_dfs_table.index:
            # define variables
            exp_data = exp_dfs[ind]
            abundance_threshold = exp_dfs_table.loc[ind,'abund_thrs']
            tolerance_of_mass = exp_dfs_table.loc[ind,'exp_err']
            orig_datafile_name = exp_dfs_table.loc[ind,'nickname']
            
            # ensure the correct names of columns
            orig_cols_data = list(exp_data.columns)
            columns_in_data = ['exp_m/z','Abund']
            col_dict_exp = dict(zip(orig_cols_data,columns_in_data))
            exp_data = exp_data.rename(columns=col_dict_exp)
    
            # sort data by m/z
            exp_data = exp_data.sort_values(by=['exp_m/z']).reset_index(drop = True)
            
            # keep only rows with abundance over the set value for variable abundance_threshold 
            exp_data= exp_data[exp_data['Abund']>=abundance_threshold]    
            
            # find best fits for experimental values from table of theoretical values, rearrange columns
            compared_data = pd.merge_asof(exp_data, theor_df_full, 
                                          left_on ='exp_m/z', right_on = 'theor_m/z', 
                                          tolerance = tolerance_of_mass, direction = 'nearest',allow_exact_matches=True)
            
            # rearrange columns in paired table
            compared_data = compared_data[['theor_m/z','exp_m/z','ID','name','ion','charge','Abund','warning']]
        
            # drop all experimental data which did not have a paired theoretical oligomer or macrocycle
            compared_data = compared_data.dropna(subset=['theor_m/z'])
    
            #sort table which contains only paired values according to the ID and m/z
            compared_data = compared_data.sort_values(by=['ID','theor_m/z']).reset_index(drop = True)
            
            # add column with orginal datafile name at each row
            compared_data['orig_file'] = orig_datafile_name
            
            # save compared data for the file to the exp_dfs_matched
            exp_dfs_matched[ind] = compared_data.copy()
            
            # edit column with orginal datafile name so it would be clear that it contains abundance after the pivoting of table
            compared_data['orig_file'] = orig_datafile_name + '_abund'
    
            ###########################################################################################################
            
            # go through all lines and make new column corresponding with name of a file and value of abundance sum for all found ions
            for i in range(theor_df_full['ID'].max()+1):
                data_subset = compared_data[compared_data['ID']==i]
                if len(data_subset)>0:
                    # save values to variables
                    name_from_subset = list(data_subset['name'])
                    orig_file_from_subset = list(data_subset['orig_file'])
                    # initiate new dataframe
                    oneline = pd.DataFrame()
                    # add values to all columns
                    oneline.loc[0,'theor_m/z'] = np.nan
                    oneline.loc[0,'exp_m/z'] = np.nan
                    oneline.loc[0,'ID'] = i
                    oneline.loc[0,'name'] = name_from_subset[0]
                    oneline.loc[0,'ion'] = 'ions sum'
                    oneline.loc[0,'charge'] = np.nan
                    oneline.loc[0,'Abund'] = data_subset['Abund'].sum()
                    oneline.loc[0,'warning'] = 'this line contains sum of abundances within particular file and molecule ID'
                    oneline.loc[0,'orig_file'] = orig_file_from_subset[0]
                    compared_data = pd.concat([compared_data,oneline],ignore_index=True)
                else:
                    pass
                
            # cast ID as integer and sort the dataframe again
            compared_data['ID']=compared_data['ID'].astype('int32')
            compared_data = compared_data.sort_values(by=['ID','theor_m/z']).reset_index(drop = True)
    
            # collect the data to one dataframe with full results
            all_in_one = pd.concat([all_in_one,compared_data], ignore_index=True)
    
            #increase count
            n+=1
        
        ######################################################################################################################    
        
        # add column with calculated average m/z and its standard deviation for each molecule throughout all files
        all_in_one['mean_m/z'] = all_in_one.groupby(['ID','ion'])["exp_m/z"].transform('mean').round(4)
        all_in_one['std_err_m/z'] = all_in_one.groupby(['ID','ion'])["exp_m/z"].transform('std').round(4)
        all_in_one['std_err_m/z'] = all_in_one['std_err_m/z'].fillna(value = 0.0000)  
        for lab,row in all_in_one.iterrows():
            all_in_one.loc[lab,'exp_mean_m/z'] = str(row['mean_m/z'])+" ± "+str(row['std_err_m/z'])    
        
        # pivot the results from long format to wide format
        # first it is necessary to fill all nan values because pivot_table function would remove these important rows
        all_in_one = all_in_one.fillna('empty')
        all_in_one = all_in_one.pivot_table(columns = 'orig_file', 
                                      values = 'Abund', 
                                      index = ['theor_m/z','ID','name','ion','charge','warning', 'exp_mean_m/z'], 
                                      aggfunc='sum',
                                      sort = False).reset_index(drop = False)
        
        # replace 'nan +- 0' in the mean m/z values
        all_in_one = all_in_one.replace(to_replace = ["nan ± 0.0", "empty"], value = [np.nan, np.nan])
        # sort the values
        all_in_one = all_in_one.sort_values(by=['ID','theor_m/z']).reset_index(drop = True)
        # rearrange columns in aggregated table
        all_in_one = all_in_one[[col for col in all_in_one.columns if col != 'warning'] + ['warning']]
        return (theor_df_full, exp_dfs_matched, all_in_one, 'Matches were found!')
    except:
        return (pd.DataFrame(),pd.DataFrame(),pd.DataFrame(), 'Something went wrong! Have you uploaded all necessary files? You can try to set larger mass accuracy value, add ions, check your data. Maybe, there are no matches anyway!')

    
    
    


def download_excel(exp_dfs_table, theor_df_full, all_in_one, exp_dfs_matched):
    # buffer to use for excel writer
    buffer = BytesIO()
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write each dataframe to a different worksheet.
        exp_dfs_table.to_excel(writer, sheet_name='overview')
        theor_df_full.to_excel(writer, sheet_name='theoretical_table')
        all_in_one.to_excel(writer, sheet_name='aggregated_results')
        # loop through the matched exps and make one sheet for each df
        for key,df in exp_dfs_matched.items():
            df.to_excel(writer, sheet_name=key)
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
    return buffer



def counter_fc():
    # add counter of downloaded files    
    with open("counter.txt", "r") as f:
        a = f.readline()  # starts as a string
        a = int(a)  # cast using int()
    a += 1  
    with open("counter.txt", "w") as f:
        f.truncate()
        f.write(f"{a}")



def show_counter():
    counter =  open("counter.txt", "r")
    counter_count =  counter.readline()  # it is a string
    return counter_count
        
    
