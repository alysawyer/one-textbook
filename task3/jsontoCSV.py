import pandas as pd 
import os
# text-ada-001.capitvlvm_1.style1.quizTypeA.json

def create_pivot_table(df, index, columns, values): 
    df = df.groupby([index, columns])[values].mean().reset_index() 
    pivot_df = df.pivot(index=index, columns=columns, values=values)
    return pivot_df


# iterate through all the files in results folder
directory = 'results'
data = []
for filename in os.listdir(directory):
    filePath = os.path.join(directory, filename)
    if os.path.isfile(filePath):
        with open(filePath) as f:
           accuracy = float(f.read())
        model, chapter, style, quiz_type = filename.split(".")[0:4]
        data.append([model, chapter, style, quiz_type, accuracy])


# making data frame
df = pd.DataFrame(data, columns=["model", "chapter", "style", "quiz_type", "accuracy"])

# pivoting to make specific tables

# model chapter table
pivot_df_model_chapter = create_pivot_table(df, 'model', 'chapter', 'accuracy')
pivot_df_model_chapter.to_csv('results-model-chapter.csv')

# chapter quiz type table
pivot_df_chapter_quiztype = create_pivot_table(df, 'chapter', 'quiz_type', 'accuracy')
pivot_df_chapter_quiztype.to_csv('results-chapter-quiz_type.csv')

# TODO: free response multi choice table

