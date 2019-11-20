import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6

# Declare output output output file
output_file("scatter.html")

# Load Dataset
data_frame = pd.read_csv('WikiArtClean.csv')

# Grab a few fields from the first 100 paintings as mini test dataset
# test_frame = data_frame.iloc[:100,:][['Title','Year','Image URL','Mean rating']]
test_frame = data_frame

style = test_frame['Style']

source = ColumnDataSource(data=dict(
    x=test_frame['Year'],
    y=test_frame['Mean rating'],
    style=style,
    titles=test_frame['Title'],
    artists=test_frame['Artist'],
    imgs=test_frame['Image URL'],
))

TOOLTIPS = """
<div>
    <div float: left; width: 230px;>
        <div>
            <img
                src="@imgs" height="200" alt="@imgs" width="200"
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

colors = factor_cmap('style', palette=Spectral6, factors=style.unique())



p = figure(plot_width=1500, plot_height=800, tooltips=TOOLTIPS,
           title="Test graph please ignore", lod_threshold=None)

p.circle('x', 'y', size=6, source=source, fill_color=colors, line_color=colors)

p.xaxis.axis_label = 'Year'
p.yaxis.axis_label = 'Mean Rating'

p.yaxis.ticker = [-3,-2,-1,0,1,2,3]
p.yaxis.major_label_overrides = {   3: 'I like it a lot',
                                    2: 'I like it',
                                    1: 'I like it somewhat',
                                    0: 'I am Neutral',
                                    -1: 'I dislike it somewhat',
                                    -2: 'I dislike it',
                                    -3: 'I dislike it a lot',}

p.min_border_left = 100
p.min_border_right = 100
p.min_border_top = 200
p.min_border_bottom = 200

show(p)
