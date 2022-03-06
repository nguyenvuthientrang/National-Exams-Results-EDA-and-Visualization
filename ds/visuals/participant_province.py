def count_province(df):
    
    A = df['CityCode'].value_counts().sort_index()
    AreaSet = []
    for i in City.keys():
        for j in Area:
            if i in Area[j]:
                AreaSet.append(j)
    AreaName = [AreaCode[i] for i in AreaSet]
    CountTinh = {'CityCode':pd.Series(City.keys()),
                 'Province':pd.Series(City.values()),
                 'AreaCode': pd.Series(AreaSet),
                 'Area':pd.Series(AreaName),
                 'Count':pd.Series(list(A))}
    df = pd.DataFrame(CountTinh)
    fig = px.bar(df, x="Province", y="Count",barmode='group',color='Area',width=1000,height=600)
    fig.update_traces(width = 1)
    return fig