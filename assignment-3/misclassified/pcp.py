import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Prediction Analysis - Parallel Coordinates')

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    
    # Calculate and display accuracy
    accuracy = df['CorrectPrediction'].mean() * 100
    st.write(f"Model Accuracy: {accuracy:.2f}%")
    
    # Get numeric columns for feature selection
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_columns = [col for col in numeric_columns if col != 'CorrectPrediction']
    
    # Feature selection
    st.write("Select 4 features for the parallel coordinates plot:")
    selected_features = st.multiselect('Select features:', 
                                     numeric_columns,
                                     max_selections=4)
    
    if len(selected_features) == 4:
        # Add CorrectPrediction to the selected features
        features_to_plot = selected_features.copy()
        
        # Create parallel coordinates plot
        fig = px.parallel_coordinates(
            df,
            dimensions=features_to_plot,
            color='CorrectPrediction',
            color_discrete_map={1: 'blue', 0: 'red'},
            title='Parallel Coordinates Plot'
        )
        
        # Update layout for better visibility
        fig.update_layout(
            showlegend=True,
            plot_bgcolor='lightgray',
            paper_bgcolor='lightgray',
            font=dict(color='black'),
        )
        
        # Display plot
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Please select exactly 4 features.")