REM login to your Heroku account
heroku login

REM change dash-app to a unique name
heroku create multipage-erlt-dashboard

REM deploy to Heroku
git push heroku master

REM run the app with a 1 heroku "dyno"
heroku ps:scale web=1

