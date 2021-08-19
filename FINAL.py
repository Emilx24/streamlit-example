import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

# Disclaimer:
# Poltly used instead of mathplotlib, they are basically the same, but plotly is aesthetically superior in my opinion and I use the same skills I applied on HW3

# add your directory for skyscrapers.xlsx here
FILE = 'C:\\Users\\emili\\PycharmProjects\\pythonProject\\FINALPROJECT\\skyscrapers.xlsx'

# USEFUL DATA FRAMES, ONE GENERAL DF, THE OTHER TO COMPARE SIZES (ALL COUNTRIES)
df = pd.read_excel(FILE, usecols=[0, 1, 3, 4, 5, 6])
df_size = pd.read_excel(FILE, usecols=[0, 1, 3, 6])
# DF FOR WORLD POWERS ONLY (CHINA, RUSSIA, USA)
powersDF = df[
    df['Country'].str.contains('United States') | df['Country'].str.contains('China') | df['Country'].str.contains(
        'Russia')]


def newDataFrame(columnType='Country', filterName='China'):
    # filters the data frame by country and creates a separate data frame
    newDF = df[df[columnType].str.contains(filterName)]
    return newDF


def graph(dataFrame=newDataFrame(), ChartType='Pie Chart', columnName='Main use'):
    # counts all of the main use values and makes a dictionary for every use (keys) and the number of buildings that use it (values)
    dictionaryDf = dataFrame[columnName].value_counts().to_dict()
    # converts dictionary to Data Frame again, but cleaner format to use for pie graph
    organizedDF = pd.DataFrame(dictionaryDf.items(), columns=[columnName, 'Buildings'])
    if columnName == 'Main use' or columnName == 'Type':
        title = f'The {columnName} Of Tall Buildings In The Selected Country'
        titleColor = 'Green'
    elif columnName == 'Country':
        title = f'Countries Using The Type Selected'
        titleColor = 'Yellow'
    # Allows the graph to be in either pie or bar chart format
    if ChartType == 'Pie Chart':
        fig = px.pie(organizedDF, names=organizedDF[columnName], values=organizedDF['Buildings'], title=title)
    elif ChartType == 'Bar Chart':
        fig = px.bar(organizedDF, x=organizedDF[columnName], y=organizedDF['Buildings'],
                     color=organizedDF[columnName], title=title)
    fig.update_layout(
        font_color="white",
        title_font_color=titleColor,
        title_font_family="Times New Roman",
        font_family="Courier New",
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
    )
    st.plotly_chart(fig)
    pass


def size_graph(dataFame=df, decadeStart=1970):
    # uses data frame for bar graph (MUST HAVE YEAR, METRES, COUNTRY AND NAME)
    # Gets the decade from the decade start value, 1970, 1971, 1972,...
    yearDF = dataFame[dataFame['Year'].isin(
        [decadeStart, decadeStart + 1, decadeStart + 2, decadeStart + 3, decadeStart + 4, decadeStart + 5,
         decadeStart + 7, decadeStart + 8, decadeStart + 9, decadeStart + 10])]
    # Creates a bar graph that displays years in x axis and metres in y axis
    fig = px.bar(yearDF, x='Year', y=' Metres', color="Country", hover_name="Name",
                 title='Tall Structures Built by Decade')
    fig.update_layout(
        font_color="white",
        title_font_color="Red",
        title_font_family="Cambria",
        font_family="Cambria",
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
    )
    st.plotly_chart(fig)
    pass


def countryChoice(stat1, stat2, stat3):
    # use for selection bar in Chart C
    if stat1 == 'USA':
        return graph(newDataFrame('Country', 'United States'), stat2, stat3)
    elif stat1 == 'RUSSIA':
        return graph(newDataFrame('Country', 'Russia'), stat2, stat3)
    elif stat1 == 'CHINA':
        return graph(newDataFrame(), stat2, stat3)


def chartA():
    # MAKE A LIST OUT OF UNIQUE 'TYPE' VALUES FOR THE LAST PIE CHART SLIDER
    unique_arr = df["Type"].unique()
    typeSlider = st.select_slider("Select type", options=unique_arr)
    graph(newDataFrame('Type', typeSlider), 'Pie Chart', 'Country')
    st.text('Graph A gathers all buildings in the dataset and is filtered by “type” by using the slider below. '
            'The pie chart represents the percentage of countries worldwide that have tall structures of the type selected.')
    pass


def chartB():
    decadeSlider = st.slider("Select the level", min_value=1970, max_value=2020, step=10)
    size_graph(df, decadeSlider)
    st.text('Graph B presents structures built by the decade, starting in 1970 and ending in 2020. '
            'The total number of meters built is shown on the Y axis, the year is shown on the X axis. '
            'The countries shown in the legend can be clicked to filter out the data.')
    pass


def chartC():
    status = st.radio("Select Country: ", ('CHINA', 'RUSSIA', 'USA'))
    status2 = st.selectbox("Select a chart type: ", ('Pie Chart', 'Bar Chart'))
    status3 = st.selectbox("Sort data: ", ('Main use', 'Type'))
    countryChoice(status, status2, status3)
    st.text('Graph C shows data for China, Russia and the US. It shows how many of its total structures found in the dataset are of the main use or type selected. '
            'The data can be changed to bar graph format.  The main use/type shown in the legend can be clicked to filter out the data. ')
    pass


def chartSelect():
    # graph selection for the two chapters so that the user does not have to scroll down while reading to see a chart
    chartLetter = st.selectbox("Select a Graph: ", ('Graph A', 'Graph B', 'Graph C'))
    if chartLetter == 'Graph A':
        return chartA()
    elif chartLetter == 'Graph B':
        return chartB()
    elif chartLetter == 'Graph C':
        return chartC()
    pass


def openImage(img):
    image = Image.open(img)
    return image


titleList = ['Introduction', 'The Opening of China', 'Russia and Post-Soviet States', 'Conclusion']
# creates sidebar
option = st.sidebar.radio('CONTENTS', titleList)

# CHAPTER 1 INTRODUCTION
if option == titleList[0]:
    st.image(openImage('C:\\Users\\emili\\PycharmProjects\\pythonProject\\FINALPROJECT\\skyscrapers.jpg'), caption='Source: Romain Trystram')
    st.title("Skyscrapers and Economies")
    st.header("How data of skyscrapers show a history of economic performance")
    st.write("""
    We can attribute large structures like skyscrapers with economic growth because these buildings are often a result of high 
    levels of investment as they are costly to build and maintain, thus they are either made to build a large profit or have an important purpose. 
    If we analyze when these large structures are built and why they are built, we can determine what the political and economic situation a country is going through in a period of time. 
    Skyscrapers are built for many different reasons, today they are a luxury and a tourist gimmick, but this has not always been the case. Jason Barr’s “The Economics of Skyscraper Height: 
    mentions that “the supertall towers rising in Manhattan during the late 1920s were not “freak” buildings, but rather, were based on reasonable economic foundations”. 
    This page will use a simple set of data from the Wikipedia page, “List of tallest freestanding structures”, to analyze type, use, height and year built to compare 
    and contrast the recent political and economic history of Russia and China, and how they compare with the United States. 
    \n
    \n""")
    st.dataframe(df)
    st.text("“List of tallest freestanding structures” from Wikipedia: https://en.wikipedia.org/wiki/List_of_tallest_freestanding_structures")

# CHAPTER 2 THE OPENING OF CHINA
elif option == titleList[1]:
    st.image(openImage('C:\\Users\\emili\\PycharmProjects\\pythonProject\\FINALPROJECT\\Flag-China.jpg'), caption='Source: Encyclopedia Britannica')
    st.title(titleList[1])
    st.write("""
    From **Graph A**, we can see that China surpasses the United States in the number of tallest skyscrapers worldwide at 38.3%, 
    while the United States comes second at 29.8%. Russia, once known as the key state behind the Soviet Union, stands at 2.12%, with only one 
    skyscraper that was built recently in 2019, as shown in **Graph B**.  As we see in Graph B, China rapidly grew its skyscrapers and other tall structures 
    in the 21st Century, peaking in 2010, building over 2,500 meters in total (it helps to filter out the UAE legend checkbox to see the total meters for year 1990). 
    China’s rise in tall structures did not start until the 1990s, which can be tied to the Chinese economic reform, or also known as the “Opening of China”, 
    which was a result of the Tiananmen Square protests in 1989. In addition, **Graph C** shows the Chinese main use of their structures seems to be more focused on 
    office space and mixed use (mixed use often involves offices, e.g Shanghai World Financial Center).
    \n\n""")
    st.write("""
    Massive urbanization and implementation of office spaces help to demonstrate how the Chinese economy rapidly liberalized to become an 
    economic power that could rival the United States in just a few short years. If we compare charts of the Chinese tallest structures and 
    the United States’ tallest structures, we can find a lot of similarities, which shows the threat China poses to the West in terms of economic dominance, 
    unlike Russia, a country that shows little economic growth since the collapse of the Soviet Union. 
    \n\n""")
    chartSelect()

elif option == titleList[2]:
    st.image(openImage('C:\\Users\\emili\\PycharmProjects\\pythonProject\\FINALPROJECT\\russiamap.jpg'), caption='Source: Encyclopedia Britannica')
    st.title(titleList[2])
    st.write("""
    The United States has 3 of the tallest structures that are industrial chimneys (**Graph A**) , making it the largest number of Chimneys held by an individual country. 
    Russia has just one of the largest Chimneys (Chimney of Berezovskaya GRES), but if we count the other former Soviet states found in the dataset such as Kazakhstan and Uzbekistan, 
    together they tie with the United States with 3 industrial chimneys. It's also important to note that these large chimneys, along with communications and lattice towers were 
    built during Soviet times strictly for government purposes, as **Graph B** shows that former Soviet States (Ukraine, Latvia, Uzbekistan and Kazakhstan) did not build any large 
    freestanding structures that could make it on the list after the 1991 collapse of the Soviet Union (with the exception of Russia’s Lakhta Center recently built in 2019). 
    \n\n""")
    st.write("""
    **Graph C** shows a very limited number of structures “use diversity”, because one is a transmitter, one is a power station and the other is a post-Soviet office. 
    In contrast, the United States in *Graph C* shows a wide diversity of buildings (the pie chart itself has to be expanded to be visible). 
    This is a sign of a large economy with constant investment as most of the building main uses involve making corporate profits instead of government assigned roles 
    (e.g hotels and offices). From both **Graph B and C**, we can observe how shallow the Russian economy truly is compared to China and the United States. 
    Russia may be one of the greatest threats to the United States and NATO in military and geopolitical terms, but it will never have the economic capacity to truly rival 
    the West like it did back in Soviet times. 
    \n\n""")
    chartSelect()

elif option == titleList[3]:
    st.image(openImage('C:\\Users\\emili\\PycharmProjects\\pythonProject\\FINALPROJECT\\skyscrapers.jpg'), caption='Source: Romain Trystram')
    st.title(titleList[3])
    st.write("""
    In conclusion, this simple and vague dataset is capable of showing recent economic and political history of China and Russia and how they compare with the United States. 
    The data provided was able to tell China is the worthy rival to the United States because its economy boomed after its capitalist economic reforms, 
    while Russia and Eastern Europe were never able to grow after the collapse of the USSR, thus making it a threat only militarily.
     Data has a lot of stories to tell, it just needs to be explored and modified to identify patterns.
    \n\n""")
    st.write("""
    **Works Cited**:\n
    Barr, J., The Economics of Skyscraper Height (Part IV): Construction Costs Around the World - Skynomics Blog says: 
    The Economics of Skyscraper Height (Part III) - Skynomics Blog says: The Economics of Skyscraper Height (Part II) - 
    Skynomics Blog says: The Technology of Tall (Part III): Getting to the Core - Skynomics Blog says: O que o espraiamento urbano e a verticalização dizem sobre as emissões de CO2 - 
    La Arc says: &amp; Espraiamento vs. Verticalização: emissões de CO2 em Nova York says: (2019, December 2). The economics of skyscraper Height (Part i) - 
    Skynomics Blog. Building the Skyline. https://buildingtheskyline.org/skyscraper-height-i/.\n 
    Encyclopædia Britannica, inc. (n.d.). Collapse of the Soviet Union. Encyclopædia Britannica. https://www.britannica.com/event/the-collapse-of-the-Soviet-Union.\n 
    Encyclopædia Britannica, inc. (n.d.). Economic policy changes. Encyclopædia Britannica. https://www.britannica.com/place/China/Economic-policy-changes.\n 
    Wikimedia Foundation. (2021, August 16). List of tallest freestanding structures. Wikipedia. https://en.wikipedia.org/wiki/List_of_tallest_freestanding_structures.\n
    **Image Sources**:\n
     https://www.britannica.com/topic/flag-of-China\n
     https://www.britannica.com/place/Russia\n
     https://romaintrystram.myportfolio.com/\n
    \n\n""")
