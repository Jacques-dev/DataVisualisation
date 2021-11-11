# Jacques TELLIER projet

# from enum import auto
from altair.vegalite.v4.schema.core import AutoSizeParams, AutosizeType
from matplotlib import colors
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import streamlit as st
import time
import datetime
import calendar
import altair as alt
import streamlit.components.v1 as components
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from pandas_profiling import ProfileReport
import random

# BACK END FUNCTIONS ----------------------------------------------------------------------------------------------------------------------

def st_log(func):
    def log_func(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time() - start
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        file1 = open("Logs.txt","a")
        file1.write("\nLog (%s): the function `%s` tooks %0.4f seconds" % (current_time, func.__name__, end))
        file1.close()
        return res

    return log_func



def main():

    @st_log
    @st.cache(suppress_st_warning=True, allow_output_mutation=True)
    def loadData(name):
        nlinesfile = 20000000
        nlinesrandomsample = 1000000
        lines2skip = np.random.choice(np.arange(1,nlinesfile+1), (nlinesfile-nlinesrandomsample), replace=False)
        df = pd.read_csv("https://jtellier.fr/DataViz/"+name, low_memory=False, skiprows=lines2skip)

        # DATA TRANSFORMATION ----------------------------------------------------------------------------------------------------------------------
        df["date_mutation"] = pd.DatetimeIndex(df['date_mutation']).month
        df = df.sort_values(by=["date_mutation"])

        def transform(df, column, type):
            try:
                df[column] = df[column].astype(type)
            except ValueError:
                df[column] = df[column].astype(str)
            return df

        def rework(df, reworks):
            for key, value in reworks.items():
                df = transform(df, key, value)
            return df

        reworks = {
            "latitude" : float,
            "longitude" : float,
            "valeur_fonciere" : float, 
            "lot1_surface_carrez" : float, 
            "lot2_surface_carrez" : float, 
            "lot3_surface_carrez" : float, 
            "lot4_surface_carrez" : float, 
            "lot5_surface_carrez" : float, 
            "surface_reelle_bati" : float,
            "nombre_pieces_principales" : float,
            "surface_terrain" : float,
            "lot1_numero" : int,
            "lot2_numero" : int,
            "lot3_numero" : int,
            "lot4_numero" : int,
            "lot5_numero" : int,
        }

        return rework(df, reworks)

    # DATA IMPORTATION -------------------------------------------------------------------------------------------------------------------------

    DF2016 = loadData("full_2016.csv")
    DF2017 = loadData("full_2017.csv")
    DF2018 = loadData("full_2018.csv")
    DF2019 = loadData("full_2019.csv")
    DF2020 = loadData("full_2020.csv")

    # DATA VISUALISATION ------------------------------------------------------------------------------------------------------------------------

    def home():
        st.title("Requesting property values")
        st.subheader('French real estate analysis from 2016 to 2020')

        components.html(
            """
            <div style='font-size: 18px'>
                <br>
                <p>You will be able to find some deep explanations and details of each dataset used for all data visualisations on the <strong>'Check DataSets'</strong> tab.</p>
                <p><strong>'Make your analysis'</strong> is the space you'll need to make your own visualisations based on parameters presets</p>
            </div>
            """
        )

        
    @st_log
    def displayPandasProfiling(file):
        report_file = open(file, 'r', encoding='utf-8')
        page = report_file.read()
        components.html(page, width=1000, height=600, scrolling=True)

    def checkDataSets():
        option = st.sidebar.selectbox('Select the dataset you want',["2016", "2017", "2018", "2019", "2020"])

        if option == "2016":
            displayPandasProfiling("df2016.html")
        if option == "2017":
            displayPandasProfiling("df2017.html")
        if option == "2018":
            displayPandasProfiling("df2018.html")
        if option == "2019":
            displayPandasProfiling("df2019.html")
        if option == "2020":
            displayPandasProfiling("df2020.html")

    # DATA CROSS ANALYSIS -----------------------------------------------------------------------------------------------------------------------

    def selectDF(year):
        if year == "2016":
            return DF2016
        if year == "2017":
            return DF2017
        if year == "2018":
            return DF2018
        if year == "2019":
            return DF2019
        if year == "2020":
            return DF2020
        return

    @st_log
    def plotingYears(typeOfPlot, df1, df2, df1name, df2name):
        COLUMNS = [
            "valeur_fonciere", 
            "lot1_surface_carrez", 
            "lot2_surface_carrez", 
            "lot3_surface_carrez", 
            "lot4_surface_carrez", 
            "lot5_surface_carrez", 
            "surface_reelle_bati",
            "nombre_pieces_principales",
            "surface_terrain"
        ]
        selected_column = st.selectbox('Select the column', COLUMNS)

        df1 = df1.sort_values(by=["date_mutation"])
        df2 = df2.sort_values(by=["date_mutation"])
        
        fig, ax = plt.subplots()

        if typeOfPlot == "difference by transaction":
            data = [df1[selected_column], df2[selected_column]]
            headers = [df1name, df2name]
            df = pd.concat(data, axis=1, keys=headers)

            ax.hist(x=df, label=headers, log = True)
            ax.legend()
            ax.set_xlabel(selected_column)
            ax.set_ylabel("Number of transaction")
            
        if typeOfPlot == "difference by month":
            
            df1 = df1.groupby(["date_mutation"]).sum()
            df2 = df2.groupby(["date_mutation"]).sum()
            X = (1,2,3,4,5,6,7,8,9,10,11,12)

            ax.bar(X, df1[selected_column], color="blue", alpha=0.5, label=df1name)
            ax.bar(X, df2[selected_column], color="red", alpha=0.5, label=df2name)
            ax.legend()
            ax.set_xlabel("months")
            ax.set_ylabel(selected_column+" by transaction")

        if typeOfPlot == "disparity by month":
            ax.scatter(x=df1["date_mutation"], y=df1[selected_column], c="blue", alpha=0.5, label=df1name)
            ax.scatter(x=df2["date_mutation"], y=df2[selected_column], c="red", alpha=0.5, label=df2name)
            ax.legend()
            ax.set_xlabel("months")
            ax.set_ylabel(selected_column+" by transaction")

        if typeOfPlot == "total difference":
            res_df1 = int(df1[selected_column].sum())
            res_df2 = int(df2[selected_column].sum())
            y = np.array([res_df1,res_df2])
            mylabels = [df1name,df2name]

            ax.pie(y,labels = mylabels)
            ax.set_xlabel(selected_column+" total")
            ax.set_ylabel("")

        st.pyplot(fig)

    def selectDFForAnalysis():
        st.subheader('Cross the years around differents aspects')
        listOfDataFrame1 = ["2016", "2017", "2018", "2019", "2020"]

        def changeListOfDF(selected_df):
            listOfDataFrame = ["2016", "2017", "2018", "2019", "2020"]
            listOfDataFrame.remove(selected_df)
            return listOfDataFrame

        selected_df_1 = st.sidebar.selectbox('Select the first DataFrame you want', listOfDataFrame1)
        
        listOfDataFrame2 = changeListOfDF(selected_df_1)

        selected_df_2 = st.sidebar.selectbox('Select the second DataFrame you want',listOfDataFrame2)
        
        selected_df_1, ' & ', selected_df_2

        typeOfPlot = st.radio("", ["difference by transaction", "difference by month", "disparity by month", "total difference"])

        plotingYears(typeOfPlot, selectDF(selected_df_1), selectDF(selected_df_2), selected_df_1, selected_df_2)

    def crossAnalysis():
        
        typeOfAnalyse = st.sidebar.radio("Type of analyse", ["Worth it Areas/Months", "Cross two years"])
        listOfColums = ["Area", "Month", "Map"]
        listOfArea = ["address", "town", "department"]
        listOfYear = ["2016", "2017", "2018", "2019", "2020"]
        listOfSize = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        
        if typeOfAnalyse == "Worth it Areas/Months":

            column = st.sidebar.selectbox("Property transaction by/on :", listOfColums)
            
            if column == "Area":
                st.subheader('Get the area (city to department) wich have the largest number of transactions by year')
                
                year = st.selectbox("Select the year", listOfYear)
                df = selectDF(year)
                slider = st.select_slider("Choose an area size", options=listOfArea)
                sliderOfSize = st.select_slider("Select number of results", options=listOfSize)

                if slider == "address":
                    dfGrouped = df.groupby(["adresse_nom_voie"]).size().reset_index(name='number of transaction')
                    dfGrouped = dfGrouped.nlargest(sliderOfSize, "number of transaction")
                    dfGrouped = dfGrouped.rename(columns={"adresse_nom_voie":'index'}).set_index("index")

                if slider == "town":
                    dfGrouped = df.groupby(["nom_commune"]).size().reset_index(name='number of transaction')
                    dfGrouped = dfGrouped.nlargest(sliderOfSize, "number of transaction")
                    dfGrouped = dfGrouped.rename(columns={"nom_commune":'index'}).set_index("index")

                if slider == "department":
                    dfGrouped = df.groupby(["code_postal"]).size().reset_index(name='number of transaction')
                    dfGrouped = dfGrouped.nlargest(sliderOfSize, "number of transaction")
                    dfGrouped = dfGrouped.rename(columns={"code_postal":'index'}).set_index("index")

                
                st.bar_chart(dfGrouped)
                
            if column == "Month":
                st.subheader('Get average transaction by month each year')
                data = []
                headers = []
                c = "valeur_fonciere"

                checkBox2016 = st.checkbox("2016", True)
                checkBox2017 = st.checkbox("2017", False)
                checkBox2018 = st.checkbox("2018", False)
                checkBox2019 = st.checkbox("2019", False)
                checkBox2020 = st.checkbox("2020", False)

                if checkBox2016:
                    data.append(DF2016[c])
                    headers.append("2016")
                if checkBox2017:
                    data.append(DF2017[c])
                    headers.append("2017")
                if checkBox2018:
                    data.append(DF2018[c])
                    headers.append("2018")
                if checkBox2019:
                    data.append(DF2019[c])
                    headers.append("2019")
                if checkBox2020:
                    data.append(DF2020[c])
                    headers.append("2020")

                df = pd.concat(data, axis=1, keys=headers)
                df["date_mutation"] = DF2020["date_mutation"]

                df = df.sort_values(by=["date_mutation"])
                df = df.groupby(["date_mutation"]).mean()
                
                st.bar_chart(df)

            if column == "Map":
                st.subheader('Get the town(s) wich have the largest number of transactions by year on map')
                selectionOfYear = st.radio("Year", ["2016", "2017", "2018", "2019", "2020"])
                sliderOfSize = st.select_slider("Choose max town", options=listOfSize)
                df = pd.DataFrame()

                if selectionOfYear == "2016":
                    df = DF2016
                if selectionOfYear == "2017":
                    df = DF2017
                if selectionOfYear == "2018":
                    df = DF2018
                if selectionOfYear == "2019":
                    df = DF2019
                if selectionOfYear == "2020":
                    df = DF2020
                
                df = df[df['longitude'].notna()]
                df = df[df['latitude'].notna()]

                df = df.groupby(["nom_commune"]).mean()

                df = df.nlargest(sliderOfSize, "valeur_fonciere")
                df = df.reset_index()

                df["longitude"] = df["longitude"]
                df["latitude"] = df["latitude"]

                st.map(df)

        if typeOfAnalyse == "Cross two years":
            selectDFForAnalysis()  

    # PROGRAM EXECUTION -----------------------------------------------------------------------------------------------------------------------

    page = st.sidebar.radio("Navigation", ["Home", "Check DataSets", "Make your analysis"])
    
    if page == "Home":
        home()

    if page == "Check DataSets":
        checkDataSets()

    if page == "Make your analysis":
        crossAnalysis()
    
    return



if __name__ == "__main__":
    main()