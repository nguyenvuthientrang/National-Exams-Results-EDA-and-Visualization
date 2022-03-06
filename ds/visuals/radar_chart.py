def plot_radar(data, range_x):
  categories = list(data.columns)
  fig = go.Figure()
  for i in range(data.shape[0]):
    fig.add_trace(go.Scatterpolar(
        r=list(data.loc[i].values),
        theta=categories,
        fill='toself',
        name=f'Label {i}'
    ))
  fig.update_layout(
    polar=dict(
      radialaxis=dict(
        visible=True,
        range=range_x,
      )),
    showlegend=False
  )
  fig.show()