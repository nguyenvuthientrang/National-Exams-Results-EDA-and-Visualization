def count_combi(df):
    
    A = df['Highest_combi'].value_counts().sort_index()
    CountTinh = {'Highest_combi':pd.Series(['A','A1','B','C','D1']),
                 'Count':pd.Series(list(A))}
    df = pd.DataFrame(CountTinh)
    fig = px.bar(df, x='Highest_combi', y='Count', labels={'Count':'Participant number'})
    return fig