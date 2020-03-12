from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017"
conn = 'mongodb://localhost:27017'
#mongo = pymongo(app)
mongo = pymongo.MongoClient(conn)

db = mongo.mars_db

#db.news.drop()

# Route to render index.html template using data from Mongo
@app.route("/scrape_mars")
def index():

    # Find one record of data from the mongo database
    mars_dict = list(db.news.find())
    print(mars_dict)
    # Return template and data
    return render_template("index.html", mars=mars_dict)

# @app.route('/')
# def index():
#     # Store the entire team collection in a list
#     teams = list(db.team.find())
#     print(teams)

#     # Return the template with the teams list passed in
#     return render_template('index.html', teams=teams)


# @app.route("/scrape")
# def scrape():
  
#     mars_dict = mongo.db.mars_dict
#     mars_data = scrape_mars.scrape()
#     # Update the Mongo database using update and upsert=True
#     mars_dict.update({}, mars_data, upsert=True)
#     return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)