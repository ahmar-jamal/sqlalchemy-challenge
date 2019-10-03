import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import jsonify, Flask

####################
## Database Setup ##
####################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement=Base.classes.measurement
Station=Base.classes.station

######################

app = Flask(__name__)

#################
## Flask Routes
#################

@app.route("/")
def welcome():
    ## List all available Api routes
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    sess = Session(engine)
    p_results=sess.query(Measurement.date, Measurement.prcp).all()
    
    sess.close()

    p_arr = []

    for date, prcp in p_results:
        p_dict = {}
        p_dict = {date:prcp}

        p_arr.append(p_dict)

    return jsonify(p_arr)

@app.route("/api/v1.0/stations")
def stations():
    sess = Session(engine)
    s_results=sess.query(Station.station).all()

    sess.close()

    return jsonify(s_results)

@app.route("/api/v1.0/tobs")
def tobs():

    sess = Session(engine)

    last_date = sess.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = last_date[0]

    breakup = max_date.split('-')
    year_ = int(breakup[0])
    month_ = int(breakup[1])
    day_ = int(breakup[2])

    from dateutil.relativedelta import relativedelta

    date_point = dt.date(year_, month_, day_) - relativedelta(months=12)


    last_year_tobs=sess.query(Measurement.tobs).filter(Measurement.date >= date_point).all()

    sess.close()

    return jsonify(last_year_tobs)

@app.route("/api/v1.0/<start_date>")
def st_date(start_date):

    sess = Session(engine)

    vals = sess.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    sess.close()

    return jsonify(vals)

@app.route("/api/v1.0/<start_date>/<end_date>")
def st_end_date(start_date, end_date):

    sess = Session(engine)

    vals = sess.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    sess.close()

    return jsonify(vals)










if __name__ == '__main__':
    app.run(debug=True)
