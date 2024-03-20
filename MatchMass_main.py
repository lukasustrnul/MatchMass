# -*- coding: utf-8 -*-
"""
Author: Lukáš Ustrnul
GitHub: https://github.com/lukasustrnul
LinkedIn: https://www.linkedin.com/in/luk%C3%A1%C5%A1-ustrnul-058420123/

Created on Sat Jan 13 15:13:31 2024
"""

import streamlit as st
from data_functions import add_ions_to_theoretical_table, determine_bar_width, raise_warning_for_masses_within_accuracy
import ui_functions as UI_fc
from about import about_expander_content
from instructions import instructions_expander_content
from plots import make_plot1, make_plot2

# set layout of the page and title
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="MatchMass")
st.header('MatchMass - Mass Spectrometry Matching Tool', divider="rainbow")
st.markdown(
    """##### Quickly compare your experimental results with a table of theoretical *m/z* values to find out which molecules and ions of interest are really present in the mixture.""")

# add expander with instructions
UI_fc.local_css("files/style.css")
with st.expander("About"):
    about_expander_content()
with st.expander("Check instructions and tips..."):
    instructions_expander_content()


# upload of user-provided data (tables)
# heading and initiate columns
st.write("#### File upload")
col1, col2, col3 = st.columns(3, gap='medium')

# use streamlit uploader to upload tables of experimental data and table of theoretical values
with col1:
    experimental_UploadedFile_object = UI_fc.experimental_data_upload_ui()
with col2:
    theoretical_table_UploadedFile_object = UI_fc.theoretical_data_upload_ui()
with col3:
    UI_fc.example_data_download()


# transform uploaded files to dataframes or create empty dataframes and dictionaries to show before upload
theoretical_mass_table_df = UI_fc.provide_empty_or_uploaded_theoretical_table(theoretical_table_UploadedFile_object)

experimental_dfs_additional_info_df, dict_containing_experimental_dfs, dict_experimental_filenames = UI_fc.provide_empty_or_uploaded_experimental_data(
    experimental_UploadedFile_object)

# divide graphically upload part and user-defined settings of mass accuracy and abundance threshold
st.markdown("***")


# User's defined exp. error and abundance threshold
# it is necessary to choose suitable experimental error for the matching process
# moreover, low abundance signals may not be of interest

# write informative text about setting experimental error and abundance threshold
st.write("#### Mass accuracy and abundance threshold has to be defined.")
st.write(
    """Mass accuracy value should be based on your spectrometer specification. 
    If you set too small value it may lead to less matches found.  
    Abundance threshold value is used to exclude signals with low abundance.""")

# show the radio button and get the user's choice
radio_choice = UI_fc.radio_for_user_input_of_accuracy_and_threshold()

# define what to show based on selected option on the radio
if radio_choice == 'No':
    accur_setting, thresh_setting = UI_fc.user_input_global_accuracy_and_threshold()
    experimental_dfs_additional_info_df['mass_accuracy(Da)'] = accur_setting
    experimental_dfs_additional_info_df['abund_thrs'] = thresh_setting

elif radio_choice == 'Yes':
    st.write('Please edit values in columns for mass accuracy and abundance threshold.')
    experimental_dfs_additional_info_df = UI_fc.user_input_individual_accuracy_and_threshold(
        experimental_dfs_additional_info_df)

else:
    pass


# pick ions to add to the theoretical table
#
# part for picking ions of interest which will be added to theoretical table
# before its use for matching with experimental results
#
# divide graphically upload part and add heading
st.markdown("***")
st.write('### Pick ions which you want to match with your experimental data')
st.write('''Generally, there are two approaches. First, to upload table containing 
         monoisotopic mass of neutral molecules and then pick cations or anions 
         of interest. Second, to upload table containing final m/z values for 
         various ions and then choose option to use uploaded theoretical m/z.''')

ions_to_add_to_theoretical_table_dict = UI_fc.ion_picking_with_checkboxes()


# prepare full table of theoretical masses
#
# define experimental error to later generate warning message for overlapping m/z of ions
max_mass_accur_value = experimental_dfs_additional_info_df['mass_accuracy(Da)'].max()

# run the AddIonsToTheoreticalTable function and obtain table with all theoretical masses of interest
expanded_theoretical_mass_table_df = add_ions_to_theoretical_table(theoretical_mass_table_df,
                                                                   ions_to_add_to_theoretical_table_dict)
# add warning for theoretical masses which are within mass accuracy range
expanded_theoretical_mass_table_df = raise_warning_for_masses_within_accuracy(expanded_theoretical_mass_table_df,
                                                                              max_mass_accur_value)


# create first plot for comparing experimental and theoretical data
#
# divide graphically ion picking part and add heading
st.markdown("***")
st.write('### You can visually compare position of experimental signals with the theoretical *m/z* values')

# dropdown menu to pick data for plot
pick_from_selectbox1 = st.selectbox('Choose an experimental file to plot against theoretical *m/z* of chosen ions:',
                                    list(dict_experimental_filenames.keys()))
# get the nickname of the file and use it to pass dataframe to plotting
selectbox1_picked_file_nickname = dict_experimental_filenames[pick_from_selectbox1]
df_for_plot1 = dict_containing_experimental_dfs[selectbox1_picked_file_nickname]

# define experimental error to use as a bar width for theoretical m/z
width_for_theoretical_mz_bars = determine_bar_width(max_mass_accur_value)

# Create first plot for our data
make_plot1(df_for_plot1, expanded_theoretical_mass_table_df, width_for_theoretical_mz_bars)


# Do the matching!
#
# divide graphically from previous part and add heading
st.markdown("***")
st.write('### Match the data, check outcomes and download results!')
st.write(' Matching process can take some time if your files are large.')
st.write(
    """ If you are not satisfied with results you can try 
    to change settings above (errors, thresholds, ion picking) 
    and then hit the **Matching button** again!!!""")

# show the matching button and save results of a matching process
dict_containing_matched_experimental_dfs, aggregated_matched_files_summary_df, matching_result_message = UI_fc.matching_button(
    experimental_dfs_additional_info_df,
    dict_containing_experimental_dfs,
    expanded_theoretical_mass_table_df)


# Show the results:
# create second plot to visualize which signals got match,
# show aggregated table,
# show download button for results
#
# make a condition to show the matched data only if there are data to show
if aggregated_matched_files_summary_df.empty:
    st.write(matching_result_message)

else:
    st.write(matching_result_message)

    # make new dictionary to use as a key for the dropdown menu
    dict_experimental_filenames2 = {str(v) + " : " + str(k): v for k, v in dict_experimental_filenames.items()}

    # dropdown menu to pick data for plot
    pick_from_selectbox2 = st.selectbox('Choose an experimental file to plot:',
                                        list(dict_experimental_filenames2.keys()))
    # get the nickname of the file and use it to pass dataframe to plotting
    selectbox2_picked_file_nickname = dict_experimental_filenames2[pick_from_selectbox2]
    not_matched_df_for_plot2 = dict_containing_experimental_dfs[selectbox2_picked_file_nickname]
    matched_df_for_plot2 = dict_containing_matched_experimental_dfs[selectbox2_picked_file_nickname]

    # Create second plot showing which signals found match and which did not
    make_plot2(not_matched_df_for_plot2, matched_df_for_plot2)

    # show the final table
    st.write('##### Final table with aggregated results from all provided experimental files')
    st.dataframe(aggregated_matched_files_summary_df, use_container_width=True)

    # show download button
    UI_fc.button_for_results_download(experimental_dfs_additional_info_df,
                                      expanded_theoretical_mass_table_df,
                                      aggregated_matched_files_summary_df,
                                      dict_containing_matched_experimental_dfs)
