import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource

# Declare output output output file
output_file("interactive_test.html")

# Load Dataset
data_frame = pd.read_csv('WikiArtClean.csv')

# Grab a few fields from the first 100 paintings as mini test dataset
test_frame = data_frame.iloc[:100,:][['Title','Year','Image URL','Mean rating']]

source = ColumnDataSource(data=dict(
    x=test_frame['Year'],
    y=test_frame['Mean rating'],
    titles=test_frame['Title'],
    imgs=test_frame['Image URL'],
))

TOOLTIPS = """
    <div>
        <div>
            <img
                src="@imgs" height="100" alt="@imgs" width="100"
                style="float: left; margin: 0px 15px 15px 0px;"
                border="2"
            ></img>
        </div>
        <div>
            <span style="font-size: 17px; font-weight: bold;">@titles</span>
        </div>
        <div>
            <span style="font-size: 15px;">Yeet</span>
            <span style="font-size: 10px; color: #696;">($x, $y)</span>
        </div>
    </div>
"""

p = figure(plot_width=1000, plot_height=600, tooltips=TOOLTIPS,
           title="Test graph please ignore")

p.circle('x', 'y', size=20, source=source)

p.xaxis.axis_label = 'Year'
p.yaxis.axis_label = 'Mean Rating'

show(p)
