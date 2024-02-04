# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 18:09:08 2024

@author: Lukáš Ustrnul
"""

import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Note: color combinations for plot bars were chosen based on their visibility for colorblind people
# An online tool from following link was used: https://venngage.com/tools/accessible-color-palette-generator 

def make_plot1(df1, theor_df_full, theor_width):
    """Creates first plot for comparing experimental data and theoretical m/z of selected ions."""
    # Create subplots
    fig = make_subplots()
    fig.add_trace(go.Bar(x=df1['exp_m/z'], 
                         y=df1['Abundance'], 
                         width = 0.0001, 
                         name = 'Experimental data',
                         marker={'color': '#00ffff'}
                         ))
    fig.add_trace(go.Bar(x=theor_df_full['m/z'], 
                         y=list((df1['Abundance'].max()) for num in range(len(theor_df_full['m/z']))),
                         width = theor_width, #
                         opacity = 0.4,
                         name = 'Theoretical m/z',
                         marker={'color': '#d0a300'}
                         ))
    
    # Set title
    fig.update_layout(
        title_text="Experimental data overlayed by theoretical m/z",
        xaxis_title="m/z",
        yaxis_title="Abundance",
    )
    
    
    # Add range slider
    fig.update_layout(
        autosize=True,
        xaxis=dict(
    
            rangeslider=dict(
                visible=True
            ),
            type="linear"
        )
    )
    
    # Add log/linear scale switch buttons
    updatemenus = [
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{"yaxis.type": "linear"}],
                    label="Linear Scale",
                    method="relayout"
                ),
                dict(
                    args=[{"yaxis.type": "log"}],
                    label="Log Scale",
                    method="relayout"
                )
            ]),
            font=dict(color="green"),
            #showactive=True,
            x=-0.1,
            xanchor="right",
            #y=1.2,
            #yanchor="bottom"
            ),
    ]  
    
    fig.update_layout(updatemenus=updatemenus)
    
    # Show the figure in the app
    return st.plotly_chart(fig, use_container_width=True)





def make_plot2(df2_orig, df2_matched):
    """Creates second plot showing which signals from original data were left unmatched"""
    # Create plot for our data
    fig = make_subplots()
    fig.add_trace(go.Bar(x=df2_orig['exp_m/z'], 
                         y=df2_orig['Abundance'], 
                         width = 0.0001, 
                         opacity = 1,
                         name = 'Unmatched signals',
                         marker={'color': '#cc2c3c'}
                         ))
    fig.add_trace(go.Bar(x=df2_matched['exp_m/z'], 
                         y=df2_matched['Abund'],
                         width = 0.0003, 
                         opacity = 1,
                         name = 'Matched signals',
                         marker={'color': '#3aff5c'}
                         ))
    
    # Set title
    fig.update_layout(
        title_text="Unmatched and matched signals from the selected file",
        xaxis_title="m/z",
        yaxis_title="Abundance",
        barmode = "overlay"
    )
    
    
    # Add range slider
    fig.update_layout(
        autosize=True,
        xaxis=dict(
    
            rangeslider=dict(
                visible=True
            ),
            type="linear"
        )
    )
    
    # Add log/linear scale switch buttons
    updatemenus = [
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{"yaxis.type": "linear"}],
                    label="Linear Scale",
                    method="relayout"
                ),
                dict(
                    args=[{"yaxis.type": "log"}],
                    label="Log Scale",
                    method="relayout"
                )
            ]),
            font=dict(color="green"),
            #showactive=True,
            x=-0.1,
            xanchor="right",
            #y=1.2,
            #yanchor="bottom"
            ),
    ]  
    
    fig.update_layout(updatemenus=updatemenus)
    
    # Show the figure in the app
    plot2 = st.plotly_chart(fig, use_container_width=True)
    return plot2