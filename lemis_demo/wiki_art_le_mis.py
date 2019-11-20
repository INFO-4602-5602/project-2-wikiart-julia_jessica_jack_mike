import numpy as np

from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.les_mis import data
import pandas as pd

# Load Dataset
data_frame = pd.read_csv('WikiArtClean.csv')
things = data_frame.columns[11:].to_list()
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


OCCUR = 0
MEANLIKE = 2
wiki_vals = np.zeros((len(things),len(things),4))
# process and calculate the cooccurances of emotions
# note this is done for now based on > 0, rather than weighted
# or other

for row in range(len(things)):
    for col in range(len(things)):
        if col >= row:
            temp = data_frame[(data_frame[things[row]]>0) & (data_frame[things[col]]>0)]
            occurance = len(temp['Mean rating']) # count
            mean_like = temp['Mean rating'].mean() # average agreeableness
            wiki_vals[row, col, OCCUR] = occurance
            wiki_vals[row, col, MEANLIKE] = mean_like


max_occur = wiki_vals[:,:,OCCUR].max()
max_mean_like = wiki_vals[:,:,MEANLIKE].max()
for row in range(len(things)):
    for col in range(len(things)):
        if col >= row:
            wiki_vals[row, col, OCCUR+1] = max(wiki_vals[row, col, OCCUR]/max_occur,0.1)
            wiki_vals[row, col, MEANLIKE+1] = max(wiki_vals[row, col, MEANLIKE]/max_mean_like,0.1)
            
# mirror the matrix
for dim in range(wiki_vals.shape[2]):
    for col in range(len(things)):
##        if col > 5: break
        for row in range(len(things)):
##            if row > 5: break
            if row != col and row > col:
                    wiki_vals[row,col,dim] = wiki_vals[col,row,dim]
                
nodes = data['nodes']
names = [node['name'] for node in sorted(data['nodes'], key=lambda x: x['group'])]

N = len(nodes)
counts = np.zeros((N, N))
for link in data['links']:
    counts[link['source'], link['target']] = link['value']
    counts[link['target'], link['source']] = link['value']

##colormap = ["#444444", "#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99",
##            "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a"]
colormap = ["#444444", "#02007D", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99",
            "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a"]

##xname = []
##yname = []
color = []
alpha = []
for i, node1 in enumerate(nodes):
    for j, node2 in enumerate(nodes):
##        xname.append(node1['name'])
##        yname.append(node2['name'])

        alpha.append(min(counts[i,j]/4.0, 0.9) + 0.1) # based on counts 

        color.append(colormap[1]) # hack
##        if node1['group'] == node2['group']: # applies either lightgray or blue
##            color.append(colormap[node1['group']]) 
##        else:
##            color.append('lightgrey')
            
color = color[0:len(xname)]
alpha = alpha[0:len(xname)]

counts = counts.flatten()
counts = counts[0:len(xname)]

# occurance
counts = wiki_vals[:,:,OCCUR].flatten()
alpha = wiki_vals[:,:,OCCUR+1].flatten()
color = wiki_vals[:,:,OCCUR+2].flatten()
# mean like
##counts = wiki_vals[:,:,MEANLIKE].flatten()
##alpha = wiki_vals[:,:,MEANLIKE+1].flatten()
##color = wiki_vals[:,:,MEANLIKE+2].flatten()

data=dict(
    xname=xname,
    yname=yname,
    colors=color,
    alphas=alpha,
    count=counts,
)

p = figure(title="Les Mis Occurrences",
           x_axis_location="above", tools="hover,save",
           x_range=list(reversed(things)), y_range=things,
           tooltips = [('names', '@yname, @xname'), ('count', '@count')])


p.plot_width = 800
p.plot_height = 800
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = np.pi/3

p.rect('xname', 'yname', 0.9, 0.9, source=data,
       color='colors', alpha='alphas', line_color=None,
       hover_line_color='black', hover_color='colors')

output_file("wiki_artles_mis.html", title="wiki art example")

show(p) # show the plot


