import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px # interactive charts 
from wordcloud import WordCloud

# Navbar
from streamlit_option_menu import option_menu

# ISO 3166
import pycountry
import pycountry_convert as coco


# # Automated EDA
# from pandas_profiling import ProfileReport
# from streamlit_pandas_profiling import st_profile_report

# Membaca datasets
df = pd.read_csv('ds_salaries.csv')


# convert country code iso 3166 to country name
# company location
def convert_country_code_to_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name
    except LookupError:
        return "Unknown"

# Menerapkan fungsi konversi pada kolom "company_location"
df["country_company"] = df["company_location"].apply(convert_country_code_to_name)
# Menampilkan df yang telah dikonversi
print(df)

# employee residence
def convert_country_code_to_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name
    except LookupError:
        return "Unknown"

# Menerapkan fungsi konversi pada kolom "employee_residence"
df["country_employee"] = df["employee_residence"].apply(convert_country_code_to_name)

# Menampilkan df yang telah dikonversi
print(df)

# side bar
st.sidebar.image('UINSA.png', caption="Final Project Data Visualization")

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
year = st.sidebar.multiselect(
    "Select the Year:",
    options=df["work_year"].unique(),
    default=df["work_year"].unique()
)

df_selection = df.query(
    "work_year == @year"
)
# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
country = st.sidebar.multiselect(
    "Select the Location:",
    options=df["country_company"].unique(),
    default=df["country_company"].unique()
)

# MEDIA QUERY UNTUK SELEKSI FILTER
df_location = df.query(
    "country_company == @country & work_year == @year"
)

st.markdown("# Data Science Salaries")
# Sub Judul
st.markdown("Explore the dataset to know more about Data Science Salaries")

selected = option_menu(
    menu_title=None,  # required
    options=["EDA", "Processing & Visualizations", "Proportion"],  # required
    icons=["clipboard-data", "bar-chart", "pie-chart"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
)

if selected == "EDA": 
    st.markdown("## Exploratory Data Analysis")
    # Dataframe
    st.markdown("### Detailed Data View")
    st.dataframe(df_selection)
    # time.sleep(1)
    # # STATISTIC DESCRIPTIVE
    st.subheader('Statistic Descriptive')
    st.write(df_selection.describe().T)
    # CHECK NULL VALUE
    st.subheader('Checkin Null Value')
    st.write(df.isnull().sum())
    # #Automated EDA
    # pr = ProfileReport(df, explorative=True)
    # st.header('**Pandas Profiling Report**')
    # st_profile_report(pr)

if selected == "Processing & Visualizations":
    st.markdown("## Data Processing and Visualization")
    # st.markdown("### Top Jobs For Each Work Year ")
    # # ---- SIDEBAR ----
    # st.sidebar.header("Please Filter Here:")
    # year = st.sidebar.multiselect(
    #     "Select the Year:",
    #     options=df["work_year"].unique(),
    #     default=df["work_year"].unique()
    # )
    # # Filter 
    # top_filter = st.sidebar.selectbox("Select the Year", pd.unique(df['work_year']))
    # # creating a single-element container.
    # placeholder = st.empty()
    # filter dataframe 
    # df = df[df['work_year']==year]

    # fig2 = px.histogram(data_frame = df, y = 'job_title')
    # st.write(fig2)


    st.markdown("### Top 5 Jobs with Most Employees ")
    # top_5 = df['job_title'].value_counts().nlargest(5).reset_index()
    # fig2 = px.bar(data_frame=top_5, y='index', x='job_title', orientation='h', title='Top 10 Job')

    # fig2.update_layout(
    #     yaxis={'title': 'Job Titles'},
    #     yaxis_autorange='reversed',
    #     xaxis={'title': 'Employees'}
    # )

    # st.plotly_chart(fig2)

    top_5 = df_selection['job_title'].value_counts().nlargest(5).reset_index()
    fig2 = px.bar(data_frame=top_5, x='index', y='job_title', title='Chart of Top 5 Job Titles', color = top_5['job_title'], color_continuous_scale='Sunset')

    fig2.update_layout(
        xaxis={'title': 'Job Titles'},
        yaxis={'title': 'Employees'}
    )
    st.plotly_chart(fig2)

    st.markdown("### Top 5 Jobs with Average Salaries ")

    top_salary = df_selection.groupby('job_title').agg({'salary_in_usd':'mean'}).sort_values(by='salary_in_usd', ascending=False).head(5)
    st.write(top_salary.head(5))

    # fig = px.bar(data_frame=top_salary, x=top_salary.index, y='salary_in_usd',title='Chart of Top 5 Jobs with Average Salaries')
    # fig.update_layout(
    #     # xaxis_tickangle=-45
    #     xaxis={'title': 'Job Titles'},
    #     yaxis={'title': 'Average Salaries'}
    #     )
    # st.plotly_chart(fig)

    fig = px.bar(data_frame=top_salary, x='salary_in_usd', y=top_salary.index, orientation='h',title='Top 5 Jobs with Average Salaries', color = 'salary_in_usd', color_continuous_scale='Sunsetdark')
    fig.update_layout(
        xaxis={'title': 'Job Titles'},
        yaxis={'title': 'Average Salaries'},
        yaxis_autorange='reversed'
        )
    st.plotly_chart(fig)

    st.markdown("### Average Salary Based On Experience Level ")
    df_selection['experience_level'].replace(['SE','MI','EN','EX'],["Senior-level / Expert","Mid-level / Intermediate","Entry-level / Junior","Executive-level / Director"],inplace=True)

    avg_salary = df_selection.groupby('experience_level').agg({'salary_in_usd':'mean'}).sort_values(by='salary_in_usd', ascending=False).head(5)
    st.write(avg_salary.head(5))

    fig = px.bar(data_frame=avg_salary, x=avg_salary.index, y='salary_in_usd',title='Chart of Average Salary Based on Experience Level', color = 'salary_in_usd', color_continuous_scale='Magenta')
    fig.update_layout(
        # xaxis_tickangle=-45
        xaxis={'title': 'Experience Level'},
        yaxis={'title': 'Average Salaries'}
        )
    st.plotly_chart(fig)

    # # MAP 
    # st.markdown("### Job Data Distribution ")
    # # Map 1
    # data_of_map = pd.DataFrame(
    #     df['job_title'],
    #     columns=["country_company", "country_employee"],
    # )
    # st.map(data_of_map)
 
    # salary_location = df.groupby(['salary_in_usd','company_location']).size().reset_index()
    # average = salary_location.groupby('company_location').mean().reset_index()

    # fig = px.choropleth(locations=average['company_location'],
    #                     color=average['salary_in_usd'],
    #                     color_continuous_scale=px.colors.sequential.solar,
    #                     template='plotly_dark',
    #                     title = '6.5. Average Salary by Company Location')
    # fig.update_layout(font = dict(size=17,family="Franklin Gothic"))
    # st.plotly_chart(fig)



    # Perbandingan rata rata gaji berdasar lokasi perusahaan
    st.markdown("### Comparison of The Average Salary Between Jobs in Each Company Location ")

    # df['company_location'].replace(['ES','US','CA','DE','GB','NG','IN','HK','NL'],
    #                                ["Spain",],inplace=True)


    # top_filter = st.sidebar.selectbox("Select Location", pd.unique(df['company_location']))
    # df = df[df['company_location']==top_filter]


    avrg_salary = df_location.groupby('job_title').agg({'salary_in_usd':'mean'}).sort_values(by='salary_in_usd', ascending=False)
    st.write(avrg_salary)

    fig = px.bar(data_frame=avrg_salary, x='salary_in_usd', y=avrg_salary.index, orientation='h',title='Chart of Comparison Average Salaries by Company Location', color = 'salary_in_usd', color_continuous_scale='Bluyl')
    fig.update_layout(
        xaxis={'title': 'Job Titles'},
        yaxis={'title': 'Average Salaries'},
        yaxis_autorange='reversed'
        )
    st.plotly_chart(fig)


    # Word cloud
    st.markdown("### Word Cloud")

    # Preprocessing teks
    text = df_location['job_title'].values
    text = ' '.join(text)

    # Sidebar untuk mengatur parameter WordCloud
    st.sidebar.title("WordCloud Options")
    max_words = st.sidebar.slider("Max Words", min_value=100, max_value=2000, value=1000)
    background_color = st.sidebar.selectbox("Background Color", ["black", "white"])
    collocations = st.sidebar.checkbox("Include Collocations", value=False)

    # Membuat WordCloud
    wc = WordCloud(background_color=background_color, width=1200, height=600,
                contour_width=0, contour_color="#410F01", max_words=max_words,
                scale=1, collocations=collocations, repeat=True, min_font_size=1)

    # Mengenerate dan menampilkan WordCloud saat ada perubahan pada parameter
    @st.cache
    def generate_wordcloud():
        wc.generate(text)
        plt.figure(figsize=[12, 6])
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        return plt

    # Menampilkan WordCloud dalam aplikasi Streamlit
    st.title("Top Words in the Text")
    st.pyplot(generate_wordcloud())

# Proporsi
if selected == "Proportion":

    # Membuat diagram pie dengan Streamlit

    # Proporsi experience level
    st.title('Proportion')

    st.markdown("## Proportion of Experience Level")

    col1, col2 = st.columns(2)
    with col1:
        df_location['experience_level'].replace(['SE','MI','EN','EX'],["Senior-level / Expert","Mid-level / Intermediate","Entry-level / Junior","Executive-level / Director"],inplace=True)
        experience_counts = df_location['experience_level'].value_counts()
        
        # st.markdown("Frequency of Experience Level")
        top_5 = df_location['experience_level'].value_counts().reset_index().head(5)
        fig_bar = px.bar(data_frame=top_5, x='index', y='experience_level', title='Frequency of Experience Level',
                        color='experience_level', color_discrete_sequence= px.colors.sequential.Plasma_r)
        fig_bar.update_layout(xaxis={'title': 'Experience Level'}, yaxis={'title': 'Frequency'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # st.markdown("Proportion of Experience Level")
        fig_pie = px.pie(names=experience_counts.index, values=experience_counts.values,
                        title='Proportion of Experience Level')
        st.plotly_chart(fig_pie, use_container_width=True)

    # Proporsi employment type 
    st.markdown("## Proportion of Employment Type") 
    col1, col2 = st.columns(2)
    with col1:
        df_location['employment_type'].replace(['FT','PT','CT','FL'],["Full Time","Part Time","Contract","Freelance"],inplace=True)
        employment_counts = df_location['employment_type'].value_counts()
        
        # st.markdown("Frequency of Experience Level")
        top_5 = df_location['employment_type'].value_counts().reset_index().head(5)
        fig_bar = px.bar(data_frame=top_5, x='index', y='employment_type', title='Frequency of Employment Type',
                        color='employment_type', color_discrete_sequence= px.colors.sequential.Plasma_r)
        fig_bar.update_layout(xaxis={'title': 'employment_type'}, yaxis={'title': 'Frequency'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # st.markdown("Proportion of Experience Level")
        fig_pie = px.pie(names=employment_counts.index, values=employment_counts.values,
                        title='Proportion of Employment Type')
        st.plotly_chart(fig_pie, use_container_width=True)

    # Proporsi Remote ratio  
    st.markdown("## Proportion of Remote Ratio")
    col1, col2 = st.columns(2)
    with col1:
        df_location['remote_ratio'].replace([100, 50, 0],["WFH","Hybrid","WFO"],inplace=True)
        ratio = df_location['remote_ratio'].value_counts()
        
        # st.markdown("Frequency of Experience Level")
        top_5 = df_location['remote_ratio'].value_counts().reset_index().head(5)
        fig_bar = px.bar(data_frame=top_5, x='index', y='remote_ratio', title='Frequency of Remote Ratio',
                        color='remote_ratio', color_discrete_sequence= px.colors.sequential.Plasma_r)
        fig_bar.update_layout(xaxis={'title': 'remote_ratio'}, yaxis={'title': 'Frequency'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # st.markdown("Proportion of Experience Level")
        fig_pie = px.pie(names=ratio.index, values=ratio.values,
                        title='Proportion of Remote Ratio')
        st.plotly_chart(fig_pie, use_container_width=True)

    # # Menghitung frekuensi setiap tingkat pengalaman (experience_level)
    # fig_col1, fig_col2 = st.columns(2)
    # with fig_col1:
    #     st.markdown("Frequency of Experience Level")
    #     df['experience_level'].replace(['SE','MI','EN','EX'],["Senior-level / Expert","Mid-level / Intermediate","Entry-level / Junior","Executive-level / Director"],inplace=True)
    #     experience_counts = df['experience_level'].value_counts()

    #     top_5 = df_selection['experience_level'].value_counts().reset_index()
    #     fig2 = px.bar(data_frame=top_5, x='index', y='experience_level', title='Chart of Top 5 Job Titles', color = top_5['experience_level'], color_continuous_scale='Sunset')

    #     fig2.update_layout(
    #         xaxis={'title': 'Experience Level'},
    #         yaxis={'title': 'Frequency'}
    #     )
    # st.plotly_chart(fig2)
        
    #     # bar_chart = px.bar(x=experience_counts.index,
    #     #            y=experience_counts.values,
    #     #            title='Proportion of Experience Level')
    #     # bar_chart.update_layout(xaxis_title='Experience Level',
    #     #                 yaxis_title='Count')
    #     # st.plotly_chart(bar_chart)
    # with fig_col2:
    #     pie_chart = px.pie(names=experience_counts.index,
    #                     values=experience_counts.values,
    #                     title='Proportion of Experience Level')
    #     st.plotly_chart(pie_chart)

    # st.markdown("## Proportion of Remote Ratio")
    # df['remote_ratio'].replace([100, 50, 0],["WFH","Hybrid","WFO"],inplace=True)

    # remote_counts = df['remote_ratio'].value_counts()
    # pie_chart = px.pie(df,
    #                    title = 'Proportion of Remote Ratio',
    #                    values = remote_counts.values,
    #                    names = remote_counts.index)
    
    # st.plotly_chart(pie_chart)



# Menambah info pada side bar
st.sidebar.markdown("[Data Source](https://www.kaggle.com/datasets/arnabchaki/data-science-salaries-2023)")
st.sidebar.info("Code by [Izzi](https://twitter.com/kemalizzi213) &  [Izza](https://twitter.com/kemalizzi213)")
st.sidebar.info("Self Exploratory Visualization on Data Science Salaries 2023 - Brought To you By [Izzi](https://www.instagram.com/_kemalizzi/) & [Izza](https://www.instagram.com/izzaryu/)  ")
st.sidebar.text("Built with  ❤️ Streamlit by Kemal")