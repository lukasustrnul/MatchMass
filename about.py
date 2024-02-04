# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 16:25:21 2024

@author: Lukáš
"""

import streamlit as st
from MS_func import show_counter



def about():
    st.write("""##### Number of files downloaded from the web:""", show_counter())
    st.write("##### ")
    st.write("#### About project")
    st.write("##### Motivation behind developing MatchMass online tool")
    st.write("""During our studies of macrocyclization reactions, a need arose for a tool to compare experimental 
             mass spectrometry (MS) data with a long list of theoretical molecules. In brief, macrocycles are typically 
             large cyclic molecules composed of several monomeric units. Monomers may contain reactive sites which can 
             form bond to other monomers or an additional reactant may be necessary. First, monomers need to form linear
             oligomers of sufficient length and then they may enclose to the final cyclic product. In our case we are using 
             urea based monomers which reacts with formaldehyde in acidic media. Such conditions yields library of macrocycles 
             and various oligomers with side-chains derived from formaldehyde.""")
    st.write("""In order to monitor the progress of the reaction, we took and measured samples at regular intervals. 
             This produced an excessive amount of data that was tedious and laborious to match manually with all the possible
             theoretical molecules that are formed in the process. And that's why the matching needed to be automated! 
             Moreover, we realized that such a tool in a form of online web app could be useful for other researchers too. """)
    st.write("##### ")
    st.write("##### Research group and university")
    st.write("""The original research using the MatchMass tool was conducted in Professor Riina Aav's 
             [Supramolecular chemistry group](https://riinaaav.wixsite.com/grouppage).
             The scientific group is based at the Department of Chemistry and Biotechnology, Tallinn University of Technology ([TalTech](https://taltech.ee/en/)), Estonia """)
    st.markdown("***")
    st.write("#### About author")
    st.write("##### Lukáš Ustrnul")
    st.write("""**A curious scientist and data analyst, always open to new collaborations and challenges.**""")
    st.write("""Additional information about the author and other projects:  
             [LinkedIn profile](https://www.linkedin.com/in/luk%C3%A1%C5%A1-ustrnul-058420123/)  
             [Github](https://github.com/lukasustrnul)  
             Researcher profile and publications [ORCID](https://orcid.org/0000-0003-4170-2132)  
             Profile at Estonian Research Information System [ETIS](https://www.etis.ee/CV/Luka%C5%A1_Ustrnul/eng/)""")
    st.write("""**If you have any questions, suggestions or you want to report any issues with MatchMass, please contact me at lukas.ustrnul[at]taltech.com**""")
    st.markdown("***")
    st.write("#### Acknowledgement")
    st.write("##### People")
    st.write("""I want to acknowledge Tatsiana Jarg ([ETIS](https://www.etis.ee/CV/Tatsiana_Shalima/eng)) for her ideas and feedback, 
             Prof. Riina Aav ([ETIS](https://www.etis.ee/CV/Riina_Aav)) for her support, and all members of Supramolecular group for positive atmosphere.""")
    st.write("##### ")
    st.write("##### Funding")
    st.write("""Development of MatchMass was supported by European Commission grant [VFP18059](https://www.etis.ee/Portal/Projects/Display/a535003a-03b5-45c8-8168-49d68ffdb3ec)
             and Estonian Research Council ([ETAG](https://etag.ee/en/)) grants [PRG399](https://www.etis.ee/Portal/Projects/Display/821f6a9c-3f7d-49c4-86b8-2747c4e210a2),
             [MOBJD592](https://www.etis.ee/Portal/Projects/Display/6dd1c9dc-6e88-4983-98c8-3b31f325bfd0), 
             [PRG2169](https://www.etis.ee/Portal/Projects/Display/2765d91c-0c57-43ee-ae98-d7fefbcedf88)""")
    col1, col2, col3 = st.columns(3, gap = 'medium')
    with col1:
        st.image('files/Estonian-Research-Council-logo-color_RGB.png'
                 )
        st.image('files/EN_Co-fundedbytheEU_RGB_NEG.png'
                 )
        st.image('files/TalTech_logo_JPG.jpg'
                 )

