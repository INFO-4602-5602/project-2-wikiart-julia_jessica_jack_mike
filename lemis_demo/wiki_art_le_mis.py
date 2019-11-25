import numpy as np

from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.les_mis import data
import pandas as pd
from bokeh.models.widgets import Panel, Tabs


## my notes on what's up next
'''
- DONE color by the three groups (pos neut neg)
- weighted sum the occurance
- cooccurance -- filter, positive mean rating, neg mean rating, all
-- the filters, just reduce the dataset so it is either > 0.5 "liked",
< 0.5 "disliked", inbetween "neutral", or all
^^^ for these filters need to modify the max min vals of the alpha, or need to scale
by the minimum as well as the maximum
'''

# Load Dataset
all_data_frame = pd.read_csv('WikiArtClean.csv') # leave for all

# positive only data
pos_data_frame = all_data_frame.loc[all_data_frame['Mean rating'] > 0.5]

# negative only data
neg_data_frame = all_data_frame.loc[all_data_frame['Mean rating'] < -0.5]

# neutral/mixed only data
neut_data_frame = all_data_frame.loc[all_data_frame['Mean rating'] > -0.5]
neut_data_frame = neut_data_frame.loc[neut_data_frame['Mean rating'] < 0.5]

things = all_data_frame.columns[11:].to_list() # list of the twenty emotions
# separate the emotions into groups
pos = ['Gratitude','Happiness','Humility','Love','Optimism','Trust']
neg = ['Anger','Arrogance','Disgust','Fear','Pessimism','Regret','Sadness', 'Shame']
other_mixed = ['Agreeableness','Anticipation','Disagreeableness','Shyness','Surprise','Neutral']

cust_things_list = neg + other_mixed + pos
things = cust_things_list

mat_size = len(things)
xname = []
yname = []
for emot in things:
    xname += [emot]*mat_size
    yname += things

## all above is consistent between tabs 
def gen_data(data_frame_L):
    ########### kind of need to determine if this is the negative data and then shift the center for the alphas to be positive
    OCCUR = 0
    MEANLIKE = 2
    wiki_vals = np.zeros((len(things),len(things),4))
    MLcolors_array = pd.DataFrame('#90A7BC', index=range(len(things)), columns=range(len(things)))
    OCcolors_array = pd.DataFrame('#90A7BC', index=range(len(things)), columns=range(len(things)))
    # process and calculate the cooccurances of emotions
    # note this is done for now based on > 0, rather than weighted
    # or other

    ##emot_max_occur = wiki_vals[:,:,OCCUR].max(0) # need this to be per column
    for row in range(len(things)):
        for col in range(len(things)):
            if col >= row:
                temp = data_frame_L[(data_frame_L[things[row]]>0) & (data_frame_L[things[col]]>0)]
                occurance = len(temp['Mean rating']) # count

                norm_count = len(data_frame_L[(data_frame_L[things[row]]>0)])
                weighted_occ = 2.5/norm_count*(data_frame_L[things[row]].to_numpy()@data_frame_L[things[col]].to_numpy())
                
                mean_like = temp['Mean rating'].mean() # average agreeableness
                
                wiki_vals[row, col, OCCUR] = occurance
    ##            wiki_vals[row, col, OCCUR] = weighted_occ
                wiki_vals[row, col, MEANLIKE] = mean_like

    Single_ramp = True # color scheme
    ## !! this is where the max occur might need to change to be per column
    max_occur = wiki_vals[:,:,OCCUR].max()
    print(max_occur)
    max_mean_like = wiki_vals[:,:,MEANLIKE].max()
    print(max_mean_like)
    for row in range(len(things)):
        for col in range(len(things)):
            if col >= row:
                # alpha vals
                # abs val this?
                wiki_vals[row, col, OCCUR+1] = max(wiki_vals[row, col, OCCUR]/max_occur,0.1)
##                wiki_vals[row, col, OCCUR+1] = max(wiki_vals[row, col, OCCUR],0.1)
                wiki_vals[row, col, MEANLIKE+1] = max(wiki_vals[row, col, MEANLIKE]/max_mean_like,0.1)
##                wiki_vals[row, col, MEANLIKE+1] = max(wiki_vals[row, col, MEANLIKE],0.1)

                
                if Single_ramp: # colors in single ramp
                    MLcolors_array.iloc[row, col] = '#a6cee3'
                    MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
                    OCcolors_array.iloc[row, col] = '#a6cee3'
                    OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
                else: # colors by group
                    if (things[row] in pos) and (things[col] in pos):
                        MLcolors_array.iloc[row, col] = '#4daf4a'
                        MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
                        OCcolors_array.iloc[row, col] = '#4daf4a'
                        OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
                    elif (things[row] in neg) and (things[col] in neg):
                        MLcolors_array.iloc[row, col] = '#e41a1c'
                        MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
                        OCcolors_array.iloc[row, col] = '#e41a1c'
                        OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
                    elif (things[row] in other_mixed) and (things[col] in other_mixed):
                        MLcolors_array.iloc[row, col] = '#377eb8'
                        MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
                        OCcolors_array.iloc[row, col] = '#377eb8'
                        OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
                    else:
                        MLcolors_array.iloc[row, col] = '#90A7BC'
                        MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
                        OCcolors_array.iloc[row, col] = '#90A7BC'
                        OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror

    # mirror the matrix
    for dim in range(wiki_vals.shape[2]):
        for col in range(len(things)):
    ##        if col > 5: break
            for row in range(len(things)):
    ##            if row > 5: break
                if row != col and row > col:
                        wiki_vals[row,col,dim] = wiki_vals[col,row,dim]

    # occurance
    counts = wiki_vals[:,:,OCCUR].flatten()
    alpha = wiki_vals[:,:,OCCUR+1].flatten()
    color = OCcolors_array.values.flatten()
    ptitle = 'Emotions --- shaded by co-occurance'
    # mean like
##    counts = wiki_vals[:,:,MEANLIKE].flatten()
##    alpha = wiki_vals[:,:,MEANLIKE+1].flatten()
##    color = MLcolors_array.values.flatten()
##    ptitle = 'Emotions --- shaded by mean like' # need to explain these further

    data=dict(
        xname=xname,
        yname=yname,
        colors=color,
        alphas=alpha,
        count=counts,
    )

    return data

# ---------- generate plot for ALL data
p1_data = gen_data(all_data_frame)
p1title = 'Emotions --- shaded by co-occurance -- All data'
# generate the first plot tab
p1 = figure(title=p1title,
           x_axis_location="above", tools="hover,save",
           x_range=list(reversed(things)), y_range=things,
           tooltips = [('names', '@yname, @xname'), ('count', '@count')])
p1.plot_width = 800
p1.plot_height = 800
p1.grid.grid_line_color = None
p1.axis.axis_line_color = None
p1.axis.major_tick_line_color = None
p1.axis.major_label_text_font_size = "10pt"
p1.axis.major_label_standoff = 0
p1.xaxis.major_label_orientation = np.pi/3

p1.rect('xname', 'yname', 0.9, 0.9, source=p1_data,
       color='colors', alpha='alphas', line_color=None,
       hover_line_color='black', hover_color='colors')

tab1 = Panel(child=p1, title="All - Art")

# ---------- generate plot for Positive data
p2_data = gen_data(pos_data_frame)
p2title = 'Emotions --- shaded by co-occurance -- Positive data'
# generate the first plot tab
p2 = figure(title=p2title,
           x_axis_location="above", tools="hover,save",
           x_range=list(reversed(things)), y_range=things,
           tooltips = [('names', '@yname, @xname'), ('count', '@count')])
p2.plot_width = 800
p2.plot_height = 800
p2.grid.grid_line_color = None
p2.axis.axis_line_color = None
p2.axis.major_tick_line_color = None
p2.axis.major_label_text_font_size = "10pt"
p2.axis.major_label_standoff = 0
p2.xaxis.major_label_orientation = np.pi/3

p2.rect('xname', 'yname', 0.9, 0.9, source=p2_data,
       color='colors', alpha='alphas', line_color=None,
       hover_line_color='black', hover_color='colors')

tab2 = Panel(child=p2, title="Positive - Art")
# ---------- generate plot for Neutral/mixed data
p3_data = gen_data(neut_data_frame)
p3title = 'Emotions --- shaded by co-occurance -- Neutral/mixed data'
# generate the first plot tab
p3 = figure(title=p3title,
           x_axis_location="above", tools="hover,save",
           x_range=list(reversed(things)), y_range=things,
           tooltips = [('names', '@yname, @xname'), ('count', '@count')])
p3.plot_width = 800
p3.plot_height = 800
p3.grid.grid_line_color = None
p3.axis.axis_line_color = None
p3.axis.major_tick_line_color = None
p3.axis.major_label_text_font_size = "10pt"
p3.axis.major_label_standoff = 0
p3.xaxis.major_label_orientation = np.pi/3

p3.rect('xname', 'yname', 0.9, 0.9, source=p3_data,
       color='colors', alpha='alphas', line_color=None,
       hover_line_color='black', hover_color='colors')

tab3 = Panel(child=p3, title="Neutral/mixed - Art")
# ---------- generate plot for Negative data
p4_data = gen_data(neg_data_frame)
p4title = 'Emotions --- shaded by co-occurance -- Negative data'
# generate the first plot tab
p4 = figure(title=p4title,
           x_axis_location="above", tools="hover,save",
           x_range=list(reversed(things)), y_range=things,
           tooltips = [('names', '@yname, @xname'), ('count', '@count')])
p4.plot_width = 800
p4.plot_height = 800
p4.grid.grid_line_color = None
p4.axis.axis_line_color = None
p4.axis.major_tick_line_color = None
p4.axis.major_label_text_font_size = "10pt"
p4.axis.major_label_standoff = 0
p4.xaxis.major_label_orientation = np.pi/3

p4.rect('xname', 'yname', 0.9, 0.9, source=p4_data,
       color='colors', alpha='alphas', line_color=None,
       hover_line_color='black', hover_color='colors')

tab4 = Panel(child=p4, title="Negative - Art")

## ---------------------------------
output_file("wiki_artles_mis.html", title="wiki art example")

##show(p) # show the plot



#####
##tabs = Tabs(tabs=[ tab1])
tabs = Tabs(tabs=[ tab1, tab2, tab3, tab4])

show(tabs)

