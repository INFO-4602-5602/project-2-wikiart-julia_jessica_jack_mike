import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6
from bokeh.models import Legend
from bokeh.models.widgets import RadioGroup
from bokeh.models.widgets import Panel, Tabs

# Declare output output output file
output_file("scatter.html")

# Load Dataset
data_frame = pd.read_csv('WikiArtClean.csv',encoding='utf_8')

# Grab sub frames for color mapping
style = data_frame['Style']
bodyparts = data_frame['Face or body']

# Generate ColumnDataSource for plots
source = ColumnDataSource(data=dict(
    style=style,
    x=data_frame['Year'],
    y=data_frame['Mean rating'],
    titles=data_frame['Title'],
    artists=data_frame['Artist'],
    bodyparts=data_frame['Face or body'],
    imgs=data_frame['Image URL'],
))

# Custom tooltip to display images on hover
TOOLTIPS = """
<div>
    <div float: left; width: 230px;>
        <div>
            <img
                src="@imgs" height="200" alt="@imgs"
                style="float: left; margin: 15px 15px 15px 15px;"
                border="2"
            ></img>
        </div>
        <div>
            <span style="float: left; margin: 10px 15px 0px 15px; font-size: 17px; width: 200px; font-weight: bold;">@titles</span>
        </div>
        <div>
            <span style="float: left; margin: 10px 15px 0px 15px; font-size: 15px; width: 200px;">Artist: @artists</span>
        </div>
        <div>
            <span style="float: left; margin: 10px 15px 0px 15px; font-size: 15px; width: 200px;">Year: @x</span>
        </div>
    </div>
</div>
"""

# Generate first plot
colors1 = factor_cmap('style', palette=['#68affc','#81ba5f','#41bbc5','#9c3b68','#9c3b68','#691b9e'], factors=style.unique())
#colors1 = ['#68affc','#422838','#41bbc5','#9c3b68','#81ba5f','#691b9e']

p1 = figure(plot_width=1500, plot_height=1000, tooltips=TOOLTIPS,
           title="Test graph please ignore", lod_threshold=None)

p1.circle('x', 'y', size=6, source=source, fill_color=colors1, line_color=colors1, legend=colors1)


p1.xaxis.axis_label = 'Year'
p1.yaxis.axis_label = 'Mean Rating'

p1.yaxis.ticker = [-3,-2,-1,0,1,2,3]
p1.yaxis.major_label_overrides = {   3: 'I like it a lot',
                                    2: 'I like it',
                                    1: 'I like it somewhat',
                                    0: 'I am neutral',
                                    -1: 'I dislike it somewhat',
                                    -2: 'I dislike it',
                                    -3: 'I dislike it a lot',}

p1.min_border_left = 100
p1.min_border_right = 100
p1.min_border_top = 200
p1.min_border_bottom = 200

p1.legend.location = "bottom_left"
p1.title.text_font_size = '20pt'

tab1 = Panel(child=p1, title="style")


# Generate second plot
colors2 = factor_cmap('bodyparts', palette=['#ffc428','#bd0026','#46bdb3'], factors=bodyparts.unique())

p2 = figure(plot_width=1500, plot_height=1000, tooltips=TOOLTIPS,
           title="Test graph please ignore", lod_threshold=None)

p2.circle('x', 'y', size=6, source=source, fill_color=colors2, line_color=colors2, legend=colors2)


p2.xaxis.axis_label = 'Year'
p2.yaxis.axis_label = 'Mean Rating'

p2.yaxis.ticker = [-3,-2,-1,0,1,2,3]
p2.yaxis.major_label_overrides = {   3: 'I like it a lot',
                                    2: 'I like it',
                                    1: 'I like it somewhat',
                                    0: 'I am neutral',
                                    -1: 'I dislike it somewhat',
                                    -2: 'I dislike it',
                                    -3: 'I dislike it a lot',}

p2.min_border_left = 100
p2.min_border_right = 100
p2.min_border_top = 200
p2.min_border_bottom = 200

p2.legend.location = "bottom_left"
p2.title.text_font_size = '20pt'

tab2 = Panel(child=p2, title="bodyparts")

tabs = Tabs(tabs=[ tab1, tab2 ])

show(tabs)
