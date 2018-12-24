from twython import Twython, TwythonError
import re


class SearchTweet(Twython, TwythonError):
    """
    twythonライブラリを使って、twittwerAPIを検索
    __init__ :　コンストラクタ
    get_tweet_id: urlから正規表現でidを抽出
    get_tweet_status: idから本文とユーザ名を取得
    get_retweet:リツイートを取得
    get_follower_data:フォロワーのデータを取得
    """

    def __init__(self, APP_KEY: str, APP_SECRET: str) -> None:
        """
            コンストラクタ
            APP_KEY,APP_SERCRET:Twythonに渡すAPIキー
            twitter:twythonオブジェクト
        """
        self.APP_KEY = APP_KEY
        self.APP_SECRET = APP_SECRET
        self.twitter = Twython(self.APP_KEY, self.APP_SECRET)


    def get_tweet_id(self, url: str) -> str:
        """

           url文字列から正規表現でidを抽出。
        """
        self.url = url
        s = re.search("[0-9].*", url)
        self.tweet_id = s.group(0)
        return self.tweet_id


    def get_tweet_status(self, tweet_id: str) -> str:
        """
           tweet_idを引数に、twythonのshow_statusメソッドで、ツイート本文と、screen_nameを取得。
           ツイート本文はreでurlと空白を消す前処理をする。
        """

        self.result = self.twitter.show_status(id=tweet_id)
        self.text = " "
        self.user = self.result["user"]["screen_name"]
        #self.text, self.user = self.result["text"], self.result["user"]["screen_name"]
        #self.text = re.sub('https?://.*',"", self.text)
        #self.text = re.sub("#.*", "", self.text)
        #self.text = self.text.replace('\n','')
        self.user = "@" + self.user
        return self.text, self.user


    def get_retweet(self, text: str, user: str, since_id: str, max_id: str, count: int) -> list:
        """
           ツイート本文と、ユーザ名、ツイートidを引数に、twythonのsearchメソッドでリツイートを探す。
           query_filter:リツイートだけを取得するためのパラメータ
           count: 一回のリクエストで取得するツイート数。100で初期化。
           since_id:該当ツイートより後のツイートを取得するために指定する。twythonに渡すパラメータ用に定義。
           maxid:ページング用

        """
        query_filter = "filter:retweets"
        self.since_id = since_id
        self.max_id = max_id
        self.count = count
        self.result = self.twitter.search(q=text + " " + query_filter + " " + user, since_id=self.since_id, max_id=self.max_id)

        return self.result

    def get_followerdata(self, screen_name: str) -> list:
        """
        　　1.対象のユーザー名を引数にして、フォロワーのidをリストで取得。
        　　2.idのリストからAPIパラメータ数の上限100ずつ取り出して、それを引数にフォロワーのstatusを取得
        　　3.
           screen_name:フォロワーのリストを取得するアカウントのユーザー名
           temp_user:
           temp_data:
           followers_data:
           followers_ids:対象アカウントのフォロワーのidリスト
        :return:
        """

        self.screen_name = screen_name
        self.users_ids = []
        self.followers_data = []
        # 対象のユーザー名からフォロワーidリストを取得
        self.followers_ids = [fw for fw in twitter.cursor(twitter.get_followers_ids, screen_name=screen_name)]
        # 取得したリストからidを取り出してuserリストに追加していく。
        for i in followers_ids:
            users_ids.append(i)
        # APIの一度にリクエストするパラメータuser_idが、上限の100になったら、API叩いて、結果のリストをusersに連結。
            if len(users_ids) == 100:
                temp_data = twitter.lookup_user(user_id=users_ids)
                followers_data.extend(temp_data)
        # リストの中身を消去
                users_ids.clear()
        # forで100個ずつ回したあとの残り端数を取得
        temp_data = twitter.lookup_user(user_id=users_ids)
        followers_data.extend(temp_data)

        return self.followers_data


