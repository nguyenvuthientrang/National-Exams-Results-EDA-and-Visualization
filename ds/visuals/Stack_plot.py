import plotly.graph_objects as go

def AreaStack(subject):
    BigData = {2018: result(2018),
               2019: result(2019),
               2020: result(2020),
               2021: result(2021)}

    r1 = [count_range(BigData[2018+i],subject,0,5.1) for i in range(4)]
    r2 = [count_range(BigData[2018+i],subject,5.2,7.1) for i in range(4)]
    r3 = [count_range(BigData[2018+i],subject,7.2,8.0) for i in range(4)]
    r4 = [count_range(BigData[2018+i],subject,8.1,10) for i in range(4)]

    x=[2018,2019,2020,2021]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x, y=r1,
        mode='lines',
        line=dict(width=0.5, color='rgb(190, 87, 12)'),
        stackgroup='one',
        name = '0 - 5.1',
        groupnorm='percent' # sets the normalization for the sum of the stackgroup
    ))
    fig.add_trace(go.Scatter(
        x=x, y=r2,
        mode='lines',
        line=dict(width=0.5, color='rgb(225, 105, 180)'),
        name = '5.2 - 7.1',
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=r3,
        mode='lines',
        line=dict(width=0.5, color='rgb(255, 220, 70)'),
        name = '7.2 - 8.0',
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=r4,
        mode='lines',
        line=dict(width=0.5, color='rgb(255, 10, 40)'),
        name = '8.1 - 10',
        stackgroup='one'
    ))

    fig.update_layout(
        showlegend=True,
        xaxis_type='category',
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%'),
        title = subject,
        legend_title = 'Score_range')

    return fig