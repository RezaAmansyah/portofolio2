import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st
import os 


#load Dataset pandas 
df = pd.read_csv("Games of the Future 2024 - BoxMatch.csv")

#===============================MOST PICK HERO==================================

pick_hero = pd.crosstab(
    index=df['Pick'],
    columns=df['Win'],
    values=df['Win'],
    aggfunc='count'
).reset_index()
pick_hero = pick_hero.fillna(0)
pick_hero['Total Pick'] = pick_hero['Lose'] + pick_hero['Win']
pick_hero = pick_hero.sort_values(by='Total Pick',ascending=False)

pick_hero['win rate'] = round(pick_hero['Win'] / pick_hero['Total Pick'] * 100,2) 
pick_hero['efectivity'] = pick_hero['Win'] - pick_hero['Lose']
pick_hero = pick_hero[['Pick','Win','Lose','Total Pick','efectivity','win rate']]

#berdasarkan Total Pick
# >= 20 High-Recomended  : 3
# >= 10 - <20 Medium-Recomended : 2
# <10 Low-Recomended : 1

def rec_hero(x):
    '''berdasarkan frekuensi pick hero'''
    if x >= 20:
        value = 4
    elif x < 20 and x >= 15 :
        value = 3
    elif x < 15 and x > 5:
        value = 2
    else :
        value = 1
    return value

#berdasakan wirate
# >= 75% High-Recomended
# >= 50% Medium recomended
# >= 25% Low Medium Recomended
# < 5% very low recomended

def rec_hero_wr(x):
    '''berdasarkan winrate hero'''
    if x >= 75:
        value = 4
    elif x < 75 and x >= 50:
        value = 3
    elif x < 50 and x >= 25 :
        value = 2
    else:
        value = 1
    return value  



def eff_hero(x):
    '''berdasarkan efektivitas'''
    if x > 0:
        value = 3
    elif x == 0:
        value = 2
    else :
        value = 1
    return value


#segmen satu >=9
#segmen dua <= 8 and >=6
#segmen dua <= 5 and <=3

def recomendation(x):
    if x >=9 :
        value = 'S'
    elif x >=6 and x <=8 :
        value = 'A'
    else :
        value = 'B'
    return value 

pick_hero['freq_hero'] = pick_hero['Total Pick'].apply(rec_hero)
pick_hero['win_hero'] = pick_hero['win rate'].apply(rec_hero_wr)
pick_hero['eff_hero'] = pick_hero['efectivity'].apply(eff_hero)
pick_hero['segmen'] = pick_hero['freq_hero'] + pick_hero['win_hero'] + pick_hero['eff_hero']
pick_hero['Tier Hero'] = pick_hero['segmen'].apply(recomendation)

#view dataframe
# pick_hero

#------------------------------Final Chapter-------------------------------------------
#======================================MOST BANNED HERO===============================

ban_hero = pd.crosstab(
    index=df['Ban'],
    columns=df['Win'],
    values=df['Win'],
    aggfunc='count'
).reset_index()
ban_hero = ban_hero.fillna(0)
ban_hero['Total Ban'] = ban_hero['Lose'] + ban_hero['Win']
ban_hero = ban_hero.sort_values(by='Total Ban',ascending=False)

ban_hero['win rate ban'] = round(ban_hero['Win'] / ban_hero['Total Ban'] * 100,2) 

ban_hero = ban_hero[['Ban','Win','Lose','Total Ban','win rate ban']]
ban_hero['efectivity'] = ban_hero['Win'] - ban_hero['Lose']

ban_hero['Ban'] = ban_hero['Ban'].apply(lambda x : x.lower())



#====================================PICKED HERO BY TEAM==============================
df['Team'] = df['Team'].apply(lambda x : x.lower().strip())
most_pick = df.groupby(['Team','Pick']).agg({
    'Pick' : 'count'
}).rename(columns={'Pick':'Total'}).reset_index().sort_values(by=['Team','Total'],ascending=[True,False])

#===========================================================================================

#================================TEAM STATISTIC WIN RATE=============================

team_stat = pd.crosstab(
    index=df['Team'],
    columns=df['Win'],
    values=df['Win'],
    aggfunc='count'
).reset_index()

team_stat = team_stat.fillna(0)
team_stat['Lose'] = team_stat['Lose'] / 5
team_stat['Win'] = team_stat['Win'] / 5

team_stat['Total Match'] = team_stat['Lose'] + team_stat['Win']

team_stat['win_rate'] = round(team_stat['Win'] / team_stat['Total Match'] * 100,2)

team_stat = team_stat.sort_values(by=['Total Match','win_rate'],ascending=False)
team_stat['Team'] = team_stat['Team'].apply(lambda x : x.lower().strip())
#view dataframe
# team_stat

#------------------------------------FInall Chapter------------------------------

#=====================================STATISTIC PLAYERS===============================

potensial_player = df.groupby(['Players','Team']).agg({
    'MVP' : 'sum',
    'Win' : 'count'
}).reset_index().rename(columns={'Win': 'Total Macth'}).sort_values(by=['MVP'],ascending=False)

potensial_player = potensial_player[potensial_player['MVP'] > 0]
potensial_player['win rate'] = round(potensial_player['MVP'] / potensial_player['Total Macth']*100,2)
potensial_player['Players'] = potensial_player['Players'].apply(lambda x : x.lower())











#=====================================BUILD STREAMLIT==================================

# Judul dengan gaya kustom menggunakan Markdown
st.markdown("<h1 style='text-align: center;'>ANALYSIS GAME OF FUTURE MOBILE LEGEND</h1>", unsafe_allow_html=True)


# show all team
image_urls = ['BG.png', 'BREN2.png', 'BLACKLIST.png', 'BURN.png',
    'DEUS VULT.png', 'FF.png', 'HOMEBOIS.png', 'KEEP BEST GAMING.png',
    'NIGHTMARE.png', 'ONIC ID.png', 'RCC.png', 'RRQ HOSHI.png',
    'S2G.png', 'TEAM FLASH.png', 'TEAM LILGUN.png', 'TWISTED.png'
]

# Mengatur tata letak dalam grid 4x4
row1, row2, row3, row4 = st.columns(4)

# # Menampilkan gambar dalam grid
with row1:
    st.image(image_urls[0], caption='BURMESE GHOULS',width=200, use_column_width=True)
    st.image(image_urls[1], caption='APBREN',width=200, use_column_width=True)
    st.image(image_urls[2], caption='BLACKLIST',width=200, use_column_width=True)
    st.image(image_urls[3], caption='BURN X FLASH',width=200, use_column_width=True)

with row2:
    st.image(image_urls[4], caption='DEUS VULT',width=200, use_column_width=True)
    st.image(image_urls[5], caption='FF',width=200, use_column_width=True)
    st.image(image_urls[6], caption='HOMEBOIS',width=200, use_column_width=True)
    st.image(image_urls[7], caption='KEEP BEST GAMING',width=200, use_column_width=True)

with row3:
    st.image(image_urls[8], caption='NIGTMARE',width=200, use_column_width=True)
    st.image(image_urls[9], caption='ONIC ID',width=200, use_column_width=True)
    st.image(image_urls[10], caption='RCC',width=200, use_column_width=True)
    st.image(image_urls[11], caption='RRQ HOSHI',width=200, use_column_width=True)

with row4:
    st.image(image_urls[12], caption='S2G',width=200, use_column_width=True)
    st.image(image_urls[13], caption='TEAM FLASH',width=200, use_column_width=True)
    st.image(image_urls[14], caption='TEAM LILGUN',width=200, use_column_width=True)
    st.image(image_urls[15], caption='TWISTED',width=200, use_column_width=True)






#------------------------------------------------------------------------------------------------------------------
#===========================================STATISTICAL TEAM==========================================
st.title('STATISTIC TEAM')

nama_tim = []
for i in team_stat['Team']:
    nama_tim.append(i)

team_name = pd.DataFrame(nama_tim, columns=['Team Name'])
st.write(team_name)
# st.write(team_stat)   non aktifkan sementara


#tex input untuk team
team = st.text_input('Name of Team (all): ',value='').lower()

#membuat fungsi get data
def get_data(x): 
    for name in team_stat['Team']:
        if x == name:
            tim = team_stat[team_stat['Team'] == x]
            return tim
        elif x == 'all':
            return team_stat
    return None

if st.button('Get Data'):
    result = get_data(team)
    #run the function
    if result is not None:
        st.write(result)
    else:
        st.write('Data Tidak Ditemukan')


#================================================STATISTIC PLAYER==============================================


st.title('STATISTIC PLAYERS')

name_players = []
for i in potensial_player['Players']:
    name_players.append(i)

player_dataframe = pd.DataFrame(name_players,columns=['Player Names'])
st.write(player_dataframe)


#text input player 

input_player = st.text_input('Player Names: (all)' ,value='')

def get_player_name(x):
    for name in potensial_player['Players']:
        if x == name:
            pp = potensial_player[potensial_player['Players'] == x]
            return pp
        elif x == 'all':
            return potensial_player
        
    return None

if st.button('Get Stat Playes'):
    players = get_player_name(input_player)
    if players is not None:
        st.write(players)
    else:
        st.write('Data is not found')


#--------------------------------------------------------------------------------------------------------------
#==============================================MOST PICK HERO================================================
st.title('MOST PICK HERO')
# st.write(pick_hero)   NONAKTIFKAN SEMENTARA


#text input untuk hero 
hero = st.text_input('Pick Tier (S/A/B/all): ',value='').upper()



#membuat fungsi get tier

def get_tier(x):
    for tier in pick_hero['Tier Hero']:

        if x == tier:
            most = pick_hero[pick_hero['Tier Hero'] == x]
            return most
        elif x == 'ALL':
            return pick_hero
    return None

if st.button('Get Tier Hero'):
    result = get_tier(hero)
    #run The Function 
    if result is not None:
        st.write(result)
    else:
        st.write('Data Tidak Di Temukan')
#==============================================MOST BANNED HERO=======================================
st.title('MOST BANNED HERO')

name_banned_hero = []

for i in ban_hero['Ban']:
    name_banned_hero.append(i)
list_banned = pd.DataFrame(name_banned_hero, columns=['Banned Hero'])

st.write(list_banned)

hero_ban = st.text_input('Hero Name: ',value='').lower()

def get_name_ban_hero(x):
    for name in ban_hero['Ban']:
        if x == name:
            banned = ban_hero[ban_hero['Ban'] == x]
            return banned
    return None

if st.button('Get Banned Hero'):
    result = get_name_ban_hero(hero_ban)

    if result is not None:
        st.write(result)
    else:
        st.write('Data Tidak Di Temukan')


#==============================================MOST PICK HERO BY TEAM================================================

st.title('HERO PICKED BY TEAM')


#text input hero per team
team_hero = st.text_input('Chose ur Team: ',value='').lower()

def find_most_pick_hero(x):
    if x == team_hero:
        return most_pick[most_pick['Team'] == x][:5].reset_index(drop=True)
    elif x == 'all':
        st.write(most_pick)  #bermasalah 
    else:
        return None



if st.button('Get Team Hero'):
    result = find_most_pick_hero(team_hero)

    if result is not None:
        st.write(result)
    else:
        st.write('Data Tidak Di temukan')


# ===========================================SELECT BOX VISUALISASI=========================================
st.title('VISUALISATION')

option = [
    'Win Rate Hero', 'Efektivitas Hero', 'Tier Hero','Players MVP', 'Players WR',
    'Total Picked Hero', 'Total Match Team', 'Win Rate Team',
    'Total Banned Hero','Efectivity Banned Hero', 'Win Rate Ban']

pilihan = st.selectbox('Pilih Grafik', option)

if pilihan == 'Win Rate Hero':
    # st.subheader('win rate')
    if st.button('Get Graph'):
        imaage_path = os.path.join(os.getcwd(),'vis win rate hero.png')
        st.image(imaage_path,use_column_width=True)
elif pilihan == 'Efektivitas Hero':
    # st.subheader('efectivity')
    if st.button('Get Graph'):
        image_path = os.path.join(os.getcwd(),'vis efectivity hero.png')
        st.image(image_path,use_column_width=True)
elif pilihan == 'Tier Hero':
    # st.subheader('tier')
    if st.button('Get Graph'):
        image_path = os.path.join(os.getcwd(),'vis tier distribution.png')
        st.image(image_path,use_column_width=True)
elif pilihan == 'Players MVP':
    if st.button('Get Graph'):
        image_path = os.path.join(os.getcwd(),'vis best player mvp.png')
        st.image(image_path,use_column_width=True)
elif pilihan == 'Players WR' :
    if st.button('Get Graph'):
        image_path = os.path.join(os.getcwd(),'vis best player wr.png')
        st.image(image_path,use_column_width=True)
elif pilihan == 'Total Picked Hero':
    if st.button('Get Graph'):
        image_path = os.path.join(os.getcwd(),'vis total pick hero.png')
        st.image(image_path,use_column_width=True)
elif pilihan == 'Total Match Team':
    if st.button('Get Graph'):
        image_path = os.path.join(os.getcwd(),'vis match tim.png')
        st.image(image_path, use_column_width=True)
elif pilihan == 'Win Rate Team':
    if st.button('Get Graph'):
        image_path = os.path.join(os.getcwd(),'vis team wr.png')
        st.image(image_path,use_column_width=True)    
elif pilihan == 'Total Banned Hero':
    if st.button('Get Graph'):
        image_path = os.path.join(os.getcwd(),'vis total ban hero.png')
        st.image(image_path, use_column_width=True)
elif pilihan == 'Efectivity Banned Hero':
    if st.button('Get Graph'):
        image_path = os.path.join(os.getcwd(),'vis efectivity baned hero.png')
        st.image(image_path, use_column_width=True)
elif pilihan == 'Win Rate Ban':
    if st.button('Get Graph'):
        image_path = os.path.join(os.getcwd(),'vis banned hero wr.png')
        st.image(image_path,use_column_width=True)

#---------------------------------------------------------------------------------------------------------------------
#====================================VISUALISASI TOTAL HERO DI PICK==========================================

def annotate_bars(ax):
    '''fungsi untuk memberikan anotasi pada bar'''
    for bar in ax.patches:
        x, y = bar.get_xy()
        ax.text(
            x + bar.get_width(), y + bar.get_height()/2, f'{bar.get_width():.0f} ',
            va='center', ha='right', color='white'
        )
    return ax
# st.title('Visualisasi Total Pick Hero By Tier')

# # Membuat plot menggunakan Seaborn
# fig, ax = plt.subplots(figsize=(12, 8))
# ax = sns.countplot(data=pick_hero, y='Tier Hero', hue='Tier Hero', palette='viridis')
# ax.set_title('Total Pick Hero By Tier')

# # Menambahkan anotasi pada bar
# annotate_bars(ax)
# # Menampilkan plot menggunakan Streamlit
# st.pyplot(fig)






