# coding: UTF-8
import setting
from time import sleep
from flask import Flask, session, render_template, request
from searchtweet import SearchTweet
from show_graph import data_to_graph
from twython import TwythonError

#APP_KEY
APP_KEY = setting.AK
#Appsecret
APP_SECRET = setting.AS

#callbakurl(ローカル)
CALLBACK_URL = "http://localhost:9999/"
#CALLBACK_URL = "http://retweetlist.herokuapp.com/"

#appでインスタンス化。カレントに移動。URLをindexにマッピング
app = Flask(__name__, static_folder='.', static_url_path='')

#flaskのセッションキーを読み込む
app.secret_key = setting.SK

t = SearchTweet(APP_KEY, APP_SECRET)

#routing
@app.route('/')
def home():
    return render_template('index.html')



@app.route('/search_reuslt.html', methods=['GET', 'POST'])

def post_query():
    """
    retweetを表示したいid、ユーザ名、テキストをフォームから受け取る。受けたidをretweet_serachに渡して、結果をレンダリング。

    """
    if request.method == 'POST':
        url = request.form['tweet_url']
        tweet_id = t.get_tweet_id(url)
        text, user = t.get_tweet_status(tweet_id)
        status, count = retweet_search(text, user, tweet_id)
        script, div = data_to_graph(status)
        return render_template('/search_result.html',  status=status, count=count, script=script, div=div, text=text)


    else:
        return render_template('/search_result.html')

#urlからツイートを取得

#twitterAPIでリツイートを検索
def retweet_search(text, user, tweet_id):
    """
　　　get_retweetで取得したツイートをapiのリクエスト上限数の100ずつ取得して、変数tweetに格納。
　　　forで処理して、status_listに格納。最後に入れたツイートのidをmaxidに格納。
    :param text: ツイート本文。get_tweet_statusで前処理したものを受け取る。
    :param user:screen_name
    :param tweet_id:ツイートのid、ループのページング制御に使用。
    :return:ツイートデータの辞書リストとツイート数のカウント結果。

    """
    #カウント初期化
    cnt = 0
    status_list = []

    try:
        tweet = t.get_retweet(text, user, since_id=tweet_id, max_id=None, count=100)
        while True:

            for status in tweet['statuses']:

                if status["id"] in status_list:
                    status_list.pop(status["id"])
                else:
                    status_list.append(status)
                    cnt += 1
                    maxid = int(status["id"]) - 1


            if len(tweet["statuses"]) == 0:
                break

            tweet = t.get_retweet(text, user, since_id=None, max_id=str(maxid), count=100)
            sleep(1)
    except TwythonError as te:
        return render_template('/search_result.html', te=te)
    return status_list, cnt

#無効なidをpostしたときの例外処理
@app.errorhandler(500)
def id_not_found(error):
    e = "エラー！　すいません！ツイートが見つかりませんでした。別のIDで検索してください"
    return render_template('/search_result.html', e=e)

app.debug=True
if __name__ == '__main__':
   app.run(port=9999)

