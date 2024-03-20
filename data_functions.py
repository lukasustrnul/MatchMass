# -*- coding: utf-8 -*-
"""
Author: Lukáš Ustrnul
GitHub: https://github.com/lukasustrnul
LinkedIn: https://www.linkedin.com/in/luk%C3%A1%C5%A1-ustrnul-058420123/

File: data_functions.py
Created on 15.03.2024

Note: definitions for functions which manipulates the data
"""
import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO
import ions_enum


def read_excel_or_csv(file_from_upload_object: st.runtime.uploaded_file_manager.UploadedFile) -> pd.DataFrame:
    """
    reads CSV or Excel file to a dataframe

    @param file_from_upload_object: a Streamlit UploadedFile object
    @return: pd.DataFrame
    """
    try:
        df_from_uploaded_file = pd.read_excel(file_from_upload_object)
    except ValueError:
        df_from_uploaded_file = pd.read_csv(file_from_upload_object)
    return df_from_uploaded_file


def rename_original_columns(df: pd.DataFrame, new_column_names: list[str]) -> pd.DataFrame:
    """
    takes DataFrame and renames its columns to desired names

    @param df:
    @param new_column_names: list of new column names
    @return: original dataframe with renamed columns
    """
    columns_dict = dict(zip(list(df.columns), new_column_names))
    df = df.rename(columns=columns_dict)
    return df


def additional_columns_to_theoretical_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    function will add necessary columns to df with theoretical monoisotopic masses.
    1. For each row (should correspond to unique mass and molecule) is added ID number
    2. Name of ions is set to Orig_M indicating it is original mass provided by user.
    3. Columns for charge and warning are added
    4. columns are rearranged to desired order

    @param df: theoretical values dataframe containing 2 original renamed columns
    @return: theoretical values dataframe extended with new columns ('ID','ion','charge','warning')
        and rearranged to desired order ('name','ID','ion','charge','theor_m/z','warning')
    """
    df['ID'] = df.index+1   # ID numbers starts with 1
    df['ion'] = 'orig_M'
    cols_list_reindex = ['name', 'ID', 'ion', 'charge', 'theor_m/z', 'warning']
    df = df.reindex(columns=cols_list_reindex)
    return df


def generate_additional_info_table(df: pd.DataFrame, filename: st.runtime.uploaded_file_manager.UploadedFile, nick: str) -> pd.DataFrame:
    """
    add new row and values to the df which holds additional information about experimental files

    @param df: df_experimental_dfs_additional_info
    @param filename: one of the files uploaded by user in a form of UploadedFile object
    @param nick: nickname of the file for further processing
    @return: df_experimental_dfs_additional_info extended by one new row
    """
    df.loc[len(df.index), 'nickname'] = nick
    df.set_index('nickname', drop=False, inplace=True)
    df.loc[nick, 'orig_name'] = str(filename.name)
    # Add columns for mass accuracy and abundance threshold to the df with additional information.
    # Columns has to be added before allowing user to input the values.
    df['mass_accuracy(Da)'] = np.nan
    df['abund_thrs'] = np.nan
    return df


def theoretical_upload_object_to_dataframe(theoretical_table_UploadedFile_object: st.runtime.uploaded_file_manager.UploadedFile) -> pd.DataFrame:
    """
    Reads uploaded file with theoretical values and ads columns with ion name and molecule ID etc.

    @param theoretical_table_UploadedFile_object: file with theoretical monoisotopic masses uploaded by user
    @return: dataframe with table of theoretical monoisotopic masses, molecule names and newly generated ID numbers for each molecule
    """
    theoretical_mass_table_df = read_excel_or_csv(theoretical_table_UploadedFile_object)

    theoretical_mass_table_df = rename_original_columns(theoretical_mass_table_df, ['name', 'theor_m/z'])

    theoretical_mass_table_df = additional_columns_to_theoretical_table(theoretical_mass_table_df)

    return theoretical_mass_table_df


def extract_info_and_data_from_experimental_upload(experimental_UploadedFile_object: st.runtime.uploaded_file_manager.UploadedFile) -> tuple:
    """
    Reads uploaded file with experimental results, then renames columns to correct names.
    For each uploaded experimental file is given nickname to avoid problems with multiple files having the same name.
    dataframes containing experimental files are collected in a dictionary
    Additionally, a dictionary with original names is generated for future use in dropdown menu
    Finally, a dataframe keeping process information for all experimental files is generated

    @param experimental_UploadedFile_object: Experimental files uploaded by user
    @return: tuple (pd.DataFrame, dict[UploadedFile]=pd.DataFrame, dict[orig_filename]= file_nickname )
    """
    # initiate variables (dataframe and dictionaries)
    experimental_dfs_additional_info_df = pd.DataFrame()               # for storing additional data about dataframes (mass_accuracy, abund_thrs,...)
    dict_containing_experimental_dfs = {}                              # dictionary for storing imported dataframes
    dict_experimental_filenames = {}                                   # only needed for dropdown menu
    i = 0                                                              # to produce consecutive numbering for uploaded files

    for filename in experimental_UploadedFile_object:
        # add count and generate new nickname for a file
        i += 1
        nick = 'file'+str(i)

        # read experimental data and rename columns
        dict_containing_experimental_dfs[nick] = read_excel_or_csv(filename)
        dict_containing_experimental_dfs[nick] = rename_original_columns(dict_containing_experimental_dfs[nick], ['exp_m/z', 'Abundance'])

        # save original file name with new nick to a dictionary for dropdown menu
        dict_experimental_filenames[str(filename.name)] = nick

        # fill the table containing additional information
        experimental_dfs_additional_info_df = generate_additional_info_table(experimental_dfs_additional_info_df, filename, nick)

    return (experimental_dfs_additional_info_df, dict_containing_experimental_dfs, dict_experimental_filenames)


def add_ions_to_theoretical_table(theoretical_mass_table_df: pd.DataFrame, ions_to_add_to_theoretical_table_dict: dict) -> pd.DataFrame:
    """
    Prepares full table of theoretical masses by adding chosen ions to the table of theoretical m/z values

    @param theoretical_mass_table_df: table containing only original masses as provided by user
    @param ions_to_add_to_theoretical_table_dict: dictionary where keys are names of ions from ions_enum.Ion and values are booleans
    @return: expanded_theoretical_mass_table_df which contains only theor_m/z values for ions of interest which will be matched with experimental data in further steps
    """
    # first make empty dataframe
    expanded_theoretical_mass_table_df = pd.DataFrame()
    try:
        # add ions which are set by user as True (tick in a checkbox)
        for ion in ions_enum.Ion:
            if ions_to_add_to_theoretical_table_dict[ion.name]:
                ion_df = theoretical_mass_table_df.copy()
                ion_df['charge'] = ion.value.charge
                ion_df['theor_m/z'] = ion_df['theor_m/z'] * ion.value.multiply_by + ion.value.add_mass
                ion_df['ion'] = ion.value.ion_formula
                expanded_theoretical_mass_table_df = pd.concat([expanded_theoretical_mass_table_df, ion_df], ignore_index=True)
            else:
                pass
        # sort the full theoretical mass table by theor_m/z
        expanded_theoretical_mass_table_df.sort_values(by='theor_m/z', inplace=True, ignore_index=True)
        # rearrange columns and keep only necessary ones
        expanded_theoretical_mass_table_df = expanded_theoretical_mass_table_df[['name', 'ID', 'ion', 'charge', 'theor_m/z', 'warning']]
        return expanded_theoretical_mass_table_df
    except:
        expanded_theoretical_mass_table_df = expanded_theoretical_mass_table_df.reindex(columns=['name', 'ID', 'ion', 'charge', 'theor_m/z', 'warning'])
        return expanded_theoretical_mass_table_df


def raise_warning_for_masses_within_accuracy(expanded_theoretical_mass_table_df: pd.DataFrame, max_mass_accur_value: float) -> pd.DataFrame:
    """
    adds warning to lines of theoretical masses which are within mass accuracy range; therefore, can be wrongly matched

    @param expanded_theoretical_mass_table_df:
    @param max_mass_accur_value:
    @return: dataframe with filled warning at rows where is risk of wrong matching due to theor_m/z being within mass accuracy range
    """
    # calculate differences between lines and give warning where the difference is smaller
    # than the double of the defined mass accuracy(mass_accur_value)
    exp_err = 2 * max_mass_accur_value
    expanded_theoretical_mass_table_df['diff'] = expanded_theoretical_mass_table_df['theor_m/z'].diff()
    expanded_theoretical_mass_table_df['diff2'] = expanded_theoretical_mass_table_df['theor_m/z'].diff(periods=-1)
    expanded_theoretical_mass_table_df['diff2'] = -expanded_theoretical_mass_table_df['diff2']
    expanded_theoretical_mass_table_df.loc[expanded_theoretical_mass_table_df[
                                               'diff'] < exp_err, 'warning'] = 'Possibility of wrong matching! Difference from previous or following theor_m/z in full theoretical table is lower than the largest mass accuracy value set by user'
    expanded_theoretical_mass_table_df.loc[expanded_theoretical_mass_table_df[
                                               'diff2'] < exp_err, 'warning'] = 'Possibility of wrong matching! Difference from previous or following theor_m/z in full theoretical table is lower than the largest mass accuracy value set by user'
    # rearrange columns and keep only necessary ones (diff and diff2 are just helping columns to raise warning)
    expanded_theoretical_mass_table_df = expanded_theoretical_mass_table_df[
        ['name', 'ID', 'ion', 'charge', 'theor_m/z', 'warning']]
    return expanded_theoretical_mass_table_df


def determine_bar_width(max_mass_accur_value: float) -> float:
    """
    Provides bar width for plotting of theoretical m/z values based on mass accuracy or arbitrary value if mass accuracy is None

    @param max_mass_accur_value: maximum defined value of mass accuracy for any dataframe with experimental values
    @return: value of bar width
    """
    if max_mass_accur_value > 0:
        width_for_theoretical_mz_bars = 2 * max_mass_accur_value
    else:
        width_for_theoretical_mz_bars = 0.005
    return width_for_theoretical_mz_bars


def get_values_from_additional_info_df(experimental_dfs_additional_info_df: pd.DataFrame, ind: str) -> tuple:
    """

    @param experimental_dfs_additional_info_df:
    @param ind: index which corresponds to nickname of file containing experimental results
    @return: tuple of values
    """
    abundance_threshold = experimental_dfs_additional_info_df.loc[ind, 'abund_thrs']
    tolerance_of_mass = experimental_dfs_additional_info_df.loc[ind, 'mass_accuracy(Da)']
    orig_datafile_nickname = experimental_dfs_additional_info_df.loc[ind, 'nickname']
    return (abundance_threshold, tolerance_of_mass, orig_datafile_nickname)


def prepare_experimental_for_matching(single_exp_file_df: pd.DataFrame, abundance_threshold: float) -> pd.DataFrame:
    """
    Prepares data before matching by sorting them and by removing signals of low abundance

    @param single_exp_file_df:
    @param abundance_threshold:
    @return: alternated version of dataframe
    """
    # sort data by m/z
    single_exp_file_df = single_exp_file_df.sort_values(by=['exp_m/z']).reset_index(drop=True)

    # keep only rows with abundance over the set value for variable abundance_threshold
    single_exp_file_df = single_exp_file_df[single_exp_file_df['Abundance'] >= abundance_threshold]
    return single_exp_file_df


def match_experimental_with_theoretical(single_exp_file_df: pd.DataFrame,
                                        expanded_theoretical_mass_table_df: pd.DataFrame,
                                        tolerance_of_mass: float
                                        ) -> pd.DataFrame:
    """
    Matches rows with theoretical and experimental m/z values within defined mass accuracy.

    @param single_exp_file_df:
    @param expanded_theoretical_mass_table_df:
    @param tolerance_of_mass:
    @return: dataframe with matched rows
    """
    compared_data_raw = pd.merge_asof(single_exp_file_df,
                                      expanded_theoretical_mass_table_df,
                                      left_on='exp_m/z',
                                      right_on='theor_m/z',
                                      tolerance=tolerance_of_mass,
                                      direction='nearest',
                                      allow_exact_matches=True)
    return compared_data_raw


def process_raw_compared_data(compared_data_raw: pd.DataFrame, orig_datafile_nickname: str) -> pd.DataFrame:
    """
    Performs simple transformations to rearrange dataframe to final shape.
    Transformations are following:
    1. rearrange and keep only columns of interest
    2. drop experimental values without matching theoretical m/z
    3. sorts rows by ID and theoretical m/z
    4. adds information about file of data origin

    @param compared_data_raw: unprocessed dataframe with matched results
    @param orig_datafile_nickname:
    @return: processed df with matched results
    """
    # rearrange columns to final order and drop columns which are not of interest
    compared_data = compared_data_raw[['theor_m/z', 'exp_m/z', 'ID', 'name', 'ion', 'charge', 'Abundance', 'warning']]

    # drop all experimental data which did not have a paired theoretical oligomer or macrocycle
    compared_data = compared_data.dropna(subset=['theor_m/z'])

    # sort table which contains only paired values according to the ID and m/z
    compared_data = compared_data.sort_values(by=['ID', 'theor_m/z']).reset_index(drop=True)

    # add column with original datafile name at each row
    compared_data['orig_file'] = orig_datafile_nickname

    return compared_data


def add_total_abundance_row_within_id(compared_data: pd.DataFrame, i: int) -> pd.DataFrame:
    """
    Adds a row with total abundance of all ions related to the molecule with particular ID number(i).
    ID numbers which are not present in the dataframe are skipped.

    @param compared_data:
    @param i: ID number of a molecule
    @return: dataframe compared data with one added line containing sum of abundances
    """
    data_subset = compared_data[compared_data['ID'] == i]
    if len(data_subset) > 0:
        # save values to variables
        name_from_subset = list(data_subset['name'])
        orig_file_from_subset = list(data_subset['orig_file'])
        # initiate new dataframe
        new_row_for_subset_total_abundance = pd.DataFrame()
        # add values to all columns
        new_row_for_subset_total_abundance.loc[0, 'theor_m/z'] = np.nan
        new_row_for_subset_total_abundance.loc[0, 'exp_m/z'] = np.nan
        new_row_for_subset_total_abundance.loc[0, 'ID'] = i
        new_row_for_subset_total_abundance.loc[0, 'name'] = name_from_subset[0]
        new_row_for_subset_total_abundance.loc[0, 'ion'] = 'ions sum'
        new_row_for_subset_total_abundance.loc[0, 'charge'] = np.nan
        new_row_for_subset_total_abundance.loc[0, 'Abundance'] = data_subset['Abundance'].sum()
        new_row_for_subset_total_abundance.loc[0, 'warning'] = 'this line contains sum of abundances within particular file and molecule ID'
        new_row_for_subset_total_abundance.loc[0, 'orig_file'] = orig_file_from_subset[0]
        compared_data = pd.concat([compared_data, new_row_for_subset_total_abundance], ignore_index=True)
    else:
        pass
    return compared_data


def prepare_matched_exp_file_for_aggregating(compared_data: pd.DataFrame, expanded_theoretical_mass_table_df: pd.DataFrame) -> pd.DataFrame:
    # edit column with orginal datafile name, so it would be clear that it contains abundance after the pivoting of table
    compared_data['orig_file'] = compared_data['orig_file'] + '_abund'

    # go through all lines and make new column corresponding with name of a file and value of abundance sum for all found ions
    for i in range(expanded_theoretical_mass_table_df['ID'].max() + 1):
        compared_data = add_total_abundance_row_within_id(compared_data, i)

    # cast ID as integer and sort the dataframe again
    compared_data['ID'] = compared_data['ID'].astype('int32')
    compared_data = compared_data.sort_values(by=['ID', 'theor_m/z']).reset_index(drop=True)
    return compared_data


def calculate_mean_and_error_for_mass_to_charge_of_ions(aggregated_matched_files_summary_df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds columns with calculated mean value and standard error within each ion of a molecule throughout all matched experimental data.

    @param aggregated_matched_files_summary_df: dataframe containing all matched experimental data (from one or more files)
    @return: provided dataframe with additional columns for mean, standard error and their combination as a string.
    """
    # calculate mean experimental m/z value within group defined by molecule ID and ion.
    aggregated_matched_files_summary_df['mean_m/z'] = aggregated_matched_files_summary_df.groupby(['ID', 'ion'])["exp_m/z"].transform('mean').round(4)
    # calculate standard error of experimental m/z values within group defined by molecule ID and ion. Fill Nan with zeroes.
    aggregated_matched_files_summary_df['std_err_m/z'] = aggregated_matched_files_summary_df.groupby(['ID', 'ion'])["exp_m/z"].transform('std').round(4)
    aggregated_matched_files_summary_df['std_err_m/z'] = aggregated_matched_files_summary_df['std_err_m/z'].fillna(value=0.0000)
    # connect mean values with standard error into one string
    for lab, row in aggregated_matched_files_summary_df.iterrows():
        aggregated_matched_files_summary_df.loc[lab, 'exp_mean_m/z'] = str(row['mean_m/z']) + " ± " + str(row['std_err_m/z'])

    return aggregated_matched_files_summary_df


def pivot_aggregated_table(aggregated_matched_files_summary_with_mean_df: pd.DataFrame) -> pd.DataFrame:
    """
    pivot the results from long format to wide format for easier comparison between multiple experiments in the final aggregated table

    @param aggregated_matched_files_summary_with_mean_df:
    @return: provided dataframe transformed from long format to wide format
    """
    # first, it is necessary to fill all nan values because pivot_table function would remove these important rows
    aggregated_matched_files_summary_with_mean_df = aggregated_matched_files_summary_with_mean_df.fillna('empty')
    # pivot the table, all columns which we want to keep should be moved to index.
    # after pivoting, we can reset the index to get the columns back to table
    aggregated_matched_files_summary_wide_df = aggregated_matched_files_summary_with_mean_df.pivot_table(columns='orig_file',
                                                                                          values='Abundance',
                                                                                          index=['theor_m/z',
                                                                                                 'ID',
                                                                                                 'name',
                                                                                                 'ion',
                                                                                                 'charge',
                                                                                                 'warning',
                                                                                                 'exp_mean_m/z'],
                                                                                          aggfunc='sum',
                                                                                          sort=False).reset_index(drop=False)
    # replace 'nan +- 0' in the mean m/z values
    aggregated_matched_files_summary_wide_df = aggregated_matched_files_summary_wide_df.replace(to_replace=["nan ± 0.0", "empty"],
                                                                                                value=[np.nan, np.nan])
    return aggregated_matched_files_summary_wide_df


def sort_and_rearrange_aggregated_to_final_form(aggregated_matched_files_summary_wide_df: pd.DataFrame) -> pd.DataFrame:
    """

    @param aggregated_matched_files_summary_wide_df:
    @return: provided dataframe sorted by molecule ID and theor_m/z. Columns rearranged to have warning as a last column
    """
    # sort the values
    aggregated_matched_files_summary_wide_df = aggregated_matched_files_summary_wide_df.sort_values(
        by=['ID', 'theor_m/z']).reset_index(drop=True)
    # rearrange columns in aggregated table (move warning to last column)
    aggregated_matched_files_summary_wide_df = aggregated_matched_files_summary_wide_df[
        [col for col in aggregated_matched_files_summary_wide_df.columns if col != 'warning'] + ['warning']]
    return aggregated_matched_files_summary_wide_df


def data_matching_sequence(experimental_dfs_additional_info_df: pd.DataFrame, dict_containing_experimental_dfs: dict, expanded_theoretical_mass_table_df: pd.DataFrame) -> tuple:
    """
    Will match experimental data with theoretical m/z values and return new matched dataframes and one dataframe with overall results

    @param experimental_dfs_additional_info_df:
    @param dict_containing_experimental_dfs:
    @param expanded_theoretical_mass_table_df:
    @return: tuple containing dictionary with matched results, dataframe with aggregated results from all matched files and message about success of matching
    """
    try:
        # initiate empty dataframes for collecting results of matching together
        aggregated_matched_files_summary_df = pd.DataFrame()

        # initiate new dictionary which will hold dataframes after the matching
        dict_containing_matched_experimental_dfs = {}

        # loop through the files and do the matching
        for ind in experimental_dfs_additional_info_df.index:
            # load one of experimental data dataframes
            single_exp_file_df = dict_containing_experimental_dfs[ind]

            # define variables
            abundance_threshold, tolerance_of_mass, orig_datafile_nickname = get_values_from_additional_info_df(experimental_dfs_additional_info_df, ind)

            # prepare data before matching
            single_exp_file_df = prepare_experimental_for_matching(single_exp_file_df, abundance_threshold)

            # find best fits for experimental values from table of theoretical values
            compared_data_raw = match_experimental_with_theoretical(single_exp_file_df,
                                                                    expanded_theoretical_mass_table_df,
                                                                    tolerance_of_mass)

            # rearrange columns, drop rows where experimental data did not find match at theoretical table, sort, add information about file of data origin
            compared_data = process_raw_compared_data(compared_data_raw, orig_datafile_nickname)

            # save compared data for the file to the exp_dfs_matched
            dict_containing_matched_experimental_dfs[ind] = compared_data.copy()
            
            ###########################################################################################################
            # prepare data for aggregating with other experimental files
            compared_data_for_aggregating = prepare_matched_exp_file_for_aggregating(compared_data, expanded_theoretical_mass_table_df)

            # collect the data to one dataframe with full results
            aggregated_matched_files_summary_df = pd.concat([aggregated_matched_files_summary_df, compared_data_for_aggregating], ignore_index=True)

        ######################################################################################################################    
        
        # add column with calculated average m/z and its standard deviation for each molecule-ion pair throughout all files
        aggregated_matched_files_summary_with_mean_df = calculate_mean_and_error_for_mass_to_charge_of_ions(aggregated_matched_files_summary_df)

        # pivot the results from long format to wide format for easier comparison between experiments in the final aggregated table
        aggregated_matched_files_summary_wide_df = pivot_aggregated_table(aggregated_matched_files_summary_with_mean_df)

        # sort and rearrange into final form for showing and exporting the aggregated results
        aggregated_matched_files_final_form_df = sort_and_rearrange_aggregated_to_final_form(aggregated_matched_files_summary_wide_df)

        return (dict_containing_matched_experimental_dfs, aggregated_matched_files_final_form_df, 'Matches were found!')

    except:
        return (pd.DataFrame(), pd.DataFrame(), 'Something went wrong! Have you uploaded all necessary files? You can try to set larger mass accuracy value, add ions, check your data. Maybe, there are no matches anyway!')


def download_excel_with_results(experimental_dfs_additional_info_df: pd.DataFrame,
                                expanded_theoretical_mass_table_df: pd.DataFrame,
                                aggregated_matched_files_summary_df: pd.DataFrame,
                                dict_containing_matched_experimental_dfs: dict
                                ) -> BytesIO:
    """
    constructs Excel file with results for the download

    @param experimental_dfs_additional_info_df:
    @param expanded_theoretical_mass_table_df:
    @param aggregated_matched_files_summary_df:
    @param dict_containing_matched_experimental_dfs:
    @return: BytesIO object, in this case containing Excel file with results
    """
    # buffer to use for Excel writer
    buffer = BytesIO()
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write each dataframe to a different worksheet.
        experimental_dfs_additional_info_df.to_excel(writer, sheet_name='overview')
        expanded_theoretical_mass_table_df.to_excel(writer, sheet_name='theoretical_table')
        aggregated_matched_files_summary_df.to_excel(writer, sheet_name='aggregated_results')
        # loop through the matched exps and make one sheet for each df
        for key, df in dict_containing_matched_experimental_dfs.items():
            df.to_excel(writer, sheet_name=key)
        # Close the Pandas Excel writer and output the Excel file.
        writer.close()
    return buffer


def count_downloads():
    """
    opens counter.txt and add 1 to the last value.
    @return:
    """
    # add counter of downloaded files    
    with open("counter.txt", "r") as f:
        a = f.readline()  # starts as a string
        a = int(a)  # cast using int()
    a += 1  
    with open("counter.txt", "w") as f:
        f.truncate()
        f.write(f"{a}")


if __name__ == '__main__':
    pass
