from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import psycopg2

app = Flask(__name__)

# Configure PostgreSQL connection parameters
DB_NAME = 'myntra'
DB_USER = 'postgres'
DB_PASSWORD = 'abc@123'
DB_HOST = 'localhost'  # Change this if your database is hosted on a different server
DB_PORT = '5432'  # Default PostgreSQL port

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

@app.route('/')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']

        # Check if email and password exist in database
        conn = connect_to_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM registration WHERE email = %s AND password = %s", (email, password))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                # User found, redirect to dashboard
                return redirect(url_for('home'))
            else:
                # User not found, render login page with error message
                return render_template('login.html', error="Invalid email or password. Please try again.")
        else:
            # Render login page with error message
            return render_template('login.html', error="Unable to connect to the database. Please try again later.")

    # Render login form
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get form data
            email = request.form['email']
            password = request.form['password']

            # Insert data into database
            conn = connect_to_db()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("INSERT INTO registration (email, password) VALUES (%s, %s)", (email, password))
                    conn.commit()
                    cur.close()
                    conn.close()
                    # Redirect to login page after registration
                    return redirect(url_for('login'))
                except psycopg2.Error as e:
                    print("Error inserting data into the database:", e)
                    conn.rollback()
                    cur.close()
                    conn.close()
                    # Render registration form with error message
                    return render_template('register.html', error="An error occurred during registration. Please try again.")
            else:
                # Render registration form with error message
                return render_template('register.html', error="Unable to connect to the database. Please try again later.")
        except KeyError as e:
            print("KeyError: ", e)
            # Render registration form with error message
            return render_template('register.html', error="Form data is incomplete. Please fill all fields.")

    # Render registration form
    return render_template('register.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Get form data
            firstname = request.form['fname']  # Corrected to match the HTML field name
            lastname = request.form['lname']  # Corrected to match the HTML field name
            country = request.form['country']
            subject = request.form['subject']

            # Insert data into database
            conn = connect_to_db()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("INSERT INTO contactus (firstname, lastname, country, subject) VALUES (%s, %s, %s, %s)",
                                (firstname, lastname, country, subject))
                    conn.commit()
                    cur.close()
                    conn.close()
                    
                    # Redirect to a confirmation page or render a success message
                    return render_template('login.html')
                except psycopg2.Error as e:
                    print("Error inserting data into the database:", e)
                    conn.rollback()
                    cur.close()
                    conn.close()
                    
                    return render_template('contact.html', error="An error occurred while submitting your message. Please try again.")
            else:
                # Render contact form with error message
                return render_template('contact.html', error="Unable to connect to the database. Please try again later.")
        except KeyError as e:
            print("KeyError: ", e)
            # Render contact form with error message
            return render_template('contact.html', error="Form data is incomplete. Please fill all fields.")

    # Render contact form
    return render_template('contact.html')

@app.route('/address', methods=['GET', 'POST'])
def address():
    if request.method == 'POST':
        try:
            # Get form data
            fullname = request.form['fullname']
            address = request.form['address']
            city = request.form['city']
            zipcode = request.form['zipcode']
            country = request.form['country']

            # Insert data into database
            conn = connect_to_db()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("INSERT INTO address (fullname, address, city, zipcode, country) VALUES (%s, %s, %s, %s, %s)",
                                (fullname, address, city, zipcode, country))
                    conn.commit()
                    cur.close()
                    conn.close()
                    # Redirect to success page after address submission
                    return redirect(url_for('order_success'))
                except psycopg2.Error as e:
                    print("Error inserting data into the database:", e)
                    conn.rollback()
                    cur.close()
                    conn.close()
                    # Render address form with error message
                    return render_template('address.html', error="An error occurred while submitting your address. Please try again.")
            else:
                # Render address form with error message
                return render_template('address.html', error="Unable to connect to the database. Please try again later.")
        except KeyError as e:
            print("KeyError: ", e)
            # Render address form with error message
            return render_template('address.html', error="Form data is incomplete. Please fill all fields.")

    # Render address form
    return render_template('address.html')



@app.route('/order_success')
def order_success():
    return render_template('order_success.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/men')
def men():
    return render_template('men.html')

@app.route('/women')
def women():
    return render_template('women.html')
@app.route('/kids')
def kids():
    return render_template('kids.html')

@app.route('/cart')
def cart_page():
    return render_template('cart.html')





if __name__ == '__main__':
    app.run(debug=True)
