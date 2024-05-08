#
# License
#

import numpy as np
import plotly.graph_objects as go

def guardar_html(fig, filename):
    """
    En lugar de exportar directamente el objeto plotly.figure a un archivo,
    lo convierte a html para poder centrar la figura haciendo un reemplazo
    de string.

    Parameters
    ----------
    fig : plotly.graph_objs._figure.Figure
        La figura creada con Plotly.
    filename : str
        Nombre del archivo donde guardar la figura, como html.

    Returns
    -------
    """
    fig = fig.to_html()
    figstr = fig.replace('<div>', '<div align="center">')
    with open(filename, "w") as file:
        file.write(figstr)


def op_plot_02(y1, z=np.linspace(-2, 5, 500), N=500, Lmax=3.5, dL=0.01, html=False):
    """Graficador con slider. Un haz, cambia n, tiempo fijo.

    Grafica un solo haz, con un cambio de índice de refracción en el
    camino, y un slider para modificar la longitud del obstáculo.

    Parameters
    ----------
    y1 : function
        Una función que calcule los valores de y para cada valor de z.
    z : numpy.ndarray
        Los valores de z donde calcular y1.
    N : int
        Cantidad de puntos en el gráfico.
    Lmax : float
        Longitud máxima del obstáculo.
    dL : float
        Paso entre valores de longitud en el slider.
    html : bool
        Hack para graficar correctamente las flechas. Al exportar como html,
        si se usa arrow-bar-up funciona siempre apuntando
        hacia el punto. Pero dentro de jupyter es necesario intercambiar
        arrow-bar-up y arrow-bar-down según el punto sea positivo o negativo.

    Returns
    -------
    plotly.graph_objs._figure.Figure
        Una figura plotly
    """

    fig = go.Figure()
    fig.update_layout(showlegend=False, width=1050, height=550)
    fig.update_yaxes(automargin=False)
    fig.update_xaxes(title_text='z', titlefont=dict(size=18))
    fig.update_yaxes(title_text='E', titlefont=dict(size=18), title_standoff = 0)
    fig.update_yaxes(showticklabels=False)
    fig.update_yaxes(range = [-1,1])

    # Add traces, one for each slider step
    Ls = np.arange(0, Lmax, dL)
    for step in Ls:
        fig.add_trace(
            go.Scatter(
                visible=False,
                mode='lines',
                name="haz",
                x=z,
                y=[y1(zi, step) for zi in z]))
    # Add arrows, one for each slider step
    for step in Ls:
        ys = y1(4, step)
        if not html:
            if ys > 0:
                symbol = "arrow-bar-up"
            elif ys < 0:
                symbol = "arrow-bar-down"
            else:
                symbol = "arrow"
        else:
            symbol = "arrow-bar-up"
        fig.add_trace(
            go.Scatter(go.Scatter(x=[4,4], y=[0,ys], visible=False,
            marker= dict(size=[0,10],symbol=symbol, color="red", angleref="previous"))))
    for step in Ls:
        fig.add_trace(go.Scatter(x=[-1,-1], y=[0,0.5],
            marker= dict(size=[0,10],symbol= "arrow-bar-up", color="red", angleref="previous")))


    fig.add_shape(type="rect",
        xref="x", yref="y",
        x0=0, y0=-0.6,
        x1=2, y1=0.6,
        line_width=0,
        fillcolor="PaleTurquoise",
        opacity=0.4,
        # visible=False,
    )

    fig.add_shape(type="rect",
        xref="x", yref="y",
        x0=0, y0=-0.6,
        x1=2, y1=0.6,
        line=dict(
            color="LightSeaGreen",
            width=2,
        ),
        # visible=False,
    )

    # fig.add_annotation(x=-1, y=0.6,
    #     text="Posición 1",
    #     showarrow=True,
    #     font=dict(
    #         family="sans serif",
    #         size=18,
    #     ),
    #     arrowhead=2,
    #     arrowsize=1,
    #     arrowwidth=2,
    # )

    # Make L=2 trace visible
    fig.data[int(2/dL)].visible = True
    fig.data[len(Ls) + int(2/dL)].visible = True

    # Create and add slider
    steps = []
    shapes = []
    for i in range(len(Ls)):
    # for i in range(len(fig.data)):
        step = dict(
            method="update",
            label=np.round(i*dL,2),
            args=[{"visible": [False] * len(fig.data)},
                {"shapes" : [
                    {
                    'fillcolor': 'PaleTurquoise',
                    'line': {'width': 0},
                    'opacity': 0.4,
                    'type': 'rect',
                    'visible': True,
                    'x0': 0,
                    'x1': np.round(i*dL,2),
                    'xref': 'x',
                    'y0': -0.6,
                    'y1': 0.6,
                    'yref': 'y'
                    },
                    {
                    'line': {'color': 'LightSeaGreen', 'width': 2},
                    'type': 'rect',
                    'visible': True,
                    'x0': 0,
                    'x1': np.round(i*dL,2),
                    'xref': 'x',
                    'y0': -0.6,
                    'y1': 0.6,
                    'yref': 'y'
                    }
                ] }],  # layout attribute
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        step["args"][0]["visible"][len(Ls)+i] = True  # Toggle i'th trace to "visible"
        step["args"][0]["visible"][2*len(Ls)+i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=int(2/dL),
        len=0.5,
        x=2/7,
        currentvalue={"prefix": "Largo: "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders
        # shapes=shapes
    )

    # fig.show(renderer='notebook')

    return fig

# Es necesario agregar un parámetro para la altura del haz 1, o hacer dos figuras.
# El valor de y=0 para el haz 1 está hardcoded.
def op_plot_04(y1, y2, z=np.linspace(-2, 5, 500), N=500, Lmax=3.5, dL=0.01, html=False):
    """Graficador.

    En proceso de edición.

    Grafica un solo haz, con un cambio de índice de refracción en el
    camino, y un slider para modificar la longitud del obstáculo.

    Parameters
    ----------
    y1, y2 : function
        Funciones que calculen los valores de y para cada valor de z.
    z : numpy.ndarray
        Los valores de z donde calcular y1.
    N : int
        Cantidad de puntos en el gráfico.
    Lmax : float
        Longitud máxima del obstáculo.
    dL : float
        Paso entre valores de longitud en el slider.

    Returns
    -------
    plotly.graph_objs._figure.Figure
        Una figura plotly
    """

    fig = go.Figure()
    fig.update_layout(showlegend=False, width=1150, height=650)
    fig.update_yaxes(automargin=False)
    fig.update_xaxes(title_text='z', titlefont=dict(size=18))
    fig.update_yaxes(title_text='E', titlefont=dict(size=18), title_standoff = 0)
    fig.update_yaxes(showticklabels=False)
    fig.update_yaxes(range = [-1,2.5])

    # Add traces, one for each slider step
    Ls = np.arange(0, Lmax, dL)
    for step in Ls:
        fig.add_trace(
            go.Scatter(
                visible=False,
                mode='lines',
                name="haz 1",
                x=z,
                y=[y1(zi) for zi in z]))
    for step in Ls:
        fig.add_trace(
            go.Scatter(
                visible=False,
                mode='lines',
                name="haz 2",
                x=z,
                y=[y2(zi, step) for zi in z]))

    # Add arrows, one for each slider step
    for step in Ls:
        ys = y2(4, step)
        if not html:
            if ys > 0:
                symbol = "arrow-bar-up"
            elif ys < 0:
                symbol = "arrow-bar-down"
            else:
                symbol = "arrow"
        else:
            symbol = "arrow-bar-up"
        fig.add_trace(
            go.Scatter(go.Scatter(x=[4,4], y=[0,ys], visible=False,
            marker= dict(size=[0,10],symbol=symbol, color="red", angleref="previous"))))
    for step in Ls:
        fig.add_trace(go.Scatter(x=[4,4], y=[1.5,2],
            marker= dict(size=[0,10],symbol= "arrow-bar-up", color="red", angleref="previous")))

    fig.add_shape(type="rect",
        xref="x", yref="y",
        x0=0, y0=-0.6,
        x1=2, y1=0.6,
        line_width=0,
        fillcolor="PaleTurquoise",
        opacity=0.4,
        # visible=False,
    )

    fig.add_shape(type="rect",
        xref="x", yref="y",
        x0=0, y0=-0.6,
        x1=2, y1=0.6,
        line=dict(
            color="LightSeaGreen",
            width=2,
        ),
        # visible=False,
    )

    fig.data[int(2/dL)].visible = True
    fig.data[len(Ls) + int(2/dL)].visible = True
    fig.data[2*len(Ls) + int(2/dL)].visible = True
    fig.data[3*len(Ls) + int(2/dL)].visible = True

    # Create and add slider
    steps = []
    shapes = []
    for i in range(len(Ls)):
    # for i in range(len(fig.data)):
        step = dict(
            method="update",
            label=np.round(i*dL,2),
            args=[{"visible": [False] * len(fig.data)},
                {"shapes" : [
                    {
                    'fillcolor': 'PaleTurquoise',
                    'line': {'width': 0},
                    'opacity': 0.4,
                    'type': 'rect',
                    'visible': True,
                    'x0': 0,
                    'x1': np.round(i*dL,2),
                    'xref': 'x',
                    'y0': -0.6,
                    'y1': 0.6,
                    'yref': 'y'
                    },
                    {
                    'line': {'color': 'LightSeaGreen', 'width': 2},
                    'type': 'rect',
                    'visible': True,
                    'x0': 0,
                    'x1': np.round(i*dL,2),
                    'xref': 'x',
                    'y0': -0.6,
                    'y1': 0.6,
                    'yref': 'y'
                    }
                ] }],  # layout attribute
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        step["args"][0]["visible"][len(Ls)+i] = True  # Toggle i'th trace to "visible"
        step["args"][0]["visible"][2*len(Ls)+i] = True  # Toggle i'th trace to "visible"
        step["args"][0]["visible"][3*len(Ls)+i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=int(2/dL),
        len=0.5,
        x=2/7,
        currentvalue={"prefix": "Largo: "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders
        # shapes=shapes
    )

    # fig.show(renderer='notebook')

    return fig




