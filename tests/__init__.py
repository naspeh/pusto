from pusto import App


app = App(prefs={
    'mongo': {'db': 'test_pusto'}
})


def drop_db():
    app.mongo.drop_database(app['mongo:db'])
