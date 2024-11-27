import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title('Prediction Analysis - Scatter Plot')

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
    col1, col2 = st.columns(2)
    with col1:
        x_feature = st.selectbox('Select X-axis feature:', numeric_columns)
    with col2:
        y_feature = st.selectbox('Select Y-axis feature:', 
                                [col for col in numeric_columns if col != x_feature])
    
    # Create scatter plot
    fig = px.scatter(df, 
                    x=x_feature, 
                    y=y_feature,
                    color='CorrectPrediction',
                    color_discrete_map={1: 'blue', 0: 'red'},
                    labels={'CorrectPrediction': 'Correctly Predicted'},
                    title=f'{x_feature} vs {y_feature} by Prediction Correctness')
    
    # Update layout
    fig.update_layout(
        legend_title_text='Correctly Predicted',
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )
    
    # Display plot
    st.plotly_chart(fig, use_container_width=True)