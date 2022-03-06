def boxplot(subject):
    df1 = df[df[subject]>=0].sample(1000)
    fig = px.box(df1, y=subject, points="all")
    return fig