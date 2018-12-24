
def get_followerdata(screen_name):
    twitter = Twython(APP_KEY, APP_SECRET)
    screen_name = screen_name
    user = []
    users = []
    #対象のユーザー名からフォロワーidリストを取得
    followers_ids = [fw for fw in twitter.cursor(twitter.get_followers_ids, screen_name=screen_name)]

    for i in followers_ids:
        user.append(i)
        if len(user) == 100:
            users_data = twitter.lookup_user(user_id=user)

            print("ok")
            # users.append(users_data)
            users.extend(users_data)
            print(len(users_data))
            print(users)
            user.clear()
    users_data = twitter.lookup_user(user_id=user)
    users.extend(users_data)
