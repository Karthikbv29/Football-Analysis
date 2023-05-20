#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install mplsoccer


# In[2]:


pip install statsbombpy


# In[3]:


from statsbombpy import sb


# In[4]:


sb.competitions()


# In[5]:


sb.matches(competition_id=16,season_id=22)


# In[6]:


match=sb.events(match_id=18236)


# In[19]:


match


# In[10]:


match.columns


# In[27]:


match['type'].value_counts()


# In[12]:


from mplsoccer import Pitch
pitch=Pitch(pitch_type='statsbomb')
pitch.draw()


# # Shot Map

# In[15]:


from mplsoccer import VerticalPitch
pitch_shot=VerticalPitch(pitch_type='statsbomb',half=True)
pitch_shot.draw()


# In[153]:


#Retrieve rows that record shots
shots = match[match.type=='Shot']

# Filtering data that record Barca
shots_barca=shots[shots.team == 'Barcelona']

# Column Selection
shots_barca=shots_barca[['team','player','minute','second','location','shot_statsbomb_xg','shot_end_location','shot_outcome']]

#
shots_barca['x']=shots_barca.location.apply(lambda x:x[0])
shots_barca['y']=shots_barca.location.apply(lambda x:x[1])

shots_barca['endx']=shots_barca.shot_end_location.apply(lambda x:x[0])
shots_barca['endy']=shots_barca.shot_end_location.apply(lambda x:x[1])


# In[154]:


goals_barca=shots_barca[shots_barca.shot_outcome=='Goal']
shots_barca=shots_barca[shots_barca.shot_outcome!='Goal']


# In[162]:


#Retrieve rows that record shots
shots = match[match.type=='Shot']

# Filtering data that record Manchester United
shots_mu=shots[shots.team == 'Manchester United']

# Column Selection
shots_mu=shots_mu[['team','player','minute','second','location','shot_statsbomb_xg','shot_end_location','shot_outcome']]

#
shots_mu['x']=shots_mu.location.apply(lambda x:x[0])
shots_mu['y']=shots_mu.location.apply(lambda x:x[1])

shots_mu['endx']=shots_mu.shot_end_location.apply(lambda x:x[0])
shots_mu['endy']=shots_mu.shot_end_location.apply(lambda x:x[1])


# In[163]:


goals_mu=shots_mu[shots_mu.shot_outcome=='Goal']
shots_mu=shots_mu[shots_mu.shot_outcome!='Goal']


# In[166]:


goals_mu


# In[161]:


def goal_map(shots_df,goals_df):
    from mplsoccer import VerticalPitch
    import matplotlib.pyplot as plt

    pitch = VerticalPitch(pitch_type='statsbomb',half=True, goal_type='box',
                     goal_alpha=0.8,pitch_color='#22312b',line_color='#c7d5cc')

    fig, axs = pitch.grid(figheight=10, title_height=0.08, endnote_space=0, axis=False,
                      title_space=0, grid_height=0.82, endnote_height=0.05)

    fig.set_facecolor("#22312b")

    scatter_shots = pitch.scatter(shots_df.x, shots_df.y, s=(shots_df.shot_statsbomb_xg * 900)+100,
                              c='red', edgecolors='black', marker='o', ax=axs['pitch'])

    scatter_goals = pitch.scatter(goals_df.x, goals_df.y, s=(goals_df.shot_statsbomb_xg * 900)+100, 
                               edgecolors='black', marker='football', ax=axs['pitch'])

    lines_goals = pitch.lines(goals_df.x, goals_df.y, goals_df.endx, goals_df.endy, color='red',ax=axs['pitch'])

    pitch.arrows(70,5,100,5,ax=axs['pitch'],color='#c7d5cc')

    axs['endnote'].text(0.85, 0.5, '[Karthik Bhagavatula]', color='#c7d5cc', va='center', ha='center', fontsize=15)
    axs['title'].text(0.5, 0.7, 'The Shot Map of FC Barcelona', color='#c7d5cc', va='center', ha='center', fontsize=30)
    axs['title'].text(0.5, 0.25, 'Whole Game', color='#c7d5cc', va='center', ha='center', fontsize=18)

    return plt.show()


# In[167]:


goal_map(shots_mu,goals_mu)


# In[43]:


match.type.value_counts()


# # Pressure Map

# In[45]:


pressure = match[match.type=='Pressure']
pressure = pressure[['team','player','location']]
pressure = pressure[pressure.team == 'Barcelona']

pressure['x'] = pressure.location.apply(lambda x:x[0])
pressure['y'] = pressure.location.apply(lambda x:x[1])


# In[46]:


pressure


# In[67]:


from scipy.ndimage import gaussian_filter

pitch2=Pitch(pitch_type='statsbomb',line_zorder =2,pitch_color='#22312b',line_color='#efefef')

fig2, axs2 = pitch2.grid(figheight=10, title_height=0.08, endnote_space=0, axis=False,
                      title_space=0, grid_height=0.82, endnote_height=0.05)

fig2.set_facecolor("#22312b")

bin_statistic = pitch2.bin_statistic(pressure.x, pressure.y, statistic='count', bins=(25, 25))

bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'],1)

pcm = pitch2.heatmap(bin_statistic,ax=axs2['pitch'],cmap='hot',edgecolors='#22312b')

cbar = fig2.colorbar(pcm, ax = axs2['pitch'],shrink=0.6)

cbar.outline.set_edgecolor('#efefef')

cbar.ax.yaxis.set_tick_params(color='#efefef')

plt.setp(plt.getp(cbar.ax.axes,'yticklabels'),color = '#efefef')

axs2['endnote'].text(0.8,0.5,'Karthik Bhagavatula',color='#c7d5cc',va='center',ha='center',fontsize=10)

axs2['endnote'].text(0.4,0.95,'Attacking Direction',color='#c7d5cc',va='center',ha='center',fontsize=12)

axs2['endnote'].arrow(0.3,0.6,0.2,0, head_width = 0.2, head_length = 0.025, ec='w',fc='w')

axs2['endnote'].set_xlim(0,1)
axs2['endnote'].set_ylim(0,1)

axs2['title'].text(0.5,0.7,'FC Barcelona\'s Pressure Heat Map',color='#c7d5cc',va='center',ha='center',fontsize=30)

plt.show()


# In[79]:


match['pass_outcome'].value_counts()


# # Passing Map

# In[75]:


passing = match[match.type=='Pass']
passing = passing[['team','player','pass_outcome','pass_goal_assist','location','pass_end_location']]
passing = passing[passing.team == 'Barcelona']

passing['x'] = passing.location.apply(lambda x:x[0])
passing['y'] = passing.location.apply(lambda x:x[1])
passing['endx'] = passing.pass_end_location.apply(lambda x:x[0])
passing['endy'] = passing.pass_end_location.apply(lambda x:x[1])


# In[76]:


assists=passing[passing.pass_goal_assist==True]


# In[130]:


assists


# In[131]:


xavi_passes_ucl2011 = passing[passing.player=='Xavier Hernández Creus']
xavi_passes_ucl2011.head()

iniesta_passes_ucl2011 = passing[passing.player=='Andrés Iniesta Luján']

busquets_passes_ucl2011 = passing[passing.player=='Sergio Busquets i Burgos']

messi_passes_ucl2011 = passing[passing.player=='Lionel Andrés Messi Cuccittini']


# In[82]:


passing['pass_outcome']=passing['pass_outcome'].fillna('Complete')


# In[145]:


# Setup the pitch
def players_passing(df):

    pitch3 = Pitch(pitch_type='statsbomb', pitch_color='#22312b',
               line_color='#c7d5cc')
    fig3,ax3 = plt.subplots(figsize=(20,18))
    fig3.set_facecolor('#22312b')
    ax3.patch.set_facecolor('#22312b')

    pitch3.draw(ax=ax3)

    if 'pass_outcome' in df.columns:
        for index, row in df.iterrows():
            if row['pass_outcome'] == 'Complete':
                plt.plot((row['x'], row['endx']), (row['y'], row['endy']), color='green')
                plt.scatter(row['x'],row['y'], color = 'green')
            if row['pass_outcome'] == 'Incomplete':
                plt.plot((row['x'], row['endx']), (row['y'], row['endy']), color='red')
                plt.scatter(row['x'],row['y'], color = 'red')    
    
    return plt.show()            
            


# In[146]:


players_passing(iniesta_passes_ucl2011)


# In[147]:


players_passing(xavi_passes_ucl2011)


# In[148]:


players_passing(busquets_passes_ucl2011)


# In[149]:


players_passing(messi_passes_ucl2011)


# In[159]:


players_passing(passing)


# In[136]:


xavi_passes_ucl2011.to_csv('xavi_passes_ucl_2011.csv')


# In[137]:


iniesta_passes_ucl2011.to_csv('iniesta_passes_ucl_2011.csv')


# In[138]:


busquets_passes_ucl2011.to_csv('busi_passes_ucl_2011.csv')


# In[139]:


messi_passes_ucl2011.to_csv('messi_passes_ucl_2011.csv')


# In[ ]:




