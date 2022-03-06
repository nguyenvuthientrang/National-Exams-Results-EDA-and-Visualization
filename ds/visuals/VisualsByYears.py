import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
from plotly.subplots import make_subplots

#############################################################################################

def add_label(data_path, ranges, colors, subject):
  province_avg = pd.read_csv(data_path)
  criteria = [province_avg[subject].between(r[0], r[1]) for r in ranges]
  province_avg['Level'] = np.select(criteria, [i for i in range(len(ranges))], 0)
  province_avg['Color'] = np.select(criteria, colors, 0)

  return province_avg[['CityCode', subject, 'Level', 'Color']]


def sankey(ranges, nodes, node_colors, path_colors, subject, weight=False):
  plt.clf()
  sns.set(style="darkgrid")
  plt.rcParams['figure.figsize'] = (15, 10)
  province_avg2021 = add_label("ds/Province_Avg2021.csv", ranges, path_colors, subject)
  province_avg2020 = add_label("ds/Province_Avg2020.csv", ranges, path_colors, subject)
  province_avg2019 = add_label("ds/Province_Avg2019.csv", ranges, path_colors, subject)
  province_avg2018 = add_label("ds/Province_Avg2018.csv", ranges, path_colors, subject)

  if weight == False:
    value = [5] * 189
  else:
    value = list(province_avg2019[subject] - province_avg2018[subject]) + list(
      province_avg2020[subject] - province_avg2019[subject]) + list(
      province_avg2021[subject] - province_avg2020[subject])

  fig = go.Figure(data=[go.Sankey(
    node=dict(
      pad=15,
      thickness=15,
      line=dict(color="rgba(255, 0, 0, 0)", width=0.5),
      label=nodes * 4,
      color=node_colors * 4
    ),
    link=dict(
      source=list(province_avg2018['Level']) + list(province_avg2019['Level'] + len(ranges)) + list(
        province_avg2020['Level'] + 2 * len(ranges)),  # indices correspond to labels, eg A1, A2, A1, B1, ...
      target=list(province_avg2019['Level'] + len(ranges)) + list(province_avg2020['Level'] + 2 * len(ranges)) + list(
        province_avg2021['Level'] + 3 * len(ranges)),
      value=value,
      color=list(province_avg2018['Color']) + list(province_avg2019['Color']) + list(province_avg2020['Color'])
    ))])

  fig.update_layout(title_text=subject, font_size=10)
  fig.update_layout(width=1000)
  fig.update_layout(height=700)
  fig.show()


#############################################################################################
