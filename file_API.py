import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#Data base setup
engine= create_engine("sqlite:///Resources/hawaii.sqlite")
#reflect the existing base into a new model 
base=automap_base()
#reflect the table 
base.prepare(engine, reflect=True)
#save reference to the table 
Measurement= base.classes.measurement 
station=base.classes.station
session=Session(engine)
#Flask setup
app=Flask(__name__)
#all necessery queries
last_year = (session.query(Measurement.date)
.group_by (Measurement.date)
.order_by(Measurement.date.desc())
.first())
last_year=list(np.ravel(last_year))[0]
last_year= dt.datetime.strptime(last_year, '%Y-%m-%d')
year=int(dt.datetime.strftime(last_year, '%y'))
month=int(dt.datetime.strftime(last_year, '%m'))
day=int(dt.datetime.strftime(last_year, '%d'))
year_prior= dt.date(year,month,day)-dt.timedelta(days=365)
#Flask Route
@app.route("/") 
def welcome():
    return(
        f"Welcome to my Surfs Up page: Haiwai's climate <br/>"
        f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>"
        f"Available routes<br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/temperature <br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date <br/>"
    )

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    result = session.query(station.name).all()
    all_stations=list(np.ravel(result))
    session.close()
    return jsonify(all_stations)
    
@app.route("/api/v1.0/precipitation") 
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results=(session.query(Measurement.prcp, Measurement.date, Measurement.station)
    .filter(Measurement.date > year_prior)
    .order_by(Measurement.date).all())
    
    session.close()
    
    
    all_precipitation= []
  
    for result in results:
        prpc_Dict = {result.date: result.prcp, "Station": result.station}
        all_precipitation.append( prpc_Dict)

    return jsonify( all_precipitation)
@app.route("/api/v1.0/temperature")
def temperature():
 # Create our session (link) from Python to the DB
    session = Session(engine)

    results = (session.query(Measurement.date, Measurement.tobs)
    .filter(Measurement.date > year_prior)
    .order_by(Measurement.date)
    .all())
    session.close()
    
                   

    all_temperature = []
    for result in results:
        Dict = {result.date: result.tobs}
        all_temperature.append(Dict)

    return jsonify(all_temperature)


@app.route("/api/v1.0/start_date")
def start_date():
# Create our session (link) from Python to the DB
    session = Session(engine)

    sel=[Measurement.date, func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs) ]
    results= session.query(*sel).filter(Measurement.date >= "2015-09-05").order_by(Measurement.date).all()
    session.close()
    
    StartDate=[]
    for result in results: 
        dict_start={}
        dict_start["date"]=result[0]
        dict_start["min temp"]=result[1]
        dict_start["avg temp"]=result[2]
        dict_start["max temp"]=result[3]
        StartDate.append(result)
    return jsonify(StartDate)
@app.route("/api/v1.0/start_date/end_date")
def start_end():
# Create our session (link) from Python to the DB
    session = Session(engine)

    sel=[Measurement.date, func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs) ]
    results= session.query(*sel).filter(Measurement.date >= "2015-09-05").filter(Measurement.date <=last_year).order_by(Measurement.date).all()
    session.close()
    
    Startend=[]
    for result in results: 
        dict_startend={}
        dict_startend["date"]=result[0]
        dict_startend["min temp"]=result[1]
        dict_startend["avg temp"]=result[2]
        dict_startend["max temp"]=result[3]
        Startend.append(result)
    return jsonify(Startend)

if __name__ == '__main__':
    app.run(debug=True)


