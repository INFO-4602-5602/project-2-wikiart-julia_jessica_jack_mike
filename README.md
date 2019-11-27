## README
<h2>How to make a crowd-pleaser: what aspects of artwork make it likeable?</h2>
<br>
<h2>Introduction</h2>
WikiArt Emotions is an ambitious project that aimed to measure how people view and experience art. A subset of WikiArt’s extensive collection was included in this study, where participants were asked to give a variety of responses to quantify their reactions to the artworks, including which of twenty given emotions the pieces evokes, if the piece contains human features, and simply how much they like or dislike it. The result is a rich dataset that contains some potentially provocative insights into how people connect with art and why. <br>

<br>This connection was the central focus of this investigation in which we designed two interactive visualizations to explore how the various aspects of the art correlate with their average likeability. We compare mean rating with time, artistic style and presence of human figures in a scatterplot, and then we designed an adjacency matrix to illustrate how emotions reported may correlate with each other and with likeability.

<br> Below you can find direct links to each of the visualizations:

Title: The Likeability of Art across Time, Style and Subject Matter 
[Scatterplot](https://info-4602-5602.github.io/project-2-wikiart-julia_jessica_jack_mike/scatter.html)

Title: Exploring the Relationship Between Emotions and Likeability 
[Adjacency Matrix](https://info-4602-5602.github.io/project-2-wikiart-julia_jessica_jack_mike/wiki_art_emotions_adjacency.html)

<h2>Team Roles </h2>
Mike: Designer/coder<br>
Brainstormed visualization possibilities.
<br>Wrote code for the emotions adjacency matrix vis.
<br>Iterated data preprocessing from team feedback to find a good combination of storytelling and ensuring vis honesty. 

<br>Jack: Designer/coder<br>
Brainstormed vis ideas.
<br>Wrote code for interactive scatterplot vis.
<br>Managed github.io hosting of vis html.
<br>Helped fix character encoding problems in dataset.

Jess: Designer/writer<br>
Sketched several prototype visualizations.
<br>Modeled several early iterations of the scatterplot Tableau.
<br>Wrote and edited content for Readme.
<br>Gave feedback on iterations of visualizations.
<br>Coded formatting in Readme.

Julia: Designer/writer<br>
Sketched several prototype visualizations.
<br>Modeled several early iterations of the scatterplot in Tableau.
<br>Cleaned up ASCII characters in data.
<br>Wrote and edited content for Readme.
<br>Gave feedback on iterations of visualizations.





<h2>Design Process</h2>
1. After reviewing the dataset and article, we decided upon a research question: what aspects of artwork influence how likable it is?
<br>2. We individually brainstormed two to three visualizations on paper, ranging from safe and realistic concepts to ambitious ones. 
<br>3. After prototyping in Tableau and Bokeh, we came together as a group to discuss our visualizations and honed in on two promising types: an adjacency matrix and a scatterplot. Based on our positive learning experience with Bokeh during the last project, we decided to use it again as our platform.
<br>4. We then began outlining our design decisions for each of the two visualizations and how we might effectively encode the data of interest. Jack began constructing the scatterplot and Mike began working on the adjacency matrix, with code pulled from the Les Miserables Co-occurrence Grid code. Julia and Jess tested versions of these prototypes as they went live while together in a meeting, checking for bugs and suggesting next step improvements.  Julia and Jack worked to find and clean the special character bugs in the dataset.
<br>5. During the following meetings we worked on refining iterations of our design and deciding on the best color schemes for each. 
<br>6. We worked remotely to continue polishing the two visualizations and collectively make design decisions over Thanksgiving break. 



<h2>Scatterplot</h2>

Attributes: Our Scatterplot incorporates both categorical and quantitative data attributes to examine patterns in painting likeability across time, artistic style, and presence of human figures. Each point represents one painting in the dataset. Year is along the x axis and the mean rating score for each painting is along the y axis, with labels pulled from some of the phrasing used in the study’s original questionnaire. Artistic style is encoded as color, specifically a set of easily distinguishable independent hues that are aesthetically cohesive and appealing. Human figure categories are also encoded in a similar manner, using hues that are different from those for artistic style as to not conflate. Artistic style and human figures are categorical attributes and  year is an ordinal attribute. Mean rating works as a quantitative attribute, though we have used categorical labels to describe it in order to display it in a way that is most intuitive to viewers.<br>

<br>Interactivity: Users can hover over a specific data point to get more information about the artwork in a tooltip box, which displays the title, artist, year and an image of the piece itself. The tooltip will display all information on all of the paintings’ data points that are stacked below the cursor, which allows for insights into the groups of paintings have very similar mean ratings and are from similar years. Viewing the actual artwork itself in the tooltip allows the user to intuitively see the intersections of the data attributes in real time. The user can also zoom, pan, and reset the display to better explore the more dense areas of the chart or focus in on a specific area of interest. Users can also use the tabs on the top of the display to toggle between color representing artistic style or human figures. This seamless toggle mechanism allows the user to compare any relationship between time, artistic style, human figures, and/or mean rating.<br>

<br>Perceptual Concepts: Our design leverages the perceptual mechanisms of both gists and Gestalt Principles. The Gestalt Principle of Similarity helps the user discern similar data points by color, either representing artistic style or by presence of human figures. Dots of the same color, regardless of their location in the scatterplot will be seen as related to one another within a single category. The Gestalt Principle of Proximity is also at play here, with data points horizontally close together being created in a similar period of history, or those vertically close together have similar mean ratings. Users are also able to gain insights simply from the gist of this visualization. Areas of high density data points are more colorful and salient, reflecting a higher volume and diversity of paintings at different periods in history and degrees of likeability.<br>
<br>


<h2>Adjacency Matrix</h2>

Attributes: Our adjacency matrix contains both categorical and quantitative attributes. The twenty emotions used in the original study are arranged along both the rows and columns, starting with positive ones at the top left corner, moving outwards into the other/mixed and then negative emotions, as defined by the original study (and shown nicely in their poster). The hue of the grid boxes corresponds with the category of the emotion within that box whether positive, other/mixed or negative. For boxes at the intersection of emotions of the same category, the box will be the color assigned to that category. Otherwise, if the box is a cross between two different categories, the assigned hue is a light blue/gray. The quantitative attribute of co-occurrence frequency is represented in tint or shade. Pairs of emotions that are more frequently tagged together for a painting will have a darker shade, while those that do not will have a lighter shade. Users can hover over the boxes to see the number of paintings that evoked that pair of emotions in the study’s participants. Emotion category is a categorical attribute, co-occurrence frequency is a quantitative attribute, and mean rating is represented as a quantitative attribute, which we will discuss more in the interactivity section. <br>  

<br>Interactivity: Hovering over a square will show the users the two emotions that intersect in that square and the amount of times that they show up together in a piece of art in a tooltip box. Also, akin to the scatterplot, tabs along the top of the display allow the user to manipulate the matrix grid. The tabs here act as filters, to include all of the paintings in the dataset, only those with a positive mean rating (liked), a mean rating between 0.5 and -0.5 (neutral), or a negative mean rating (disliked). This interactive feature is what allows the user to explore the relationship between which emotions are associated with the likability of artwork. <br>

<br>Perceptual Concepts: Our adjacency matrix leverages the Gestalt Principle of Similarity in the categorical color scheme that we used to group the “positive”, “other/mixed” and “negative” emotions as they were grouped by the researchers for this project. Users can tell that boxes that are similarly colored belong to the same group of emotions. It is the tinting of this color scheme that works to convey information within the concept of bottom-up visual attention. Darker shaded boxes indicate that there is a higher level of concurrence between two emotions and this use of color draws the viewer’s attention to those points of interest, therefore influencing what aspects of the visualization the viewer pays attention to. The user can also glean insights just from the gist, especially as they toggle through mean rating filter. By scanning for the darkest regions of the grid, it’s possible to intuitively see which types of emotions are more frequently associated with liked or disliked works of art, both by using the spatial ordering of the emotional categories positive to negative and by hue. 


