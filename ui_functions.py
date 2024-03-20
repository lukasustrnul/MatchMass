"""
Author: Lukáš Ustrnul
GitHub: https://github.com/lukasustrnul
LinkedIn: https://www.linkedin.com/in/luk%C3%A1%C5%A1-ustrnul-058420123/

File: ui_functions.py
Created on 15.03.2024

Note: this file should contain definitions for functions which provides graphical output to the UI
"""
import pandas as pd
import numpy as np
import streamlit as st
from data_functions import theoretical_upload_object_to_dataframe, extract_info_and_data_from_experimental_upload, data_matching_sequence, download_excel_with_results, count_downloads
from ions_enum import Ion


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def experimental_data_upload_ui() -> st.runtime.uploaded_file_manager.UploadedFile:
    """
    Shows part of page with upload widget for experimental files and returns UploadedFile object

    @return: UploadedFile object containing all uploaded experimental files
    """
    st.write('##### Upload experimental data')
    experimental_UploadedFile_object = st.file_uploader(
        'Multiple files are allowed. \n\n You can use the .CSV, .XLSX or .XLS filetype here',
        type=['xlsx', 'xls', 'csv'],
        accept_multiple_files=True,
        help='Maximum size of file is 200 MB',
        on_change=None,
        disabled=False,
        label_visibility="visible"
    )
    return experimental_UploadedFile_object


def theoretical_data_upload_ui() -> st.runtime.uploaded_file_manager.UploadedFile:
    """
    Shows part of page with upload widget for table containing theoretical masses and returns UploadedFile object

    @return: UploadedFile object containing uploaded theoretical table
    """
    st.write('##### Upload table of monoisotopic masses (or *m/z*)')
    theoretical_table_UploadedFile_object = st.file_uploader(
        'Only one file is allowed. \n\n You can use the .CSV, .XLSX or .XLS filetype here',
        type=['xlsx', 'xls', 'csv'],
        accept_multiple_files=False,
        help='Only one file!',
        on_change=None,
        disabled=False,
        label_visibility="visible"
    )
    return theoretical_table_UploadedFile_object


def example_data_download() -> None:
    """
    Shows part of page with download buttons for simulated examples of theoretical table and experimental data.
    User may download the files and test the functionality of the app with them.

    @return: None
    """
    st.write("##### Download example")
    st.write("You can test the app with our simulated data.")
    with open('files/simulated_theor.xlsx', 'rb') as my_file:
        st.download_button(label='Download simulated theoretical masses table!',
                           data=my_file,
                           file_name='theoretical_simulated.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                           use_container_width=True,
                           help="monoisotopic masses were randomly generated")
    with open('files/simulated_exp_full.xlsx', 'rb') as my_file:
        st.download_button(label='Download simulated experimental data!',
                           data=my_file,
                           file_name='experimental_simulated.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                           use_container_width=True,
                           help="Simulated exp. data may contain [M]+, [M+H]+, [M+Na]+ and [2M+H]+ ions")


def provide_empty_or_uploaded_theoretical_table(theoretical_table_UploadedFile_object: st.runtime.uploaded_file_manager.UploadedFile) -> pd.DataFrame:
    """
    provides empty dataframe if no theoretical table was uploaded yet, or it provides uploaded theoretical table as a dataframe for further processing

    @param theoretical_table_UploadedFile_object: UploadedFile object containing file from upload widget for theoretical table
    @return: dataframe with theoretical table, either empty if no file was uploaded or with content provided by user
    """
    if theoretical_table_UploadedFile_object:
        theoretical_mass_table_df = theoretical_upload_object_to_dataframe(theoretical_table_UploadedFile_object)
    else:
        theoretical_mass_table_df = pd.DataFrame()
    return theoretical_mass_table_df


def provide_empty_or_uploaded_experimental_data(experimental_UploadedFile_object: st.runtime.uploaded_file_manager.UploadedFile) -> tuple:
    """

    @param experimental_UploadedFile_object: UploadedFile object containing files from upload widget for experimental files
    @return: tuple (pd.DataFrame, dict[UploadedFile]=pd.DataFrame, dict[orig_filename]= file_nickname )
        tuple contains real data if any file was uploaded or dummy dataframe and dictionaries if there is no uploaded experimental file
    """
    if experimental_UploadedFile_object:
        experimental_dfs_additional_info_df, dict_containing_experimental_dfs, dict_experimental_filenames = extract_info_and_data_from_experimental_upload(
            experimental_UploadedFile_object)
    else:
        experimental_dfs_additional_info_df = pd.DataFrame(index=['orig_name'],
                                                           columns=['orig_name', 'mass_accuracy(Da)', 'abund_thrs'])
        dict_containing_experimental_dfs = {
            'No data uploaded': pd.DataFrame([{'exp_m/z': np.nan}, {'Abundance': np.nan}])}
        dict_experimental_filenames = {'No experimental data uploaded': 'No data uploaded'}
    return (experimental_dfs_additional_info_df, dict_containing_experimental_dfs, dict_experimental_filenames)


def user_input_global_accuracy_and_threshold() -> tuple:
    """
    allows user to input numerical values for mass accuracy and abundance threshold which will be used on all (globally) experimental files

    @return: tuple containing user defined value for mass accuracy and abundance threshold
    """
    # initiate session state to keep values of mass accuracy and abundance set if radio = 'No'
    if "mass_accuracy_value" not in st.session_state:
        st.session_state["mass_accuracy_value"] = 0.00001
    if "Abund_thresh_value" not in st.session_state:
        st.session_state["Abund_thresh_value"] = 0.0

    # define helping functions to save values to the session state
    def set_accuracy():
        st.session_state["mass_accuracy_value"] = st.session_state["new_accuracy_value"]

    def set_threshold():
        st.session_state["Abund_thresh_value"] = st.session_state["new_abund_thresh_value"]

    # define what to show based on selected option on the radio
    col101, col102 = st.columns(2, gap='medium')
    with col101:
        st.session_state["mass_accuracy_value"] = st.number_input('Insert mass accuracy (Da)',
                                                                  step=0.00001,
                                                                  key="new_accuracy_value",
                                                                  value=st.session_state["mass_accuracy_value"],
                                                                  format="%0.5f",
                                                                  on_change=set_accuracy
                                                                  )
    with col102:
        st.session_state["Abund_thresh_value"] = st.number_input('Insert abundance threshold (in a scale from experimental data)',
                                                                 step=0.01,
                                                                 key="new_abund_thresh_value",
                                                                 value=st.session_state["Abund_thresh_value"],
                                                                 on_change=set_threshold
                                                                 )
    # save user defined values to variable and return them as a tuple
    accur_setting = st.session_state["mass_accuracy_value"]
    thresh_setting = st.session_state["Abund_thresh_value"]
    return (accur_setting, thresh_setting)


def user_input_individual_accuracy_and_threshold(df: pd.DataFrame) -> pd.DataFrame:
    """

    @param df: dataframe holding additional information about processing of experimental files
    @return: original dataframe with values in mass accuracy and abundance threshold column changed by user input
    """
    df = st.data_editor(df,
                        disabled=["orig_name", 'nickname'],
                        column_config={
                            'mass_accuracy(Da)': st.column_config.NumberColumn(
                               help="you can copy values from one line to the rest in the same way as in excel"),
                            'abund_thrs': st.column_config.NumberColumn(
                               help="you can copy values from one line to the rest in the same way as in excel")
                        })
    return df


def radio_for_user_input_of_accuracy_and_threshold() -> str:
    """
    Show radio button to allow a user to choose if to set mass accuracy and abundance threshold
    globally (for all experimental files the same values -> radio is at 'No')
    or individually (values for each experimental file can be different -> radio is at 'Yes')

    @return: string 'Yes' or 'No' according to the current setting of the radio button
    """
    # initiate value of radio to "No"
    if "mass_accur_abund_thresh_radio" not in st.session_state:
        st.session_state["mass_accur_abund_thresh_radio"] = "No"

    # add the radio button for switching between setting global experimental error or different error value for each file
    st.radio(
        "Do you wish to set different mass accuracy and abundance threshold for each uploaded file? ",
        ['No', 'Yes'],
        key="mass_accur_abund_thresh_radio"
    )

    return st.session_state["mass_accur_abund_thresh_radio"]


def ion_picking_with_checkboxes() -> dict:
    """
    Shows checkboxes for selecting which ions to add to the table of theoretical m/z

    @return: dictionary where keys are names of ions from ions_enum.Ion and values are booleans
    """
    # generate necessary lists
    cations_list = [ion for ion in Ion if ion.value.ion_type == 'cation']
    anions_list = [ion for ion in Ion if ion.value.ion_type == 'anion']

    # initiate dictionary to save choices from checkboxes
    ions_to_add_to_theoretical_table_dict = {}

    col1, col2, col3 = st.columns(3, gap='medium')
    with col1:
        st.write('Pick from following for positive mode MS experimental results.')
        for ion in cations_list:
            ions_to_add_to_theoretical_table_dict[ion.name] = st.checkbox(ion.value.ion_formula,
                                                                          help='tick to add ion to the theoretical table')
    with col2:
        st.write('''Pick from following for negative mode MS experimental results.''')
        for ion in anions_list:
            ions_to_add_to_theoretical_table_dict[ion.name] = st.checkbox(ion.value.ion_formula,
                                                                          help='tick to add ion to the theoretical table')
    with col3:
        st.write("""Keeping the original values from the user-supplied theoretical table should only be used if the table
                 already contained *m/z* values for the ions of interest instead of neutral monoisotopic masses.""")
        ions_to_add_to_theoretical_table_dict[Ion.M_orig.name] = st.checkbox(Ion.M_orig.value.ion_formula,
                                                                             help='tick to keep m/z values as provided in uploaded table of theoretical values')

    return ions_to_add_to_theoretical_table_dict


def matching_button(experimental_dfs_additional_info_df: pd.DataFrame, dict_containing_experimental_dfs: dict, expanded_theoretical_mass_table_df: pd.DataFrame) -> tuple:
    """
    shows button for matching and saves results of matching to session state. Provides empty dataframes and string if there was no matching done yet.

    @param experimental_dfs_additional_info_df: table with additional information about experimental files and settings for matching
    @param dict_containing_experimental_dfs: dictionary containing all experimental files as dataframes
    @param expanded_theoretical_mass_table_df: dataframe containing theoretical values of m/z for matching with experimental data
    @return: tuple
    """
    # initiate the session state to hold results of matching
    if "matched_results" not in st.session_state:
        st.session_state["matched_results"] = (pd.DataFrame(), pd.DataFrame(), '')

    # create button to initiate matching
    do_the_matching = st.button("""# Find matching signals!""")

    # match the data and save to session state if the button is pushed
    if do_the_matching:
        st.session_state["matched_results"] = data_matching_sequence(experimental_dfs_additional_info_df, dict_containing_experimental_dfs, expanded_theoretical_mass_table_df)
    else:
        pass

    # save the content of session state and return as a tuple
    dict_containing_matched_experimental_dfs, aggregated_matched_files_summary_df, matching_result_message = st.session_state["matched_results"]
    return (dict_containing_matched_experimental_dfs, aggregated_matched_files_summary_df, matching_result_message)


def show_count_of_downloads() -> str:
    """
    shows number from counter.txt

    @return: string containing number of downloaded files
    """
    counter = open("counter.txt", "r")
    counter_count = counter.readline()  # it is a string
    return counter_count


def button_for_results_download(experimental_dfs_additional_info_df: pd.DataFrame,
                                expanded_theoretical_mass_table_df: pd.DataFrame,
                                aggregated_matched_files_summary_df: pd.DataFrame,
                                dict_containing_matched_experimental_dfs: dict
                                ) -> None:
    """
    shows button for download of results

    @param experimental_dfs_additional_info_df:
    @param expanded_theoretical_mass_table_df:
    @param aggregated_matched_files_summary_df:
    @param dict_containing_matched_experimental_dfs:
    @return:
    """
    st.download_button(
        label="Download data as Excel",
        data=download_excel_with_results(experimental_dfs_additional_info_df,
                                         expanded_theoretical_mass_table_df,
                                         aggregated_matched_files_summary_df,
                                         dict_containing_matched_experimental_dfs),
        file_name='results_matched.xlsx',
        mime='application/vnd.ms-excel',
        key="downloaded",
        on_click=count_downloads
    )


if __name__ == '__main__':
    pass
