from datetime import datetime, timedelta




def lastfriday():
    n = datetime.now()
    f =  n - timedelta(days=n.weekday()) + timedelta(days=4, weeks=-1)
    return ("{}-{}-{}T12:00:00Z".format(f.year,f.month,f.day))
