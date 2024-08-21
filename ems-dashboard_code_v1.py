import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import plotly.graph_objects as go


# Set page title and title of the app
st.set_page_config(page_title='EMS Dashboard!!!', page_icon=":bar_chart:", layout="wide")
st.title('EMS QUALITY DASHBOARD :bar_chart:')
st.markdown('<style>div.block-container{padding-top:1rem;}<style>',unsafe_allow_html=True)


# File uploader
uploaded_file = st.file_uploader(":file_folder: Choose Excel file", type=["csv", "txt", "xlsx", "xls"])
# st.write("If you have mapped Gdrive to PC follow the path to select Excel file <EMS Quality - FPY Improvement Pojects.xlsx>  :- Shared drives\EMS Quality\BFIH First Pass Yield Improvement")

# If a file is uploaded
if uploaded_file is not None:
    # Read the file based on the extension
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
        data = pd.read_excel(uploaded_file, sheet_name='ICT_FCT_EOL_CAL')
    else:
        st.error("Unsupported file format")
        st.stop()


    # Convert 'Month' column to datetime
    data['Month'] = pd.to_datetime(data['Month'])


    # Create columns for start and end date
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", min_value=data['Month'].min().date(), max_value=data['Month'].max().date(), value=data['Month'].min().date())
    with col2:
        end_date = st.date_input("End Date", min_value=data['Month'].min().date(), max_value=data['Month'].max().date(), value=data['Month'].max().date())
   
    # Sidebar filters
    st.sidebar.header("Choose your Product:")
    # products = st.sidebar.multiselect("Product", options=data['Product'].unique(), default=data['Product'].unique())
    # stages = st.sidebar.multiselect("Testing Stage", options=data['Testing Stage'].unique(), default=data['Testing Stage'].unique())
    products = st.sidebar.multiselect("Product", options=data['Product'].unique())
    stages = st.sidebar.multiselect("Testing Stage", options=data['Testing Stage'].unique())
    # Filter data based on sidebar filters and date range
    filtered_data = data[(data['Product'].isin(products)) & (data['Testing Stage'].isin(stages)) &
                         (data['Month'] >= pd.to_datetime(start_date)) & (data['Month'] <= pd.to_datetime(end_date))]


    # Ensure 'Month' is treated as a categorical variable for plotting purposes
    filtered_data['Month'] = filtered_data['Month'].dt.strftime('%Y-%m')


    # Create subheader for bar charts
    st.subheader("Testing Stage Wise Yield")


    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()
        processed_data = output.getvalue()
        return processed_data


    # Create columns for bar charts
    col3, col4 = st.columns(2)


    # Plot bar chart for ICT
    with col3:
        ict_data = filtered_data[filtered_data['Testing Stage'] == 'ICT']
        if not ict_data.empty:
            st.write("ICT")
            fig = px.bar(ict_data, x='Month', y='Number of Units tested')
            fig.add_scatter(x=ict_data['Month'], y=ict_data['First Pass Yield %'], mode='lines+markers', name='First Pass Yield %', yaxis="y2")
            # fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right'))
            fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right', tickformat='.0%')) 
            st.plotly_chart(fig)


            if st.checkbox("View ICT Data"):
                transposed_ict_data = ict_data[['Month', 'First Pass Yield %']].T
                st.write(transposed_ict_data)

    # Plot bar chart for FCT
    with col4:
        fct_data = filtered_data[filtered_data['Testing Stage'] == 'FCT']
        if not fct_data.empty:
            st.write("FCT")
            fig = px.bar(fct_data, x='Month', y='Number of Units tested')
            fig.add_scatter(x=fct_data['Month'], y=fct_data['First Pass Yield %'], mode='lines+markers', name='First Pass Yield %', yaxis="y2")
            # fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right'))
            fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right', tickformat='.0%')) 
            st.plotly_chart(fig)


            if st.checkbox("View FCT Data"):
                transposed_fct_data = fct_data[['Month', 'First Pass Yield %']].T
                st.write(transposed_fct_data)



    # Create columns for EOL and CAL bar charts
    col5, col6 = st.columns(2)


    # Plot bar chart for EOL
    with col5:
        eol_data = filtered_data[filtered_data['Testing Stage'] == 'EOL']
        if not eol_data.empty:
            st.write("EOL")
            fig = px.bar(eol_data, x='Month', y='Number of Units tested')
            fig.add_scatter(x=eol_data['Month'], y=eol_data['First Pass Yield %'], mode='lines+markers', name='First Pass Yield %', yaxis="y2")
            # fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right'))
            fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right', tickformat='.0%')) 
            st.plotly_chart(fig)


            if st.checkbox("View EOL Data"):
                transposed_eol_data = eol_data[['Month', 'First Pass Yield %']].T
                st.write(transposed_eol_data)



    # Plot bar chart for CAL
    with col6:
        cal_data = filtered_data[filtered_data['Testing Stage'] == 'CAL']
        if not cal_data.empty:
            st.write("CAL")
            fig = px.bar(cal_data, x='Month', y='Number of Units tested')
            fig.add_scatter(x=cal_data['Month'], y=cal_data['First Pass Yield %'], mode='lines+markers', name='First Pass Yield %', yaxis="y2")
            # fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right'))
            fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right', tickformat='.0%')) 
            st.plotly_chart(fig)


            if st.checkbox("View CAL Data"):
                transposed_cal_data = cal_data[['Month', 'First Pass Yield %']].T
                st.write(transposed_cal_data)




    
    import plotly.figure_factory as ff
    st.subheader(":point_right: Month wise Yield Summary")
    # with st.expander("Summary_Table"):
    st.write("Summary_Table")
    def color_fpy(val):
        if pd.isna(val):  # Check if the value is NaN (empty cell)
            return ""  # Return an empty string for system default styling
        color = "orange" if val < 0.90 else "#00ff00" if val >= 0.98 else "yellow" # 00ff00 is for light Green color to match the Monthly_FPY_Summary table
        return f'background-color: {color}; color: black'  # Add 'color: black' to set text color

    filtered_data['Month'] = pd.to_datetime(filtered_data['Month'], format='%Y-%m').dt.strftime('%b %Y')
    monthly_fpy_summary = pd.pivot_table(data = filtered_data, values= "First Pass Yield %", index= ["Product","Testing Stage"], columns= "Month")
    st.write(monthly_fpy_summary.style.applymap(color_fpy))
    
    st.subheader("Testing Stage Wise Yield Distribution")

    #Add Pie chart to display FPY%, Retest Pass%, Real Fail%
    # st.subheader("Product Quality Metrics")
    pie1, pie2 = st.columns(2)
    with pie1:        
        st.write("ICT Yield Distribution")
        ict_data = filtered_data[filtered_data['Testing Stage'] == 'ICT']
        if not ict_data.empty:
            # Aggregate data for pie chart
            aggregated_data = {
                "Metric": ["First Pass Yield %", "Retest Pass %", "Real Fail %"],
                "Value": [
                    ict_data["First Pass Yield %"].mean(),
                    ict_data["Retest Pass %"].mean(),
                    ict_data["Real Fail %"].mean()
                ]
            }
            # Create aggregated DataFrame
            agg_df = pd.DataFrame(aggregated_data)            
            # fig = px.pie(agg_df, values= "Value", names= "Metric", hole = 0.5, template= "plotly_dark", pull=[0, 0, 0.2])
            fig = go.Figure(
                data=[go.Pie(
                    labels=agg_df["Metric"], 
                    values=agg_df["Value"], 
                    hole=0.5,  # Set the hole size for the pie chart
                    pull=[0, 0.2, 0.2]  # Pull sectors for "Retest Pass %" and "Real Fail %"
                )]
            )
            fig.update_traces(textposition = "outside")
            st.plotly_chart(fig, use_container_width=True)

    with pie2:        
        st.write("FCT Yield Distribution")
        fct_data = filtered_data[filtered_data['Testing Stage'] == 'FCT']
        if not fct_data.empty:
            # Aggregate data for pie chart
            aggregated_data = {
                "Metric": ["First Pass Yield %", "Retest Pass %", "Real Fail %"],
                "Value": [
                    fct_data["First Pass Yield %"].mean(),
                    fct_data["Retest Pass %"].mean(),
                    fct_data["Real Fail %"].mean()
                ]
            }
            # Create aggregated DataFrame
            agg_df = pd.DataFrame(aggregated_data)            
            # fig = px.pie(agg_df, values= "Value", names= "Metric", hole = 0.5, template= "plotly_dark", title="FCT Yield Distribution")
            fig = go.Figure(
                data=[go.Pie(
                    labels=agg_df["Metric"], 
                    values=agg_df["Value"], 
                    hole=0.5,  # Set the hole size for the pie chart
                    pull=[0, 0.2, 0.2]  # Pull sectors for "Retest Pass %" and "Real Fail %"
                )]
            )
            fig.update_traces(textposition = "outside")
            st.plotly_chart(fig, use_container_width=True)
    
    pie3, pie4 = st.columns(2)
    with pie3:
        st.write("EOL Yield Distribution")
        eol_data = filtered_data[filtered_data['Testing Stage'] == 'EOL']
        if not eol_data.empty:
            # Aggregate data for pie chart
            aggregated_data = {
                "Metric": ["First Pass Yield %", "Retest Pass %", "Real Fail %"],
                "Value": [
                    eol_data["First Pass Yield %"].mean(),
                    eol_data["Retest Pass %"].mean(),
                    eol_data["Real Fail %"].mean()
                ]
            }
            # Create aggregated DataFrame
            agg_df = pd.DataFrame(aggregated_data)            
            # fig = px.pie(agg_df, values= "Value", names= "Metric", hole = 0.5, template= "plotly_dark")
            fig = go.Figure(
                data=[go.Pie(
                    labels=agg_df["Metric"], 
                    values=agg_df["Value"], 
                    hole=0.5,  # Set the hole size for the pie chart
                    pull=[0, 0.2, 0.2]  # Pull sectors for "Retest Pass %" and "Real Fail %"
                )]
            )
            fig.update_traces(textposition = "outside")
            st.plotly_chart(fig, use_container_width=True)

    with pie4:
        st.write("CAL Yield Distribution")
        cal_data = filtered_data[filtered_data['Testing Stage'] == 'CAL']
        if not cal_data.empty:
            # Aggregate data for pie chart
            aggregated_data = {
                "Metric": ["First Pass Yield %", "Retest Pass %", "Real Fail %"],
                "Value": [
                    cal_data["First Pass Yield %"].mean(),
                    cal_data["Retest Pass %"].mean(),
                    cal_data["Real Fail %"].mean()
                ]
            }
            # Create aggregated DataFrame
            agg_df = pd.DataFrame(aggregated_data)            
            # fig = px.pie(agg_df, values= "Value", names= "Metric", hole = 0.5, template= "plotly_dark")
            fig = go.Figure(
                data=[go.Pie(
                    labels=agg_df["Metric"], 
                    values=agg_df["Value"], 
                    hole=0.5,  # Set the hole size for the pie chart
                    pull=[0, 0.2, 0.2]  # Pull sectors for "Retest Pass %" and "Real Fail %"
                )]
            )
            fig.update_traces(textposition = "outside")
            st.plotly_chart(fig, use_container_width=True)
                      
    # Create a tree based on Region, Category, Sub-Category
    st.subheader("Hierarchical view of Yield") # using TreeMap
    fig3 = px.treemap(filtered_data, path= ["Product","Testing Stage", "Month","First Pass Yield %"], values="Number of Units tested",
                    hover_data=["First Pass Yield %"], color="Month")
    fig3.update_layout(width = 800, height = 650)
    st.plotly_chart(fig3,use_container_width=True)


else:
    st.info("Please upload a file to get started")
