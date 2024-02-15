# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 15:13:31 2024

@author: Lukáš Ustrnul
"""

import streamlit as st
#import plotly.graph_objects as go
import pandas as pd
import numpy as np
from ions import *
from MS_func import local_css, add_ions, make_theoretical, make_experimental, match_data, download_excel, counter_fc
from about import about
from instructions import instructions
from plots import make_plot1, make_plot2



# set layout of the page and title
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="MatchMass")
st.header('MatchMass - Mass Spectrometry Matching Tool', divider = "rainbow")
st.markdown("""##### Quickly compare your experimental results with a table of theoretical *m/z* values to find out which molecules and ions of interest are really present in the mixture.""")

# add expander with instructions
local_css("files/style.css")
with st.expander("About"):
    about()
with st.expander("Check instructions and tips..."):
    instructions()




###################### import of user's data 
# heading and initiate columns
st.write("#### File upload")
col1, col2, col3= st.columns(3, gap = 'medium')

# use streamlit uploader to upload tables of experimental data and table of theoretical values
with col1:
    st.write('##### Upload experimental data')
    exp_upload = st.file_uploader(
        'Mutiple files are allowed. \n\n You can use the .CSV, .XLSX or .XLS filetype here', 
                     type= ['xlsx','xls','csv'],
                     accept_multiple_files=True, 
                     help='Maximum size of file is 200 MB', 
                     on_change=None, 
                     disabled=False, 
                     label_visibility="visible"
                     )
with col2:
    st.write('##### Upload table of monoisotopic masses (or *m/z*)')
    theor_upload = st.file_uploader(
        'Only one file is allowed. \n\n You can use the .CSV, .XLSX or .XLS filetype here', 
                     type= ['xlsx','xls','csv'],
                     accept_multiple_files=False, 
                     help='Only one file!', 
                     on_change=None, 
                     disabled=False, 
                     label_visibility="visible"
                     )
with col3:
    st.write("##### Download example")
    st.write("You can test the app with our simulated data.")
    with open('files/simulated_theor.xlsx', 'rb') as my_file:
        st.download_button(label = 'Download simulated theoretical masses table!', 
                           data = my_file, 
                           file_name = 'theoretical_simulated.xlsx', 
                           mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                           use_container_width=True,
                           help = "monoisotopic masses were randomly generated")
    with open('files/simulated_exp_full.xlsx', 'rb') as my_file:
        st.download_button(label = 'Download simulated experimental data!', 
                           data = my_file, 
                           file_name = 'experimental_simulated.xlsx', 
                           mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                           use_container_width=True,
                           help = "Simulated exp. data may contain [M]+, [M+H]+, [M+Na]+ and [2M+H]+ ions")







############### transform imported files to dataframes and create empty dataframes and dictionaries to show before upload
if theor_upload:
    theor_df = make_theoretical(theor_upload)
else:
    theor_df = pd.DataFrame()

if exp_upload:
    exp_dfs_table, exp_dfs, exp_dfs_names = make_experimental(exp_upload)
else:
    exp_dfs_table=pd.DataFrame(index = ['orig_name'], columns=['orig_name','exp_err','abund_thrs'])        
    exp_dfs={'No data uploaded':pd.DataFrame([{'exp_m/z':np.nan},{'Abundance':np.nan}])}                          
    exp_dfs_names = {'No experimental data uploaded':'No data uploaded'}  

# divide graphically upload part and settings of error
st.markdown("***") 








########## User's defined exp. error and abundance threshold
# it is necessary to choose suitable experimental error for the matching process
# moreover, low abundance signals may not be of interest

# initiate value of radio to "No"
if "err_abund_def" not in st.session_state:
    st.session_state["err_abund_def"] = "No"
# write informative text about setting experimental error and abundance threshold 
st.write("#### Mass accuracy and abundance threshold has to be defined.") 
st.write("""Mass accuracy value should be based on your spectrometer specification. If you set too small value it may lead to less matches found.  
         Abundance threshold value is used to exclude signals with low abundance.""")     
# add the radio button for switching between setting global experimental error or different error value for each file
st.radio(
    "Do you wish to set different mass accuracy and abundance threshold for each uploaded file? ",
    ['No','Yes'],
    key = "err_abund_def" 
    )
# initiate session state to keep values of error and abundance set if radio = 'No'
if "err_no_val" not in st.session_state:
    st.session_state["err_no_val"] = 0.00001
if "abund_thrs_no_val" not in st.session_state:
    st.session_state["abund_thrs_no_val"] = 0.0

# define what to show based on selected option on the radio
if st.session_state["err_abund_def"] == 'No':
    col101, col102= st.columns(2, gap = 'medium')
    with col101:
        exp_dfs_table['exp_err'] = st.number_input('Insert mass accuracy (Da)',
                                                   step=0.00001,
                                                   key = "err_no_val",
                                                   value = st.session_state["err_no_val"],
                                                   format="%0.5f"
                                                   )
    with col102:
        exp_dfs_table['abund_thrs'] = st.number_input('Insert abundance threshold (in a scale from experimental data)',
                                                      step=0.01,
                                                      key = "abund_thrs_no_val",
                                                      value = st.session_state["abund_thrs_no_val"]
                                                      )
elif st.session_state["err_abund_def"] == 'Yes':
    st.write('Please edit values in columns for mass accuracy and abundance threshold.')
    exp_dfs_table = st.data_editor(exp_dfs_table, 
                                   disabled=["orig_name",'nickname'],
                                   column_config={
                                       "exp_err": st.column_config.NumberColumn(help="you can copy values from one line to the rest in the same way as in excel"),
                                       "abund_thrs": st.column_config.NumberColumn(help="you can copy values from one line to the rest in the same way as in excel")
                                       })
else:
    pass








################# pick ions to add to the theoretical table
# part for picking ions of interest which will be added to theoretical table before its use for matching with experimental results
# divide graphically upload part and add heading
st.markdown("***")  
st.write('### Pick ions which you want to match with your experimental data')
st.write('''Generally, there are two approaches. First, to upload table containing 
         monoisotopic mass of neutral molecules and then pick cations or anions 
         of interest. Second, to upload table containing final m/z values for 
         various ions and then choose option to use uploaded theoretical m/z.''')
col11, col12, col13 = st.columns(3, gap = 'medium')
with col11:
    st.write('Pick from following for positive mode MS experimental results.')
    for ion in pos_ion_list:
        ion['add_to_df'] = st.checkbox(ion['ion'], help='tick to add ion to the theoretical table')
with col12:
    st.write('''Pick from following for negative mode MS experimental results.''')
    for ion in neg_ion_list:
        ion['add_to_df'] = st.checkbox(ion['ion'], help='tick to add ion to the theoretical table')
with col13:
    st.write("""Keeping the original values from the user-supplied theoretical table should only be used if the table
             already contained *m/z* values for the ions of interest instead of neutral monoisotopic masses.""")
    M_orig['add_to_df'] = st.checkbox(M_orig['ion'], help='tick to keep m/z values as provided in uploaded table of theoretical values')
    

############### prepare full table of theoretical masses
# define experimental error to later generate warning message for overlaping m/z of ions
exp_err = exp_dfs_table['exp_err'].max()
# run the function and obtain table with all theoretical masses of interest
theor_df_full = add_ions(theor_df, ion_list, exp_err)


    




################### crate first plot for comparing experimental and theoretical data
# divide graphically ion picking part and add heading
st.markdown("***") 
st.write('### You can visually compare position of experimental signals with the theoretical *m/z* values')
# dropdown menu to pick data for plot
pick1 = st.selectbox('Choose an experimental file to plot against theoretical *m/z* of choosen ions:', list(exp_dfs_names.keys()))
file_pick1=exp_dfs_names[pick1]
df1=exp_dfs[file_pick1]

# define experimental error to use as a bar width for theoretical m/z 
if exp_err>0:
    theor_width =2*exp_err
else:
    theor_width = 0.005
# Create first plot for our data
make_plot1(df1, theor_df_full, theor_width)






################# do the matching!
# divide graphically from previous partand add heading
st.markdown("***") 
st.write('### Match the data, check outcomes and download results!')
st.write(' Matching process can take some time if your files are large.')
st.write(' If you are not satisfied with results you can try to change settings above (errors, thresholds, ion picking) and then hit the **Matching button** again!!!')
# initiate session state to hold results of matching
if "matched_results" not in st.session_state:
    st.session_state["matched_results"] = (pd.DataFrame(),pd.DataFrame(),pd.DataFrame(), '')
# create button to initiate matching
matched = st.button("""# Find matching signals!""")
if matched:
    st.session_state["matched_results"] = match_data(exp_dfs_table, exp_dfs, theor_df_full)
else:
    pass
# save the results
theor_df_final, exp_dfs_matched, all_in_one, message_match = st.session_state["matched_results"]






################### create second plot to visualize which signals got match
# make a condition to show the matched data only if there are data to show
if all_in_one.empty:
    st.write(message_match)
else:
    st.write(message_match)
    # make new dictionary to use as a key for the dropdown menu
    exp_dfs_names_nick = {str(v)+" : "+str(k):v for k,v in exp_dfs_names.items()}
    # dropdown menu to pick data for plot
    pick2 = st.selectbox('Choose an experimental file to plot:', list(exp_dfs_names_nick.keys()))
    file_pick2=exp_dfs_names_nick[pick2]
    df2_orig=exp_dfs[file_pick2]
    df2_matched=exp_dfs_matched[file_pick2]
    
    # Create second plot showing which signals found match and which did not
    make_plot2(df2_orig, df2_matched)
    
    # show the final table
    st.write('##### Final table with aggregated results from all provided experimental files')
    st.dataframe(all_in_one,use_container_width=True)
    
    
    st.download_button(
        label="Download data as Excel",
        data=download_excel(exp_dfs_table, theor_df_full, all_in_one, exp_dfs_matched),
        file_name='results_matched.xlsx',
        mime='application/vnd.ms-excel',
        key = "downloaded",
        on_click = counter_fc
        )


