# MatchMass - Mass Spectrometry Matching Tool
### Compare your experimental data from mass spectrometry (MS) with a table of theoretical mass-to-charge ratio (m/z) values to quickly find out which molecules and ions of interest are present in the sample.
***
## **Brief overview**  
Mass spectrometry is very sensitive and precise analytical technique for identification and quantification of molecules; therefore, it isused in many fields of science. MatchMass was developed to provide free easy-to-use tool to help researchers with identification of molecules in complex mixtures. The MatchMass was developed during the chemical research focused to study mechanism of macrocyclization reactions. Additional information about our motivation and research can be found in the app itself. 

In the near future, MatchMass will be hosted at Tallinn University of Technology domain (taltech.ee). However, you can test it as a **locally running browser version** made in [stlite](https://edit.share.stlite.net/?sampleAppId=intro). The app code and data are encoded into the URL as a hash like `https://share.stlite.net/#!ChBz...`. Probably due to the excessive length of the link I was not able to make a functional hyperlink here in GitHub. Therefore, please find *stlite_browser_version.md* file and copy the full link (ctrl+a) from there to new tab at your browser.


## **How it works?** 
MatchMass takes at least one file with experimental results (m/z of signal and its abundance) and exactly one file containing theoretical m/z values with names of molecules. Then, it will perform matching using user-defined experimental errors, abundance threshold (minimum signal intensity), and ions of interest. Ions of molecules from theoretical table are found in the experimental data. The results of matching can be checked in plot and in table with aggregated results from all provided experimental files. Finally, the data can be downloaded as a MS Excel file containing all important details. 

### Now, let's check it step by step...

![Instructions: Figure 1](https://github.com/lukasustrnul/MatchMass/blob/main/instruct_jpg/matchmass_instructions_1.jpg 'Instructions: Figure 1')  








## **Technical comments and challenges during the development** 
Main application file in the repository is MatchMass.py. Other files contains additional content, data and function definitions.


## **References**  
[Read more about stlite and how it allows you to share apps built with streamlit](https://edit.share.stlite.net/?sampleAppId=intro)

Interested in chemistry? Read more about...  
[Mass spectrometry on wikipedia](https://en.wikipedia.org/wiki/Mass_spectrometry)  
[What are macrocycles?](https://en.wikipedia.org/wiki/Macrocycle)  
[What is supramolecular chemistry about?](https://en.wikipedia.org/wiki/Supramolecular_chemistry)
