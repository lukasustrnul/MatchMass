# [MatchMass - Mass Spectrometry Matching Tool](https://matchmass.taltech.ee/)
### Compare your experimental data from mass spectrometry (MS) with a table of theoretical mass-to-charge ratio (m/z) values to quickly find out which molecules and ions of interest are present in the sample.
***
Note: Main application file in the repository is MatchMass_main.py. Other files contains additional content, data and function definitions.

## **Main Goal** 
_Provide user-friendly tool which will be able to find matches between large sets of experimental values and a list of theoretical values of interest._

## **Brief Overview**  
Mass spectrometry is very sensitive and precise analytical technique for identification and quantification of molecules; therefore, it isused in many fields of science. MatchMass was developed to provide free easy-to-use tool to help researchers with identification of molecules in complex mixtures. The MatchMass was developed during the chemical research focused to study mechanism of macrocyclization reactions. Additional information about our motivation and research can be found in the app itself. Script for data matching was written in Python, hence it seemed logical to use [Streamlit](https://streamlit.io/) for developing it into web application.  

In the near future, MatchMass will be hosted at Tallinn University of Technology domain (taltech.ee) at the address [matchmass.taltech.ee](https://matchmass.taltech.ee/). However, it is temporarily deployed at [https://matchmass.streamlit.app/](https://matchmass.streamlit.app/) where you can test it (hosted at [streamlit community cloud](https://streamlit.io/cloud)). 

### Functions of MatchMass
- Load tables containing experimental data and theoretical masses of molecules provided by user.
- Set the limits of matching by defining experimental error of machine and minimum signal intensity (abundance) of interest.
- Generate mass-to-charge (_m/z_) values for ions of interest from the provided theoretical masses of neutral molecules.
- Provide simple plot for visual comparison between experimental results and theoretical _m/z_ values before matching.
- Do the matching. This means finding and returning experimental values corresponding (within user-defined limits) to the molecules (ions) in the theoretical table.
- Show results of matching in a plot.
- Generate excel file with overview of matching settings, all results, and theoretical table containing all ions.
- Users may downoad our dummy data to test the MatchMass without having their own data.

## **Why Is Such a Tool Needed?**
Although MS is very widely used method and various free online tools exist, we did not find any which would be particularly useful for exploring complex mixtures. Common available tools usually accept only one value at the time or a text input to generate exact mass or isotopic patterns based on chemical formula. Precise calculators of ion m/z values exists in various forms but always work with mass of one chemical compound at the time which means a lot of manual work if we need to generate m/z values for longer list of molecules. Finally, we did not find any tool which could check experimental results for the presence of multiple terget molecules at once. We suppose that some professional software may have such feature(s), but most programs for scientific purposes are very expensive, so it is only worth investing in them if they are used regularly.

_Therefore, main benefits of MatchMass are:_ **(1.)** possibility to **upload table** of theoretical masses, **(2.)** calculate _m/z_ of ions **for each molecule** in the provided table and **(3.)** quickly compare experimental data to a long list (table) of theoretical _m/z_ values.

## **Further Plans**
- Add tests to make it easier for others to contribute to the development of MatchMass
- Add security features to reduce risks related to upload of files containing malicious code

## **How It Works?** 
MatchMass takes at least one file with experimental results (_m/z_ of signal and its abundance) and exactly one file containing theoretical _m/z_ values with names of molecules. Then, it will perform matching using user-defined experimental errors, abundance threshold (minimum signal intensity), and ions of interest. Ions of molecules from theoretical table are found in the experimental data. The results of matching can be checked in plot and in table with aggregated results from all provided experimental files. Finally, the data can be downloaded as a MS Excel file containing all important details. 

### Now, let's check it step by step...
Check for the numbers in following figures  
1. Notice expanders with information about project, authors, funding and detailed instructuions how to use the MatchMass
2. Let's assume you dont have your own data at the moment. You can download our example files of experimental data and table of theoretical molecules
3. Upload the experimental and theoretical files to correct upload fields
![Instructions: Figure 1](https://github.com/lukasustrnul/MatchMass/blob/main/instr/matchmass_instructions_1edit.jpg 'Instructions: Figure 1')
* In the next step, you need to set experimental error. Ideally, based on the precision of your MS instrument. Abundance can be set to zero or higher if you are not interested in signals of low intensity.
4. If you want to set different experimental error or abundance threshold for each experimental file then you can change it to "Yes" and table of files will appear.
5. Set the error to 0.01 and abundance to 0.00 for our example files.
![Instructions: Figure 2](https://github.com/lukasustrnul/MatchMass/blob/main/instr/matchmass_instructions_2edit.jpg 'Instructions: Figure 2')
6. Pick ions from particular column based on the mode of measurement. Example data contains ions from positive mode MS; thereofore, you can select some or all checkboxes from the first column.
![Instructions: Figure 3](https://github.com/lukasustrnul/MatchMass/blob/main/instr/matchmass_instructions_3edit.jpg 'Instructions: Figure 3')
* Now, you can visually check which areas and signals will be matched using current settings for experimental error and ions.
7. Choose which experimental file you want to see in the plot.
8. You can switch the plot to logarithmic scale to improve visibility of low abundance signals.
9. Use slider to check specific regions of your MS data.
10. You can also zoom directly in the plot and move along x-axis with the help of slider.
11. If you dont see overlap of experimental data and theoretical m/z, then you can increase experimental error or add more ions.
![Instructions: Figure 4](https://github.com/lukasustrnul/MatchMass/blob/main/instr/matchmass_instructions_4edit.jpg 'Instructions: Figure 4')
12. Hit the "Find matching signals!" button.
![Instructions: Figure 5](https://github.com/lukasustrnul/MatchMass/blob/main/instr/matchmass_instructions_5edit.jpg 'Instructions: Figure 5')
13. Message informing about successful or failed matching will appear under the button.
14. Select which file you want to see at the plot.
15. You can visually check which signals were matched. Navigation through the plot is same as in the previous plot.
![Instructions: Figure 6](https://github.com/lukasustrnul/MatchMass/blob/main/instr/matchmass_instructions_6edit.jpg 'Instructions: Figure 6')
16. Table contains results of matching for all uploaded experimental files
17. Click to download MS Excel file with complete results
18. Excel file contains: sheet with overview of all uploaded files and used experimental errors, sheet with full table of theoretical m/z (including all ions and ID number generated for each original molecule), sheet with aggregated results from all files as shown in the app, sheet for each uploaded file with matching results for the particular file.
![Instructions: Figure 7](https://github.com/lukasustrnul/MatchMass/blob/main/instr/matchmass_instructions_7edit.jpg 'Instructions: Figure 7') 

   
## **Challenges and Limitations Encountered During The Development** 
As someone completely new to web development, I tried to approach building MatchMass in the simplest and most straightforward way possible. Indeed, some of the parts of code could be better optimized or written in a different way which could look more structured.  
Applications made in Streamlit run all of the code from the beginning till the end after each user's interaction with an app. This leads to two typical issues which I have encountered. First, until files are uploaded or values set in some of widgets it may easily happen that some variables cannot have any content yet and running of code brings some sort of error (usually KeyError). Good example is displaying of the first plot which needs experimental data and a table of theoretical masses tranformed into masses of ions. However, there was no dataframe to display until an ion was picked in checkboxes and KeyError occured because plotly could not find a column with expected name. This an similar problems were mostly solved by adding except clause which returned empty dataframe but with expected column names. 

Second, some of the widgets may "forget" user's previous input if a change in another widget initiated rerun of the app. Such an issue can be solved with streamlit session_state which works similarly as python dictionary. In addition, session_state can be employed to optimize the speed of app by keeping data which took longer to calculate. While being aware of possible problems, I have initially written the MatchMass without using session_state to evaluate which parts and widgets really needs the session_state and which does not. To my surprise, most parts of MatchMass worked without problem even without implemented session state. Main issue was a loss of values from input of experimental error, abundance threshold, and also matched results after a download of results initiated by corresponding button. Nevertheless, I tried to implement session_state to most parts of the MatchMass. 

Now, I will briefly comment on each functionality in regards to session_state use. First, there was no need for session_state for expanders which only shows additional information and instructions. Second, I considered to use session_state in the data upload process; however, I was not sure how exactly streamlit operates with upload objects and if there is really need to save the dataframes to session state. Transformation of upload object into dataframe seemed fast; therefore, I decided not to use any memory for keeping dataframes in the session state. If necessary it can be considered in future to add sessions states for this or some other steps. 

Next, the session state was used to keep radio button state as well as values of experimental error and abundance threshold in the case that user is switching radio button between "No" and "Yes". Moreover, I wanted values which have been set when radio == "No" to translate to all rows of a table shown when radio == "Yes". Although, my code worked, there was possibility of scenario (editing values for each file separately and then switching  radio buton to "No" and back to "Yes" without changing any value) in which users would see in the table different values (all the same) than the ones which would be used (individually set before switching radio repeatedly) in matching process. Nevertheless, this functionality is not necessary. 

Further, I tried to add session state in the step of ion picking to avoid generating complete theoretical table in each rerun of the MatchMass. However, strange behavior was observed. It was difficult to understand what is the cause but it may have been related to fact that checkboxes are generated in for loop. In the end, a theoretical table will likely not have thousands of theoretical molecules provided by user; therefore, generating the complete table with selected ions should be relatively quick.

Finally, the main need for session state was to hold results of matching after the "matching" button was pushed. There are two reasons for that. First, matching is done only upon pushing the button so without having the results in session state the results vanished everytime when user interacted with other parts of the app (case described at the beginning of this section). Second, in the case of large or multiple files, the matching is the most demanding process and it is not desirable to do this process in each rerun of the app which is also reason why the process is initiated by pressing the button.


## **References** 
[Do you have experience with python and considering to build an web app, check Streamlit!](https://streamlit.io/)  

[Read more about stlite and how it allows you to share apps built with streamlit](https://edit.share.stlite.net/?sampleAppId=intro)

Interested in chemistry? Read more about...  
[Mass spectrometry on wikipedia](https://en.wikipedia.org/wiki/Mass_spectrometry)  
[What are macrocycles?](https://en.wikipedia.org/wiki/Macrocycle)  
[What is supramolecular chemistry about?](https://en.wikipedia.org/wiki/Supramolecular_chemistry)
