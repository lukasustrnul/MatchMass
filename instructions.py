# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:14:29 2024

@author: Lukáš
"""
import streamlit as st


@st.cache_data
def instructions():
    st.write("#### Instructions")
    st.write("Prepare your data and go simply from top to the bottom of the page! :wink::blush:")
    st.write(""" * 0. Data preparation.  
             This has to be done in your computer before you upload your data. At least one 
             file of experimental values and maximum one file of theoretical values 
             are needed. It is crucial to use correct order of columns and to use first row 
             for column names (see examples below).
             Uploader supports .XLS, .XLSX and .CSV files.  
             *Experimental file:* First column contains m/z values and second column is abundance (intensity of signal).  
             *Theoretical file:* First column with molecule name and second column with theoretical mass (not molar mass) or m/z values for ions.
             """)
    col1, col2 = st.columns(2, gap = 'medium')
    with col1:
        st.image('files/exp_png_example.jpg', 
                 caption = 'example of file with experimental data',
                 width = 400
                 )
    with col2:
        st.image('files/theor_png_example.jpg', 
                 caption = 'example of file with theoretical m/z',
                 width = 400
                 )
    st.write(""" * 1. Upload data.  
             (You can download and use our simulated data to test the functionality)""" )
    st.write(""" * 2. Define experimental error and threshold for abundance.  
             It can be done for all files at once or for each file separately. 
             Keep in mind that large experimental error can lead to wrong matching 
             if some of theoretical m/z are near to each other. 
             However, you will get warning note in the matched data and 
             check such signals later manually. """ )
    st.write(""" * 3. Pick ions to add in your table of theoretical masses.  
             Notice: Although you can add both, positive and negative ions, at the same time, 
             such a combination cannot occur in any real MS measurement.  
             First plot of experimental data overlayed with theoretical masses 
             can be used to estimate which ions to add.""" )
    st.write(""" * 4. Push the 'Matching' button""" )
    st.write(""" * 5. Check the results in the plot.  
             Chart shows which experimental signals were matched with theoretical m/z values.  
             If you are not happy with the results you can try to make changes 
             in steps 2. and 3. and then push the 'Matching' button again.""" )
    st.write(""" * 6. Download the results""" )
    st.write(""" * 7. Please, cite this online app.  
             We recommend that if you use MatchMass you cite it with these two references in the citation list:  
                 1. .........TBA........, Author: Lukas Ustrnul, published February 2024.  
                 2. .........TBA........, article will be submitted to peer reviewed journal during Q1 2024.    
                 This will help to increase the visibility of this online tool.""" )
    st.markdown("***")
    st.write("#### Tips and additional notes")
    st.write(""" * Our example data under 'Download dummy data' are purely simulated 
             values and does not correspond to any real molecules. Experimental data was 
             simulated by adding [M]+, [M+H]+, [M+Na]+ and [2M+H]+ ions. Random error 
             to m/z values was obtained by adding random numbers from normal distribution 
             with standard deviation 0.003. Abundance was randomly generated from 
             uniform distribution from range 50 to 100000. Abundance of ions other 
             than [M+H]+ was divided by 10 to improve resemblance to a real MS data.""")
    st.write(""" * Picking of ions... List of available ions is based on typical ion 
             composition in our own experiments and on the list of most common ions 
             provided in article from [M. R. Blumer et al.](https://pubs.acs.org/doi/10.1021/acs.jcim.1c00579).""" )
    st.write(""" * Warning column in the results of matching can tell you **'Possibility of wrong matching! Difference from previous
             or following m/z in full theoretical table is lower than the largest experimental error set by user.'** Message
             is generated based on m/z differences between ions and the experimental error defined by user. In the case of 
             experimental errors defined individually for each experimental file, the largest defined error is used to 
             determine lines with the warning message. The message will be seen for any matched ion which could fall under two or more 
             ions from the full theoretical table. Nevertheless, matching of experimental m/z is always to the nearest theoretical m/z. 
             Formula for calculating the warning: (m/z(ion1) - m/z(ion2)) < 2*experimental_error """)
    st.write(""" * Do you miss some ions? Here is a tip...  
             You can use your starting theoretical m/z and add ions from our list. 
             Run the matching and download results, one of the sheets contains complete
             table of used theoretical masses. You can use this sheet to make new 
             table of theoretical masses to which you will manually add other ions 
             of your interest. We propose to calculate theoretical m/z in Excel calculator
             provided by [Fiehn Lab](https://fiehnlab.ucdavis.edu/staff/kind/metabolomics/ms-adduct-calculator).
             Finally, you will use this table in next round of matching but instead of adding ions
             you will use third option of [M] because your table already contains all 
             ions of interest.""" )
    st.write(""" * Plots can be switched to fullscreen view""")
    st.write(""" * Bar width in the plots...  
             While it is always 0.0001 Da for experimental data, the bar width for 
             theoretical m/z values corresponds to double of experimental error or to 0.005 Da if the error is set to zero.
             This may help to visually evaluate your settings for matching.""")
    st.write(""" * If you need to calculate a monoisotopic mass or are trying to find a possible molecular formula for 
             an unidentified mass, we recommend using [ChemCalc](http://chemcalc.org/).""")