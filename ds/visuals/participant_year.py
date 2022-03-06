def count_year(bigData):
    A = bigData['year'].value_counts().sort_index()
    CountYear = {'year':pd.Series(A.index.astype('str')),
                 'Count':pd.Series(A.values)}
    df = pd.DataFrame(CountYear)
    fig = px.bar(df, x='year', y='Count', labels={'Count':'Participant number'})
    return fig