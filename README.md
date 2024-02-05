# MatchMass - Mass Spectrometry Matching Tool
### Compare your experimental data from mass spectrometry (MS) with a table of theoretical mass-to-charge ratio (m/z) values to quickly find out which molecules and ions of interest are present in the sample.
***
## **Brief overview**  
Mass spectrometry is very sensitive and precise analytical technique for identification and quantification of molecules; therefore, it isused in many fields of science. MatchMass was developed to provide free easy-to-use tool to help researchers with identification of molecules in complex mixtures. The MatchMass was developed during the chemical research focused to study mechanism of macrocyclization reactions. Additional information about our motivation and research can be found in the app itself. 

In the near future, MatchMass will be hosted at Tallinn University of Technology domain (taltech.ee). However, you can test it as a **locally running browser version** made in [stlite](https://edit.share.stlite.net/?sampleAppId=intro). The app code and data are encoded into the URL as a hash like `https://share.stlite.net/#!ChBz...`. Probably due to the excessive length of the link I was not able to make a functional hyperlink here in GitHub. Therefore, please find *stlite_browser_version.md* file and copy the full link (ctrl+a) from there to new tab at your browser.


## **How it works?** 
MatchMass takes at least one file with experimental results (m/z of signal and its abundance) and exactly one file containing theoretical m/z values with names of molecules. Then, it will perform matching using user-defined experimental errors, abundance threshold (minimum signal intensity), and ions of interest. Ions of molecules from theoretical table are found in the experimental data. The results of matching can be checked in plot and in table with aggregated results from all provided experimental files. Finally, the data can be downloaded as a MS Excel file containing all important details. 

### Now, let's check it step by step...
Check for the numbers in following figures  
1. Notice expanders with information about project, authors, funding and detailed instructuions how to use the MatchMass
2. Let's assume you dont have your own data at the moment. You can download our example files of experimental data and table of theoretical molecules
3. Upload the experimental and theoretical files to correct upload fields
* In the next step, you need to set experimental error. Ideally, based on the precision of your MS instrument. Abundance can be set to zero or higher if you are not interested in signals of low intensity.
4. If you want to set different experimental error or abundance threshold for each experimental file then you can change it to "Yes" and table of files will appear.
5. Set the error to 0.01 and abundance to 0.00 for our example files.
6. Pick ions from particular column based on the mode of measurement. Example data contains ions from positive mode MS; thereofore, you can select some or all checkboxes from the first column.
* Now, you can visually check which areas and signals will be matched using current settings for experimental error and ions.
7. Choose which experimental file you want to see in the plot.
8. You can switch the plot to logarithmic scale to improve visibility of low abundance signals.
9. Use slider to check specific regions of your MS data.
10. You can also zoom directly in the plot and move along x-axis with the help of slider.
11. If you dont see overlap of experimental data and theoretical m/z, then you can increase experimental error or add more ions.
12. Hit the "Find matching signals!" button.
13. Message informing about successful or failed matching will appear under the button.
14. Select which file you want to see at the plot.
15. You can visually check which signals were matched. Navigation through the plot is same as in the previous plot.
16. Table contains results of matching for all uploaded experimental files
17. Click to download MS Excel file with complete results
18. Excel file contains: sheet with overview of all uploaded files and used experimental errors, sheet with full table of theoretical m/z (including all ions and ID number generated for each original molecule), sheet with aggregated results from all files as shown in the app, sheet for each uploaded file with matching results for the particular file. 

   




![Instructions: Figure 2](https://github.com/lukasustrnul/MatchMass/blob/main/instruct_jpg/matchmass_instructions_1.jpg 'Instructions: Figure 3') 





## **Technical comments and challenges during the development** 
Main application file in the repository is MatchMass.py. Other files contains additional content, data and function definitions.


## **References**  
[Read more about stlite and how it allows you to share apps built with streamlit](https://edit.share.stlite.net/?sampleAppId=intro)

Interested in chemistry? Read more about...  
[Mass spectrometry on wikipedia](https://en.wikipedia.org/wiki/Mass_spectrometry)  
[What are macrocycles?](https://en.wikipedia.org/wiki/Macrocycle)  
[What is supramolecular chemistry about?](https://en.wikipedia.org/wiki/Supramolecular_chemistry)
