from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)
# connection string is in the format mysql://user:password@server/database
conn_str = 'mysql://root:cset155@localhost/boatdb'
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/boats')
def boats():
    boats = conn.execute(text('SELECT * FROM boats')).all()
    return render_template('boats.html', boats=boats)

@app.route('/boat-create', methods=['GET'])
def get_boat():
    return render_template('boat_create.html')

@app.route('/boat-create', methods=['POST'])
def create_boat():
    try:
        conn.execute(text('INSERT INTO boats VALUES(:id, :name, :type, :owner_id, :rental_price)'), request.form)
        return render_template('boat_create.html', error=None, sucess='Successful')
    except:
        return render_template('boat_create.html', error='Failed', sucess=None)
    
@app.route('/boat-search', methods=['GET'])
def get_boat_search():
    boats = []
    return render_template('boat_search.html', boats = boats)

@app.route('/boat-search', methods=['POST'])
def find_boat_search():
    try:
        boats = conn.execute(text('SELECT * FROM boats WHERE id = :id'), request.form).all()
        return render_template('boat_search.html', boats=boats, error=None, sucess='Sucess')
    except:
        return render_template('boat_search.html', boats=boats, error='Falied', sucess=None)
    
@app.route('/boat-delete', methods=['GET'])
def get_boat_delete():
    return render_template('boat_delete.html')

@app.route('/boat-delete', methods=['POST'])
def delete_boat():
    boat_id = request.form.get("id") 

    try: 
        with engine.connect() as conn:
            result = conn.execute(text("DELETE FROM boats WHERE id = :id"), {"id": boat_id})
            conn.commit()  

        if result.rowcount > 0:
            return render_template("boat_delete.html", result=f"Boat ID {boat_id} successfully deleted.")
        else:
            return render_template("boat_delete.html", error=f"Boat ID {boat_id} not found.")
    except:
        if result.rowcount > 0:
            return render_template("boat_delete.html", result=f"Boat ID {boat_id} successfully deleted.")
        else:
            return render_template("boat_delete.html", error=f"Boat ID {boat_id} not found.")

# Should always be last 2 lines of code
if __name__ == '__main__': # Checks to make sure the file that the code is ran on is the Flask main
    app.run(debug=True) # Runs the application and debug gives live updates when you change your code