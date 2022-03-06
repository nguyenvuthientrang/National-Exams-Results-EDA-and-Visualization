def score_spectrum_area(df,subject,CodeArea):
 
    data_province = df[df.CityArea == CodeArea]
    subject_name = ''
    if (len(subject)<3 or ('-' in subject)):
        bins = [i/2 for i in range(0,61)]
        data_show = data_province[subject].value_counts(bins = bins).sort_index()
        subject_name = 'Combination: '+subject
    else:
        data_show = data_province[subject].value_counts().sort_index()
        subject_name = subject
        
    count_score = {'Score': pd.Series((data_show.index).astype('str')),
               'Count': pd.Series(data_show.values)}
    
    df = pd.DataFrame(count_score)
    fig = px.bar(df, x='Score', y='Count',title=AreaCode[CodeArea]+': '+subject_name)
    return fig