from flask import Flask
from flask import render_template,redirect,url_for
import pandas as pd
from prediction import Predictor
import random
import time

app= Flask(__name__)

book_df=pd.read_csv('new_books.csv')
pred_df=pd.read_csv('output.csv')
pred_df.drop('Unnamed: 0',axis=1,inplace=True)

predict=Predictor(pred_df,book_df)
reccomended_books=predict.make_prediction(12)


df1=book_df.loc[reccomended_books[0]]
df2=book_df.iloc[7:13]

links_df=df1[['image_url','title']]
links=links_df.to_records()
links2=df2[['image_url','title']].to_records()

high_rated_books=book_df.sort_values('average_rating',ascending=False)
high_rated=high_rated_books.iloc[0:30]
high_rated_df=high_rated[['image_url','title']].to_records()

liked_books=[]

first_sec=[0,30,60,90]
last_sec=[30,60,90,120]

btn_styles=['outline-dark']*4


x_index=0
y_index=6

def get_new_books(value):
    total_books=len(value)
    recent=80*(total_books)//100
    first=75*(total_books)//100
    random_books=[value[random.randint(0,first)] for n in range(3)]
    print(recent)
    print(first)
    value=value[recent:]
    value=value+random_books
    return list(set(value))

@app.route('/')
def home():
    global links,x_index,y_index
    reccs=links[x_index:y_index]
    return render_template('index.html',links=reccs,links2=links2)

@app.route("/forward/<var>", methods=['POST'])
def move_forward(var):
    global links,x_index,y_index
    x_index=0
    y_index=6
    var=int(var)
    k=predict.make_prediction(var)
    reccomended_books = k
    df1 = book_df.loc[reccomended_books[0]]
    links_df = df1[['image_url', 'title']]
    links = links_df.to_records()
    return redirect(url_for('home'))

@app.route('/high_rated')
def high_rated():
    global x_index,y_index
    x_index=0
    y_index=6
    return  render_template('allbooks.html',data=high_rated_df,styles=btn_styles)

@app.route('/high_rated/<var>',methods=['POST'])
def like(var):
    global liked_books
    if int(var) not in liked_books:
        liked_books.append(int(var))
        print(liked_books)
    return redirect(url_for('high_rated'))


@app.route('/high-rated/cum-predict')
def predict_for_all():
    global liked_books,x_index,y_index
    global links
    if liked_books == []:
        liked_books.append(12)
    new_books=get_new_books(liked_books)
    dfs = predict.cum_prediction(ids=new_books)
    print(len(dfs))
    print(f'predict {new_books}')
    nums=1/len(liked_books)
    new_df=nums*sum(dfs)
    next_df=new_df.sort_values('index',ascending=False)
    next_df.reset_index(inplace=True)
    df1 = book_df.loc[next_df[0]]
    links_df = df1[['image_url', 'title']]
    links = links_df.to_records()
    x_index=0
    y_index=6
    return redirect(url_for('home'))

@app.route('/high-rated/pages/<var>',methods=['POST'])
def page_change(var):
    global high_rated_df
    global high_rated_books
    global btn_styles
    var=int(var)
    for n in range(4):
        if n==var:
            btn_styles[n]='dark'
        else:
            btn_styles[n]='outline-dark'
    next_page = high_rated_books.iloc[first_sec[var]:last_sec[var]]
    print(first_sec[var])
    high_rated_df = next_page[['image_url', 'title']].to_records()
    return redirect(url_for('high_rated'))


@app.route('/recommend_more',methods=['POST'])
def recommend():
    global x_index,y_index
    x_index+=6
    y_index+=6
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)





