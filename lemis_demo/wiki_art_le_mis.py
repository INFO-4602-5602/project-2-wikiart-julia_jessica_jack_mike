import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.les_mis import data
import pandas as pd
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import Legend, LegendItem, Title
from bokeh.layouts import column, row

'''
Citations:
This was the initial code example we worked off of: https://docs.bokeh.org/en/latest/docs/gallery/les_mis.html
'''

# Load Dataset
all_data_frame = pd.read_csv('../WikiArtClean.csv') # leave for all

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

Single_color = '#691b9e' # darkish purple

Multi_positive = '#066303' # darkish green
Multi_negative = '#a80002'# darkish red
Multi_neutral = '#1f5f94' # darkish light blue

pos_and_neg = '#4B3903' # red and green blend
pos_and_neut = '#146156' # green and blue blend
neut_and_neg = '#5A3655' # red and blue blend

not_used = '#90A7BC' # light blue gray

## all above is consistent between tabs
def gen_data(data_frame_L, Occurance_Not_Mean_Like):
    OCCUR = 0
    MEANLIKE = 2
    wiki_vals = np.zeros((len(things),len(things),4))
    MLcolors_array = pd.DataFrame('#90A7BC', index=range(len(things)), columns=range(len(things)))
    OCcolors_array = pd.DataFrame('#90A7BC', index=range(len(things)), columns=range(len(things)))
    # process and calculate the cooccurances of emotions
    # note this is done for now based on > 0, rather than weighted
    # or other
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

    Single_ramp = False # color scheme
    row_max_occur = wiki_vals[:,:,OCCUR].max(0) # per column
    row_min_occur = wiki_vals[:,:,OCCUR].min(0)
    row_max_like = wiki_vals[:,:,MEANLIKE].max(0)
    row_min_like = wiki_vals[:,:,MEANLIKE].min(0)
    max_occur = wiki_vals[:,:,OCCUR].max()
    min_occur = wiki_vals[:,:,OCCUR].min()
##    print('max occur: ',max_occur)
##    print('min occur: ',min_occur)
    max_mean_like = wiki_vals[:,:,MEANLIKE].max()
    min_mean_like = wiki_vals[:,:,MEANLIKE].min()
##    print('max like: ',max_mean_like)
##    print('min like: ',min_mean_like)
    for row in range(len(things)):
        for col in range(len(things)):
            if col >= row:
                # alpha values
                # no normalization
##                wiki_vals[row, col, OCCUR+1] = max(wiki_vals[row, col, OCCUR],0.1)
##                wiki_vals[row, col, MEANLIKE+1] = max(wiki_vals[row, col, MEANLIKE],0.1)

                # full matrix normalization
##                wiki_vals[row, col, OCCUR+1] = max((wiki_vals[row, col, OCCUR]+abs(min_occur))/(max_occur-min_occur),0.1)
##                wiki_vals[row, col, MEANLIKE+1] = max((wiki_vals[row, col, MEANLIKE]+abs(min_mean_like))/(max_mean_like-min_mean_like),0.1)

                # by row normalization
                wiki_vals[row, col, OCCUR+1] = max((wiki_vals[row, col, OCCUR]+abs(row_min_occur[col]))/(row_max_occur[col]-row_min_occur[col]),0.1)
                wiki_vals[row, col, MEANLIKE+1] = max((wiki_vals[row, col, MEANLIKE]+abs(min_mean_like))/(max_mean_like-min_mean_like),0.1)

                if row == col: # blank out the diagonal
                    wiki_vals[row, col, OCCUR+1] = 1.0
                    wiki_vals[row, col, MEANLIKE+1] = 1.0


                if Single_ramp: # colors in single ramp
                    MLcolors_array.iloc[row, col] = Single_color
                    MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
                    OCcolors_array.iloc[row, col] = Single_color
                    OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
                else: # colors by group
                    if (things[row] in pos) and (things[col] in pos):
                        MLcolors_array.iloc[row, col] = Multi_positive
                        MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
                        OCcolors_array.iloc[row, col] = Multi_positive
                        OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
                    elif (things[row] in neg) and (things[col] in neg):
                        MLcolors_array.iloc[row, col] = Multi_negative
                        MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
                        OCcolors_array.iloc[row, col] = Multi_negative
                        OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
                    elif (things[row] in other_mixed) and (things[col] in other_mixed):
                        MLcolors_array.iloc[row, col] = Multi_neutral
                        MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
                        OCcolors_array.iloc[row, col] = Multi_neutral
                        OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
##                    elif (things[row] in pos) and (things[col] in neg):
##                        MLcolors_array.iloc[row, col] = pos_and_neg
##                        MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
##                        OCcolors_array.iloc[row, col] = pos_and_neg
##                        OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
##                    elif (things[row] in pos) and (things[col] in other_mixed):
##                        MLcolors_array.iloc[row, col] = pos_and_neut
##                        MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
##                        OCcolors_array.iloc[row, col] = pos_and_neut
##                        OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
##                    elif (things[row] in neg) and (things[col] in other_mixed):
##                        MLcolors_array.iloc[row, col] = neut_and_neg
##                        MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
##                        OCcolors_array.iloc[row, col] = neut_and_neg
##                        OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
                    else:
                        MLcolors_array.iloc[row, col] = not_used
                        MLcolors_array.iloc[col, row] = MLcolors_array.iloc[row, col] # mirror
                        OCcolors_array.iloc[row, col] = not_used
                        OCcolors_array.iloc[col, row] = OCcolors_array.iloc[row, col] # mirror
                if row == col:
                    MLcolors_array.iloc[row, col] = '#F1F1F1'
                    OCcolors_array.iloc[row, col] = '#F1F1F1'

    # mirror the matrix
    for dim in range(wiki_vals.shape[2]):
        for col in range(len(things)):
    ##        if col > 5: break
            for row in range(len(things)):
    ##            if row > 5: break
                if row != col and row > col:
                        wiki_vals[row,col,dim] = wiki_vals[col,row,dim]

    if Occurance_Not_Mean_Like:
        # occurance
        counts = wiki_vals[:,:,OCCUR].flatten()
        alpha = wiki_vals[:,:,OCCUR+1].flatten()
        color = OCcolors_array.values.flatten()
        ptitle = 'Emotions --- shaded by co-occurance'
    else:
        # mean like
        counts = wiki_vals[:,:,MEANLIKE].flatten()
        alpha = wiki_vals[:,:,MEANLIKE+1].flatten()
        color = MLcolors_array.values.flatten()
        ptitle = 'Emotions --- shaded by mean like' # need to explain these further

    data=dict(
        xname=xname,
        yname=yname,
        colors=color,
        alphas=alpha,
        count=counts,
    )

    return data

tabs_not_grid = True
Occurance_Not_Mean_Like = True

names = ["Positive","Neutral","Negative","Combination"," ","Saturation key","High co-occurance","Medium co-occurance","Low co-occurance"]
colors = [Multi_positive,Multi_neutral,Multi_negative,not_used,'#FFFFFF','#FFFFFF','#046301','#498046','#6d806c']

# ---------- generate plot for ALL data
p1_data = gen_data(all_data_frame, Occurance_Not_Mean_Like)

# generate the first plot tab
p1 = figure(x_axis_location="above", tools="hover,save",
           x_range=list(reversed(things)), y_range=things,
           tooltips = [('Co-occurring Emotions', '@yname, @xname'), ('Number of Paintings', '@count')])

p1.add_layout(Title(text="Showing all Art", text_font_style="italic"), 'above')
p1.add_layout(Title(text="Exploring the Relationship Between Emotions and Likeability", text_font_size="12pt"), 'above')

p1.plot_width = 1000
p1.plot_height = 800
p1.grid.grid_line_color = None
p1.axis.axis_line_color = None
p1.axis.major_tick_line_color = None
p1.axis.major_label_text_font_size = "12pt"
p1.axis.major_label_standoff = 0
p1.xaxis.major_label_orientation = np.pi/3
p1.title.text_font_size = '12pt'

legend_items = []
names = ["Positive","Neutral","Negative","Combination"," ","Saturation key","High co-occurance","Medium co-occurance","Low co-occurance"]
colors = [Multi_positive,Multi_neutral,Multi_negative,not_used,'#FFFFFF','#FFFFFF','#046301','#498046','#6d806c']




p1.rect('xname', 'yname', 0.9, 0.9, source=p1_data,
       color='colors', alpha='alphas', line_color=None,
       hover_line_color='black', hover_color='colors')

for i in range(9):
    legend_items += [(names[i],[p1.rect(0,0,width=0,height=0,color=colors[i])])]
p1.add_layout(Legend(items=legend_items),'right')


if tabs_not_grid: tab1 = Panel(child=p1, title="All Art")

# ---------- generate plot for Positive data
p2_data = gen_data(pos_data_frame, Occurance_Not_Mean_Like)

# generate the first plot tab
p2 = figure(x_axis_location="above", tools="hover,save",
           x_range=list(reversed(things)), y_range=things,
           tooltips = [('Co-occurring Emotions', '@yname, @xname'), ('Number of Paintings', '@count')])

p2.add_layout(Title(text="Filtered by only liked Art", text_font_style="italic"), 'above')
p2.add_layout(Title(text="Exploring the Relationship Between Emotions and Likeability", text_font_size="12pt"), 'above')

p2.plot_width = 1000
p2.plot_height = 800
p2.grid.grid_line_color = None
p2.axis.axis_line_color = None
p2.axis.major_tick_line_color = None
p2.axis.major_label_text_font_size = "12pt"
p2.axis.major_label_standoff = 0
p2.xaxis.major_label_orientation = np.pi/3
p2.title.text_font_size = '12pt'



p2.rect('xname', 'yname', 0.9, 0.9, source=p2_data,
       color='colors', alpha='alphas', line_color=None,
       hover_line_color='black', hover_color='colors')

legend_items = []
for i in range(9):
    legend_items += [(names[i],[p2.rect(0,0,width=0,height=0,color=colors[i])])]
p2.add_layout(Legend(items=legend_items),'right')


if tabs_not_grid: tab2 = Panel(child=p2, title="Liked Art")

# ---------- generate plot for Neutral/mixed data
p3_data = gen_data(neut_data_frame, Occurance_Not_Mean_Like)


# generate the first plot tab
p3 = figure(x_axis_location="above", tools="hover,save",
           x_range=list(reversed(things)), y_range=things,
           tooltips = [('Co-occurring Emotions', '@yname, @xname'), ('Number of Paintings', '@count')])

p3.add_layout(Title(text="Filtered by only neutral/mixed Art", text_font_style="italic"), 'above')
p3.add_layout(Title(text="Exploring the Relationship Between Emotions and Likeability", text_font_size="12pt"), 'above')

p3.plot_width = 1000
p3.plot_height = 800
p3.grid.grid_line_color = None
p3.axis.axis_line_color = None
p3.axis.major_tick_line_color = None
p3.axis.major_label_text_font_size = "12pt"
p3.axis.major_label_standoff = 0
p3.xaxis.major_label_orientation = np.pi/3
p3.title.text_font_size = '12pt'

legend_items = []
for i in range(9):
    legend_items += [(names[i],[p3.rect(0,0,width=0,height=0,color=colors[i])])]
p3.add_layout(Legend(items=legend_items),'right')


p3.rect('xname', 'yname', 0.9, 0.9, source=p3_data,
       color='colors', alpha='alphas', line_color=None,
       hover_line_color='black', hover_color='colors')

if tabs_not_grid: tab3 = Panel(child=p3, title="Neutral/Mixed Art")

# ---------- generate plot for Negative data
p4_data = gen_data(neg_data_frame, Occurance_Not_Mean_Like)

# generate the first plot tab
p4 = figure(x_axis_location="above", tools="hover,save",
           x_range=list(reversed(things)), y_range=things,
           tooltips = [('Co-occurring Emotions', '@yname, @xname'), ('Number of Paintings', '@count')])

p4.add_layout(Title(text="Filtered by only disliked Art", text_font_style="italic"), 'above')
p4.add_layout(Title(text="Exploring the Relationship Between Emotions and Likeability", text_font_size="12pt"), 'above')

p4.plot_width = 1000
p4.plot_height = 800
p4.grid.grid_line_color = None
p4.axis.axis_line_color = None
p4.axis.major_tick_line_color = None
p4.axis.major_label_text_font_size = "12pt"
p4.axis.major_label_standoff = 0
p4.xaxis.major_label_orientation = np.pi/3
p4.title.text_font_size = '12pt'

legend_items = []
for i in range(9):
    legend_items += [(names[i],[p4.rect(0,0,width=0,height=0,color=colors[i])])]
p4.add_layout(Legend(items=legend_items),'right')

p4.rect('xname', 'yname', 0.9, 0.9, source=p4_data,
       color='colors', alpha='alphas', line_color=None,
       hover_line_color='black', hover_color='colors')

if tabs_not_grid: tab4 = Panel(child=p4, title="Disliked Art")

## ---------------------------------
output_file("wiki_art_emotions_adjacency.html", title="wiki art project 2 vis")

##show(p) # show the plot

if tabs_not_grid:
    tabs = Tabs(tabs=[ tab1, tab2, tab3, tab4])
    #tabs.add_layout(Legend(items=legend_items),'right')
    show(tabs)
else:
    show(column(row(p1,p3), row(p2,p4)))
