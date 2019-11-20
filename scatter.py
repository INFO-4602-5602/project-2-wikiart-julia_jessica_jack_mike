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

# Grab a few fields from the first 100 paintings as mini test dataset
# test_frame = data_frame.iloc[:100,:][['Title','Year','Image URL','Mean rating']]
test_frame = data_frame

style = test_frame['Style']
bodyparts = test_frame['Face or body']

source = ColumnDataSource(data=dict(
    style=style,
    x=test_frame['Year'],
    y=test_frame['Mean rating'],
    titles=test_frame['Title'],
    artists=test_frame['Artist'],
    bodyparts=test_frame['Face or body'],
    imgs=test_frame['Image URL'],
))

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

colors1 = factor_cmap('style', palette=Spectral6, factors=style.unique())

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

tab1 = Panel(child=p1, title="style")



colors2 = factor_cmap('bodyparts', palette=Spectral6, factors=bodyparts.unique())

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

tab2 = Panel(child=p2, title="bodyparts")

tabs = Tabs(tabs=[ tab1, tab2 ])

show(tabs)
