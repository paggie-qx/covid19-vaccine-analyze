from django.shortcuts import render
from django.http import HttpResponse
from plotly.offline import plot
import plotly.express as px 
import pandas as pd
import time


#python notebook CODE
# Read data

    


#VIEWS
def home_views(request,*args, **kwargs):
    information = {
        "name"   : "Paggie Chen",
        "age"    : 21,
        "gender" : "female"
    }
    return render(request,"home.html",information)


def about_views(request,*args, **kwargs):
    # 2-1. 疫苗施打總劑數的地區分佈
    def Region():
        #從WHO官網讀取'WHO-vaccine.csv'資料檔
        data = pd.read_csv('https://covid19.who.int/who-data/vaccination-data.csv')
        # data.to_csv('WHO-vaccine.csv') 
        fig = px.pie(data, names='WHO_REGION', values='TOTAL_VACCINATIONS', title="疫苗施打總劑數的地區分佈")
        plot_div = plot(fig, auto_open = False, output_type="div")
        
        return plot_div
    # 2-2. 全球疫苗施打總劑數排名
    def VacTotal():
        #從WHO官網讀取'WHO-vaccine.csv'資料檔
        data = pd.read_csv('https://covid19.who.int/who-data/vaccination-data.csv')
        # data.to_csv('WHO-vaccine.csv') 
        
        data_sort = data.sort_values(by=['TOTAL_VACCINATIONS'],ascending=False).head(15) 
        
        fig = px.bar(data_sort, y='TOTAL_VACCINATIONS', x='COUNTRY', text='TOTAL_VACCINATIONS', title='全球疫苗施打總劑數排名')
        fig.update_traces(texttemplate='%{text:.2s}', textposition='auto')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        plot_div = plot(fig, auto_open = False, output_type="div")
        
        return plot_div
    
    #2-3. 全球疫苗施打總劑數排名，和其相對應所施打的疫苗種類數量
    def VacType():
        #從WHO官網讀取'WHO-vaccine.csv'資料檔
        data = pd.read_csv('https://covid19.who.int/who-data/vaccination-data.csv')
        # data.to_csv('WHO-vaccine.csv') 
        
        data_sort = data.sort_values(by=['TOTAL_VACCINATIONS'],ascending=False).head(15)

        fig = px.bar(data_sort, y='TOTAL_VACCINATIONS', x='COUNTRY', text='NUMBER_VACCINES_TYPES_USED', color='NUMBER_VACCINES_TYPES_USED', title='全球疫苗施打總劑數排名，和其相對應所施打的疫苗種類數量')
        fig.update_traces(texttemplate='%{text:s}', textposition='auto')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        plot_div = plot(fig, auto_open = False, output_type="div")
        
        return plot_div

    #2-4. 各國完全接種疫苗的累計人數排名
    def fullyVac():
        #從WHO官網讀取'WHO-vaccine.csv'資料檔
        data = pd.read_csv('https://covid19.who.int/who-data/vaccination-data.csv')
        # data.to_csv('WHO-vaccine.csv') 
        data_fully_vac = data.sort_values(by=['PERSONS_FULLY_VACCINATED'],ascending=False).head(15)

        fig = px.bar(data_fully_vac, y='PERSONS_FULLY_VACCINATED', x='COUNTRY', text='PERSONS_FULLY_VACCINATED', title='各國完全接種疫苗的累計人數')
        fig.update_traces(texttemplate='%{text:.2s}', textposition='auto')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        plot_div = plot(fig, auto_open = False, output_type="div")
        
        return plot_div
    
    #2-5. 判斷全球平均接種的疫苗種類數量，和對應的地區
    def VacAvg():
        #從WHO官網讀取'WHO-vaccine.csv'資料檔
        data = pd.read_csv('https://covid19.who.int/who-data/vaccination-data.csv')
        # data.to_csv('WHO-vaccine.csv') 
        fig = px.scatter(data, x='NUMBER_VACCINES_TYPES_USED',y='COUNTRY',color='WHO_REGION',title="判斷全球平均接種的疫苗種類數量，和對應的地區")
        plot_div = plot(fig, auto_open = False, output_type="div")
        
        return plot_div

    context={
        "Region": Region(),
        "VacTotal": VacTotal(),
        "VacType": VacType(),
        "fullyVac": fullyVac(),
        "VacAvg": VacAvg()
    }
    return render(request, "about.html",context)


def Map_views(request,*args, **kwargs):

    def totalDeath():
        #data_death 
        data_death = pd.read_csv('https://covid19.who.int/WHO-COVID-19-global-table-data.csv')

        #由於原始csv檔案中將第一個欄位設為index, 直接叫出來會出錯，因此需要做資料前處理
        data_death.reset_index(inplace=True)                #將檔案回覆到原始狀態，即不會自動將index欄位的column名稱屏蔽
        data_death.rename(columns={"index":"Country",          #欄位重命名
            "Name":'WHO Region',
            "WHO Region":"Cases - cumulative total",
            "Cases - cumulative total":"Cases - cumulative total per 1000000 population",
            "Cases - cumulative total per 1000000 population":"Cases - newly reported in last 7 days",
            "Cases - newly reported in last 7 days": "Cases - newly reported in last 7 days per 1000000 population",
            "Cases - newly reported in last 7 days per 1000000 population":"Cases - newly reported in last 24 hours",
            "Cases - newly reported in last 24 hours": "Deaths - cumulative total",
            "Deaths - cumulative total": "Deaths - cumulative total per 100000 population",
            "Deaths - cumulative total per 100000 population": "Deaths - newly reported in last 7 days",
            "Deaths - newly reported in last 7 days":"Deaths - newly reported in last 7 days per 100000 population",
            "Deaths - newly reported in last 7 days per 100000 population": 'Deaths - newly reported in last 24 hours.'
        },inplace=True)
        data_death = data_death.drop('Deaths - newly reported in last 24 hours',1)  #將最後一個欄位捨棄
        data_death = data_death.replace(['United States of America'],'United States')
        # data_death.to_csv("WHO-death.csv")

        #country代碼，以畫在地圖上
        country_code = pd.read_csv('countries_codes_and_coordinates.csv',usecols=['Country','Alpha-3 code'])
        # country_code.to_csv("country code.csv")

        #將country code和data death合併
        merge_file = pd.merge(data_death,country_code,on='Country')

        fig = px.choropleth(merge_file,
                        locations ='Country', color='Deaths - cumulative total',
                        # animation_frame="Cases - cumulative total",
                        locationmode='country names',
                        color_continuous_scale=px.colors.sequential.solar_r, #colors.diverging.RdBu,
                        projection = "orthographic", #地球呈現方式
                        title="各國新冠疫情死亡人數總計"
                        )

        plot_div = plot(fig, auto_open = False, output_type="div")

        return plot_div
    
    context={
        "totalDeath": totalDeath(),
    }
    return render(request, "map.html",context)