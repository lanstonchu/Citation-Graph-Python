Project Title: **Automatic Generation of Academic Citation Graph (Python Version)**

Also on: [WordPress][8]

This Python tool will automatically generate citation graph of a given set of papers. This is a Python version of a similar tool that I previously created in Wolfram Language.

Source Code and Data: [Original Wolfram Language version][2] and [Python version][3]

1. Download Chrome Driver at [here][6] with respect to your Chrome version (the current version in my Github repository is for Chrome version 77 only)
2. Select papers from your references management software (e.g. Mendeley) and export to .bib file.
3. Run **Citation_Tree.py** to draw citation graph

**Notes:**

1. This Python version can only draw [DAG][7]. If you got an error because your network is not DAG, please remove some papers in your .bib file.
2. If your Chrome driver doesn't work, please confirm you are using the correct driver version.
3. If the graph doesn't look good, you may want to change figsize and rerun the "last 3 lines only" to save time
4. Or you may re-run starting from the line "posi={}"
5. In my code, I set the desired distance between vertices to be 0.7, and I will loop through all vertices for 1.4*x times, where x is the number of vertices. You may want to adjust these parameters according to your own requirement in graph quality and run time.

-----------------------------------------

(Details)

In certain fields of academic studies (e.g. Deep Learning), academic papers are released in a much faster speed than people in the field read them (although it is certainly true in all fields). As researchers, we know that we want to know how the papers fit into the whole academic conversation, so it would be nice if we can automatically generate an academic paper citation graph, and immediately tell which one cites which.

I created a tool for you *homo academicus* to automatically create the said citation graph for any paper. This should be helpful for researchers to catch up on the trend of a rapidly changing field.

First, if you are using Mendeley (or any other Reference Management Software), export your papers as a **.bib** file which should include the arXiv ID and issue year information. Then, use Mathematica to run the code. It will take you to the [Astrophysics Data System of Harvard][4] and find out the list of reference for each paper. Finally, a citation graph will be drawn with the help of Wolfram Language.

See the below example. Here, I’ve selected a list of papers in Mendeley about adversarial examples (published in the past five years), and I want to know how they are related to each other (“citationally”).

![Image 1 - Mendeley][5]

Click **File->Export** and then save the papers’ metadata as **My Collection.bib**.

Download Chrome Driver at [here][6] with respect to your Chrome version (the current version in my Github repository is for Chrome version 77 only)

Run the code **Citation_Tree.py**. This is the end product:

![Image 2 - Citation Tree][1]

You can see that *Transferability in Machine Learning: from Phenomena to Black-Box Attacks using Adversarial Samples (Papernot et. al. 2016)* and *Explaining and harnessing adversarial examples (Goodfellow et. al. 2014)* are the most influential nodes among those selected papers (i.e. most cited).

If you want to add more information (say author) to the vertex labels, you can modify the second to last column of **data_all_papers** (i.e. **vrt_name_multi_lines**) to do that. You just need to change a few lines so I am not going to be verbose here.

Enjoy.

[1]: https://github.com/lanstonchu/Citation-Graph-Python/blob/master/Citaion%20Graph%20Example.png
[2]: https://github.com/lanstonchu/citation-graph
[3]: https://github.com/lanstonchu/Citation-Graph-Python
[4]: https://ui.adsabs.harvard.edu/
[5]: https://raw.githubusercontent.com/lanstonchu/citation-graph/master/Mendeley.png
[6]: https://chromedriver.chromium.org/downloads
[7]: https://en.wikipedia.org/wiki/Directed_acyclic_graph
[8]: https://lanstonchu.wordpress.com/2019/09/22/automatic-generation-of-academic-citation-graph-python-version/
