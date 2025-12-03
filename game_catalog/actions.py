def toggle_favorite(user, instance):
    if user.favorited(instance):
        user.favorite_games.remove(instance)
    else:
        user.favorite_games.add(instance)
