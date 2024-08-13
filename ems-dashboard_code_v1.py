import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO


# Set page title and title of the app
st.set_page_config(page_title='EMS Dashboard!!!', page_icon=":bar_chart:", layout="wide")
st.title('EMS QUALITY DASHBOARD :bar_chart:')
st.markdown('<style>div.block-container{padding-top:1rem;}<style>',unsafe_allow_html=True)


# File uploader
uploaded_file = st.file_uploader(":file_folder: Choose a file", type=["csv", "txt", "xlsx", "xls"])


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
            fig = px.bar(ict_data, x='Month', y='Number of Units tested', title="ICT - Number of Units tested and First Pass Yield %")
            fig.add_scatter(x=ict_data['Month'], y=ict_data['First Pass Yield %'], mode='lines+markers', name='First Pass Yield %', yaxis="y2")
            # fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right'))
            fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right', tickformat='.0%')) 
            st.plotly_chart(fig)


            if st.checkbox("View ICT Data"):
                transposed_ict_data = ict_data[['Month', 'First Pass Yield %']].T
                st.write(transposed_ict_data)
                xlsx_ict_data = to_excel(ict_data[['Month', 'First Pass Yield %']])
                st.download_button(label='📥 Download ICT Data as XLSX',
                                   data=xlsx_ict_data,
                                   file_name='ict_data.xlsx')


    # Plot bar chart for FCT
    with col4:
        fct_data = filtered_data[filtered_data['Testing Stage'] == 'FCT']
        if not fct_data.empty:
            st.write("FCT")
            fig = px.bar(fct_data, x='Month', y='Number of Units tested', title="FCT - Number of Units tested and First Pass Yield %")
            fig.add_scatter(x=fct_data['Month'], y=fct_data['First Pass Yield %'], mode='lines+markers', name='First Pass Yield %', yaxis="y2")
            # fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right'))
            fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right', tickformat='.0%')) 
            st.plotly_chart(fig)


            if st.checkbox("View FCT Data"):
                transposed_fct_data = fct_data[['Month', 'First Pass Yield %']].T
                st.write(transposed_fct_data)
                xlsx_fct_data = to_excel(fct_data[['Month', 'First Pass Yield %']])
                st.download_button(label='📥 Download FCT Data as XLSX',
                                   data=xlsx_fct_data,
                                   file_name='fct_data.xlsx')


    # Create columns for EOL and CAL bar charts
    col5, col6 = st.columns(2)


    # Plot bar chart for EOL
    with col5:
        eol_data = filtered_data[filtered_data['Testing Stage'] == 'EOL']
        if not eol_data.empty:
            st.write("EOL")
            fig = px.bar(eol_data, x='Month', y='Number of Units tested', title="EOL - Number of Units tested and First Pass Yield %")
            fig.add_scatter(x=eol_data['Month'], y=eol_data['First Pass Yield %'], mode='lines+markers', name='First Pass Yield %', yaxis="y2")
            # fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right'))
            fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right', tickformat='.0%')) 
            st.plotly_chart(fig)


            if st.checkbox("View EOL Data"):
                transposed_eol_data = eol_data[['Month', 'First Pass Yield %']].T
                st.write(transposed_eol_data)
                xlsx_eol_data = to_excel(eol_data[['Month', 'First Pass Yield %']])
                st.download_button(label='📥 Download EOL Data as XLSX',
                                   data=xlsx_eol_data,
                                   file_name='eol_data.xlsx')


    # Plot bar chart for CAL
    with col6:
        cal_data = filtered_data[filtered_data['Testing Stage'] == 'CAL']
        if not cal_data.empty:
            st.write("CAL")
            fig = px.bar(cal_data, x='Month', y='Number of Units tested', title="CAL - Number of Units tested and First Pass Yield %")
            fig.add_scatter(x=cal_data['Month'], y=cal_data['First Pass Yield %'], mode='lines+markers', name='First Pass Yield %', yaxis="y2")
            # fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right'))
            fig.update_layout(yaxis2=dict(title='First Pass Yield %', overlaying='y', side='right', tickformat='.0%')) 
            st.plotly_chart(fig)


            if st.checkbox("View CAL Data"):
                transposed_cal_data = cal_data[['Month', 'First Pass Yield %']].T
                st.write(transposed_cal_data)
                xlsx_cal_data = to_excel(cal_data[['Month', 'First Pass Yield %']])
                st.download_button(label='📥 Download CAL Data as XLSX',
                                   data=xlsx_cal_data,
                                   file_name='cal_data.xlsx')


    # Create time series analysis chart
    st.subheader("Time Series Analysis")
    time_series_chart = px.line(filtered_data, x='Month', y='First Pass Yield %', color='Testing Stage', title='First Pass Yield % Over Time')
    time_series_chart.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(time_series_chart)


    # Provide option to view and download data
    if st.checkbox("View Data of TimeSeries"):
        # filtered_data['Month'] = pd.to_datetime(filtered_data['Month'], format='%Y-%m').dt.strftime('%b %Y')
        filtered_data['Formatted Month'] = pd.to_datetime(filtered_data['Month']).dt.strftime('%b %Y')
        # transposed_data = filtered_data[['Month', 'First Pass Yield %']].T
        transposed_data = filtered_data[['Formatted Month', 'First Pass Yield %']].T
        st.write(transposed_data)


        # Provide option to download data as XLSX
        xlsx_data = to_excel(filtered_data[['Month', 'First Pass Yield %']])
        st.download_button(label='📥 Download Current Data as XLSX',
                           data=xlsx_data,
                           file_name='time_series_data.xlsx')
       


    import plotly.figure_factory as ff
    st.subheader(":point_right: Month wise Yield Summary")
    with st.expander("Summary_Table"):
        # df_sample = filtered_data[0:10][["Product","Month","Testing Stage","First Pass Yield %","Overall Fail %","Retest Pass %"]]
        # fig = ff.create_table(df_sample, colorscale="Cividis")
        # st.plotly_chart(fig, use_container_width=True)


        st.markdown("Month wise FPY Summary")
        # filtered_data['Month'] = pd.to_datetime(filtered_data['Month'], format='%Y-%m').dt.strftime('%b %Y')
        # monthly_fpy_summary = pd.pivot_table(data = filtered_data, values= "First Pass Yield %", index= ["Product","Testing Stage"], columns= "Month")
        # st.write(monthly_fpy_summary.style.background_gradient(cmap="Blues"))
        
        # def color_fpy(val):
        #     color = "red" if val <0.90 else "green" if val >=0.98 else "orange"
        #     return f'background-color: {color}'
        
        # def color_fpy(val):
        #     color = "red" if val < 0.90 else "green" if val >= 0.98 else "orange"
        #     return f'background-color: {color}; color: black'  # Add 'color: black' to set text color

        # color_fpy function to set the backgroud color of pivot table monthly_fpy_summary
        def color_fpy(val):
            if pd.isna(val):  # Check if the value is NaN (empty cell)
                return ""  # Return an empty string for system default styling
            color = "orange" if val < 0.90 else "#00ff00" if val >= 0.98 else "yellow" # 00ff00 is for light Green color to match the Monthly_FPY_Summary table
            return f'background-color: {color}; color: black'  # Add 'color: black' to set text color

        filtered_data['Month'] = pd.to_datetime(filtered_data['Month'], format='%Y-%m').dt.strftime('%b %Y')
        monthly_fpy_summary = pd.pivot_table(data = filtered_data, values= "First Pass Yield %", index= ["Product","Testing Stage"], columns= "Month")
        st.write(monthly_fpy_summary.style.applymap(color_fpy))
        # st.write(monthly_fpy_summary, unsafe_allow_html=True)
        # st.markdown(monthly_fpy_summary, unsafe_allow_html=True)


    # Create a tree based on Region, Category, Sub-Category
    st.subheader("Hierarchical view of Yield") # using TreeMap
    fig3 = px.treemap(filtered_data, path= ["Product","Testing Stage", "Month","First Pass Yield %"], values="Number of Units tested",
                    hover_data=["First Pass Yield %"], color="Month")
    fig3.update_layout(width = 800, height = 650)
    st.plotly_chart(fig3,use_container_width=True)


else:
    st.info("Please upload a file to get started")




# In this trial all the combination worked along with
# a option to view data of trime series in Tranposed manner and
# option to download in excel.
# The download option is given for col3-6
# update the date format to MMM-YYYY in the "Month wise FPY Summary" table
# derived from trial13 code clean up
# added Tree map for viewing
# changed the Y2 axis format to decimal to % format
# added a - color_fpy function to set the backgroud color of pivot table monthly_fpy_summary
