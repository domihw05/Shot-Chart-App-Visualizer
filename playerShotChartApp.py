#import modules and packages
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import streamlit as st
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
import matplotlib.font_manager as font_manager
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



def json_to_df(data):
    minute = []
    player = []
    h_a = []
    situation = []
    season = []
    shotType = []
    match_id = []
    h_team = []
    a_team = []
    h_goals = []
    a_goals = []
    player_assisted = []
    lastAction = []
    x = []
    y = []
    xg = []
    result = []

    for idx in range(len(data)):
        for key in data[idx]:
            if key == 'X':
                x.append(data[idx][key])
            if key == 'Y':
                y.append(data[idx][key])
            if key == 'xG':
                xg.append(data[idx][key])
            if key == 'result':
                result.append(data[idx][key])
            if key == 'shotType':
                shotType.append(data[idx][key])
            if key == 'minute':
                minute.append(data[idx][key])
            if key == 'player':
                player.append(data[idx][key])
            if key == 'h_a':
                h_a.append(data[idx][key])
            if key == 'situation':
                situation.append(data[idx][key])
            if key == 'season':
                season.append(data[idx][key])
            if key == 'match id':
                match_id.append(data[idx][key])
            if key == 'h_team':
                h_team.append(data[idx][key])
            if key == 'a_team':
                a_team.append(data[idx][key])
            if key == 'h_goals':
                h_goals.append(data[idx][key])
            if key == 'a_goals':
                a_goals.append(data[idx][key])
            if key == 'player_assisted':
                player_assisted.append(data[idx][key])
            if key == 'lastAction':
                lastAction.append(data[idx][key])

    col_names = ['minute','result','x','y','xg','player','h_a','situation',
                 'season','shotType','match_id','h_team','a_team','h_goals',
                 'a_goals', 'player_assisted', 'lastAction']
    df = pd.DataFrame([minute,result, x,y,xg,player,h_a,situation,
                       season,shotType,match_id,h_team, a_team,h_goals, 
                       a_goals, player_assisted, lastAction],index = col_names)
    df = df.T
    df = df.astype({'x':float,'y':float,'xg':float})

    return df

def parse_data():
    # scrape single game shots
    base_url = 'https://understat.com/player/'

    player_id = player_entry.get()
    season = season_menu.get()

    if not player_id:
        messagebox.showerror("Error","Please enter a valid Player ID")
        return

    #id = str(input(f'Please enter the Understat Player ID: '))
    url = base_url + str(player_id)

    res = requests.get(url)
    soup = BeautifulSoup(res.content,'lxml')

    # find scripts to find shots data (INSPECT)

    scripts = soup.find_all('script')

    # get only shots data

    strings = scripts[3].string #PLAYER

    # strip symbols so we only have the json data

    ind_start = strings.index("('")+2
    ind_end = strings.index("')")

    json_data = strings[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')

    # convert string to json format

    data = json.loads(json_data)  

    
    df = json_to_df(data)

    if season == "All":
        return df
    else:
        df_new = df[df["season"] == season]
        if df_new.empty:
            messagebox.showerror("Error","No data found for this season.")
            return None
        return df_new


def print_shot_map():
    df = parse_data()
    season = season_menu.get()

    if df is None:
        messagebox.showerror("Error","No data found for this player.")
    else:
        # Scale x and y coordinates properly
        df['x'] = df['x'] * 100
        df['y'] = df['y'] * 100

        player_name = df['player'].iloc[0]

        # Black color
        background_color = '#0C0D0E'

        font_path = 'Fonts/Poppins/Poppins-Medium.ttf'
        font_props = font_manager.FontProperties(fname=font_path)

        fig = plt.figure(figsize=(8,12))
        fig.patch.set_facecolor(background_color)

        ax1 = fig.add_axes([0,.735,1,.2]) # left, bottom, width, height
        ax1.set_facecolor(background_color)
        ax1.set_xlim(0,1)
        ax1.set_ylim(0,1)


        # PLAYER NAME TITLE
        ax1.text(
            x=0.5,
            y=0.9,
            s=player_name,
            fontsize = 25,
            fontproperties = font_props,
            fontweight = 'bold',
            color = 'white',
            ha = 'center'
        )

        # SUB HEADINGS
        ax1.text(
            x=0.5,
            y=0.75,
            s=f'Career Shot Chart' if season == "All" else f'{season} Shot Chart',
            fontsize = 16,
            fontproperties = font_props,
            fontweight = 'bold',
            color = 'white',
            ha = 'center'
        )

        ax1.text(
            x=0.25,
            y=0.5,
            s=f'Low Quality Chance',
            fontsize = 12,
            fontproperties = font_props,
            fontweight = 'bold',
            color = 'white',
            ha = 'center'
        )

        ax1.scatter(
            x = 0.37,
            y = 0.53,
            s = 100,
            color = background_color,
            edgecolor = 'white',
            linewidth = 0.8
        )

        ax1.scatter(
            x = 0.42,
            y = 0.53,
            s = 200,
            color = background_color,
            edgecolor = 'white',
            linewidth = 0.8
        )
        ax1.scatter(
            x = 0.48,
            y = 0.53,
            s = 300,
            color = background_color,
            edgecolor = 'white',
            linewidth = 0.8
        )
        ax1.scatter(
            x = 0.54,
            y = 0.53,
            s = 400,
            color = background_color,
            edgecolor = 'white',
            linewidth = 0.8
        )
        ax1.scatter(
            x = 0.6,
            y = 0.53,
            s = 500,
            color = background_color,
            edgecolor = 'white',
            linewidth = 0.8
        )

        ax1.text(
            x=0.75,
            y=0.5,
            s=f'High Quality Chance',
            fontsize = 12,
            fontproperties = font_props,
            fontweight = 'bold',
            color = 'white',
            ha = 'center'
        )

        # GOAL VS NO GOAL

        ax1.text(
            x=0.45, 
            y=0.27, 
            s=f'Goal', 
            fontsize=10, 
            fontproperties=font_props, 
            color='white', 
            ha='right'
        )
        ax1.scatter(
            x=0.47, 
            y=0.3, 
            s=100, 
            color='Green', 
            edgecolor='white', 
            linewidth=.8,
            alpha=.7
        )


        ax1.scatter(
            x=0.53, 
            y=0.3, 
            s=100, 
            color=background_color, 
            edgecolor='white', 
            linewidth=.8
        )

        ax1.text(
            x=0.55, 
            y=0.27, 
            s=f'No Goal', 
            fontsize=10, 
            fontproperties=font_props, 
            color='white', 
            ha='left'
        )

        ax1.set_axis_off()

        # SHOT CHART

        ax2 = fig.add_axes([0.05,.313,.9,.5]) # left, bottom, width, height
        ax2.set_facecolor(background_color)

        pitch = VerticalPitch(
            pitch_type='opta',
            half = True,
            pitch_color = background_color,
            pad_bottom=0.5,
            line_color = 'white',
            linewidth = 0.75,
            axis = True,
            label = True
        )

        pitch.draw(ax = ax2)

        for x in df.to_dict(orient='records'):
            pitch.scatter(
                x['x'],
                x['y'],
                s=300 * x['xg'],
                color = 'green' if x['result'] == 'Goal' else background_color,
                ax = ax2,
                alpha = 0.7,
                linewidth = 0.8,
                edgecolor = 'white'
            )

        ax2.set_axis_off()

        # STATS BELOW SHOT CHART

        total_shots = df.shape[0]
        total_goals = df[df['result'] == 'Goal'].shape[0]
        total_xG = df['xg'].sum()
        xG_per_shot = total_xG / total_shots

        ax3 = fig.add_axes([0,.26,1,.05]) #  left, bottom, width, height
        ax3.set_facecolor(background_color)

        ax3.text(x=0.25,y=0.6,s='Shots',fontsize = 20, fontproperties = font_props,
            fontweight='bold',color='white',ha = 'center')
        
        ax3.text(x = 0.25,y=0.1, s=f"{total_shots}",fontsize=16,
                fontproperties = font_props,color='green',ha='center')

        ax3.text(x=0.42,y=0.6,s='Goals',fontsize = 20, fontproperties = font_props,
                fontweight='bold',color='white',ha = 'center')
        ax3.text(x = 0.42,y=0.1, s=f"{total_goals}",fontsize=16,
                fontproperties = font_props,color='green',ha='center')

        ax3.text(x=0.55,y=0.6,s='xG',fontsize = 20, fontproperties = font_props,
                fontweight='bold',color='white',ha = 'center')
        ax3.text(x = 0.55,y=0.1, s=f"{total_xG:.2f}",fontsize=16,
                fontproperties = font_props,color='green',ha='center')

        ax3.text(x=0.69,y=0.6,s='xG/Shot',fontsize = 20, fontproperties = font_props,
                fontweight='bold',color='white',ha = 'center')
        ax3.text(x = 0.69,y=0.1, s=f"{xG_per_shot:.2f}",fontsize=16,
                fontproperties = font_props,color='green',ha='center')
        
        goals_only = df[df['result'] == 'Goal']
        top_assisters = goals_only['player_assisted'].value_counts().head(5)
        top_assists = top_assisters.tolist()
        top_assisters = top_assisters.index.tolist()

        # TOP ASSISTERS

        ax3.text(x=0.29,y=-0.91,s='Top Assisters',fontsize = 20, fontproperties = font_props,
                fontweight='bold',color='white',ha = 'center')

        for idx in range(5):
            # Only print if valid index
            if idx < len(top_assisters): 
                name = top_assisters[idx]
                assists = top_assists[idx]

                ax3.text(x = 0.16,y=-1.6 - (idx*0.4), s=f"{idx+1}. {name} - {assists:.0f} assists",fontsize=12,
                    fontproperties = font_props,color='white',ha='left')

        ax3.set_axis_off()
        
        # PIE CHART

        ax4 = fig.add_axes([0.605,0.058,0.18,0.18]) # left, bottom, width, height

        home_away = goals_only['h_a'].value_counts()
        labels_ha = ['Home','Away']
        colors = ['green','#36454F']

        ax4.pie(home_away,labels = labels_ha,autopct='%1.1f%%', startangle=90, 
                colors = colors, 
                textprops={'fontproperties': font_props,'color':'white'})
        ax4.set_title("Distribution of Goals", fontproperties=font_props,
                    color = 'white',fontsize = 20)

        ax4.set_axis_off()   

        # PRINT FIGURE IN WINDOW

        fig.set_size_inches(7.5,11.25)
        plt.subplots_adjust(top=0.98)  # Moves everything up by reducing the top margin
        #plt.show(block=False)
        canvas = FigureCanvasTkAgg(fig, master = main_frame)
        #canvas.get_tk_widget().config(width=750,height = 1125)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3,column=0,columnspan=2, stick="snew")
    


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Player Shot Chart Visualization")
    root.geometry("1000x1500") # window size (width x height)
    root.resizable(True,True)

    root.configure(bg="#20392C")



    # Modern Font
    FONT = ("Verdana",17)
    HEADER_FONT = ("Verdana",20,"bold")

    # ------------- SIDEBAR ---------------
    sidebar = tk.Frame(root, width = 250, bg = "#232B2B", padx=10, pady=20)
    sidebar.pack(side="left",fill="y")

    title_label = tk.Label(sidebar,text="Player Analysis", font = HEADER_FONT,
                           fg = "white", bg = "#232B2B")
    title_label.pack(pady=10)


    # --------- Process Player ID ---------
    main_frame = tk.Frame(root, bg="#20392C", padx=20,pady=20)
    main_frame.pack(expand=True,fill="both")

    tk.Label(main_frame,text="Player ID:",font=FONT,fg="white",
             bg="#20392C").grid(row=0,column=0,padx=10,pady=10,sticky="w")
    player_entry = tk.Entry(main_frame, font=FONT)
    player_entry.grid(row = 0,column=1, padx=10,pady=10)

    tk.Label(main_frame, text="Season:",font=FONT,fg="white",
             bg="#20392C").grid(row=1,column=0,padx=10,pady=10,sticky="w")
    season_var = tk.StringVar(value="All")
    poss_seasons = [str(year) for year in range(2000,2025)]
    poss_seasons.append("All")
    season_menu = ttk.Combobox(main_frame, textvariable=season_var, values = poss_seasons)
    season_menu.grid(row=1, column=1, padx=10,pady=10)

    generate_button = ttk.Button(main_frame, text="Generate Visualization", command=print_shot_map)
    generate_button.grid(row=2, column=0, columnspan=2, pady=20)

    root.mainloop()
