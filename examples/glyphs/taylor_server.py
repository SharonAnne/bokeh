from __future__ import print_function

import sys
import time
import requests

import numpy as np
import sympy as sy

from bokeh.objects import Plot, DataRange1d, LinearAxis, ColumnDataSource, Glyph, Grid, Legend
from bokeh.widgetobjects import Slider, TextInput, HBox, VBox
from bokeh.glyphs import Patch, Line, Text
from bokeh.session import PlotServerSession

xs = sy.Symbol('x')
expr = sy.exp(-xs)*sy.sin(xs)
order = 1

def taylor(fx, xs, order, x_range=(0, 1), n=200):
    x0, x1 = x_range
    x = np.linspace(float(x0), float(x1), n)

    fy = sy.lambdify(xs, fx, modules=['numpy'])(x)
    tx = fx.series(xs, n=order).removeO()

    if tx.is_Number:
        ty = np.zeros_like(x)
        ty.fill(float(tx))
    else:
        ty = sy.lambdify(xs, tx, modules=['numpy'])(x)

    return x, fy, ty

def update_data():
    x, fy, ty = taylor(expr, xs, order, (-2*sy.pi, 2*sy.pi), 200)

    plot.title = "%s vs. taylor(%s, n=%d)" % (expr, expr, order)
    legend.legends = {
        "%s"         % expr: [line_f_glyph],
        "taylor(%s)" % expr: [line_t_glyph],
    }
    source.data = dict(x=x, fy=fy, ty=ty)
    slider.value = order

    session.store_all()

source = ColumnDataSource(data=dict(
    x  = [],
    fy = [],
    ty = [],
))

xdr = DataRange1d(sources=[source.columns("x")])
ydr = DataRange1d(sources=[source.columns("fy")])

plot = Plot(data_sources=[source], x_range=xdr, y_range=ydr, width=800, height=400)

line_f = Line(x="x", y="fy", line_color="blue", line_width=2)
line_f_glyph = Glyph(data_source=source, xdata_range=xdr, ydata_range=ydr, glyph=line_f)
plot.renderers.append(line_f_glyph)

line_t = Line(x="x", y="ty", line_color="red", line_width=2)
line_t_glyph = Glyph(data_source=source, xdata_range=xdr, ydata_range=ydr, glyph=line_t)
plot.renderers.append(line_t_glyph)

xaxis = LinearAxis(plot=plot, dimension=0)
yaxis = LinearAxis(plot=plot, dimension=1)

xgrid = Grid(plot=plot, dimension=0, axis=xaxis)
ygrid = Grid(plot=plot, dimension=1, axis=yaxis)

legend = Legend(plot=plot, orientation="bottom_left")
plot.renderers.append(legend)

def on_slider_value_change(obj, attr, old, new):
    global order
    order = int(new)
    update_data()

def on_text_value_change(obj, attr, old, new):
    global expr
    expr = sy.sympify(new, dict(x=xs))
    update_data()

slider = Slider(start=1, end=20, value=order, step=1, title="Order:")
slider.on_change('value', on_slider_value_change)

text = TextInput(value=str(expr), title="Expression:")
text.on_change('value', on_text_value_change)

inputs = HBox(children=[slider, text])
layout = VBox(children=[inputs, plot])

try:
    session = PlotServerSession(serverloc="http://localhost:5006")
except requests.exceptions.ConnectionError:
    print("ERROR: This example requires the plot server. Please make sure plot server is running, by executing 'bokeh-server'")
    sys.exit(1)

session.use_doc('taylor_server')
session.add_plot(layout)

update_data()

try:
    to_pull = [slider, text]
    while True:
        for obj in to_pull:
            obj.pull()
        time.sleep(0.1)
except KeyboardInterrupt:
    print()