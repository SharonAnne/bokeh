.. _quickstart:

##########
Quickstart
##########

Some python distributions include Bokeh at installation.  To check if 
your python installation includes Bokeh, run the command in python::

    >> import bokeh
    
If you get the error ``No module named bokeh`` then you will need to download and 
install the module.

Downloading
-----------

If you are using the `Anaconda Python distribution <http://continuum.io/anaconda>`_ install bokeh and it's dependencies from a bash prompt with::

    $ conda install bokeh

For other distributions of python, use one of the package managers pip or easy-install, with one of these::

    $ pip install bokeh
    $ easy-install bokeh

To download from source, clone the `Bokeh repository <https://github.com/ContinuumIO/bokeh>`_ from Github,
then run::

    $ python setup.py install

If you are using Windows, please see the
:ref:`install_windows`.

Plotting
-------------------------

To generate a preformatted scatter plot:

The same plot can be built from individual glyphs using:


Generate Static HTML Files
--------------------------

Now you are ready to generate static plots. In ``examples/plotting/file/``, try::

    $ python iris.py

This will write a static HTML file ``iris.html`` in the current directory and
open a browser window to display it, and it should look like:

.. image:: /_images/iris.png

Try running ``line.py`` or ``candlestick.py`` for other static HTML file examples.

If these HTML files are too large (since they embed the source code for
the BokehJS JavaScript library, as well as the various Bokeh CSS), then you
can modify any of the example scripts in ``examples/plotting/file`` and change
the ``output_file()`` function calls by adding ``mode`` keyword argument.
For the ``iris.py`` example, you could change the call::

    output_file("iris.html", title="iris.py example")

to::

    output_file("iris.html", title="iris.py example", mode="cdn")

Using the Plot Server
---------------------

Rather than embedding all the data directly into the HTML file, you can also
store data into a "plot server" and the client-side library will directly,
dynamically load the data from there.

If you installed Bokeh via running ``python setup.py`` or via a
`conda <http://docs.continuum.io/conda/intro.html>`_ package, then you should
have a command `bokeh-server` available to you.  You can run this command in
any directory, but it will create temporary files in the directory in which
you are running it.  You may want to create a ``~/bokehtemp/`` directory or
some such, and run the command there::

    $ bokeh-server

If you have Bokeh installed for development mode (see :ref:`developer_install`),
then you should go into the checked-out source directory and run::

    $ python ./bokeh-server

Once the plot server is started, you can run any of the examples in
``examples/plotting/server/``.  When those examples run, they will not
necessarily open a new browser window.  Instead, you should navigate to
**http://localhost:5006/bokeh** and you will see a list of all plot "documents"
which have been created.  Clicking on a document name will display its
plots.


Example IPython Notebooks
-------------------------

There are a number of IPython notebooks in the ``examples/plotting/notebook/``
directory.  Just run::

    ipython notebook

in that directory, and open any of the notebooks.
