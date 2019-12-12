from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask('__name', template_folder='templates')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'api'
app.config['MYSQL_PASSWORD'] = 'Bjit@1243'
app.config['MYSQL_DB'] = 'api'

db = MySQL(app)


@app.route('/index')
def index():
    return render_template('api.html')


@app.route('/create_new_user', methods=['POST'])
def create_new_user():
    columns = ['username', 'password']
    username = request.form.get('username')
    password = request.form.get('password')
    con = db.connection.cursor()
    sql_query = f'insert into user({columns[0]}, {columns[1]}) values("{username}","{password}");'
    con.execute(sql_query)
    db.connection.commit()
    con.close()
    return "new user created"


# get all users
@app.route('/get_data', methods=['GET'])
def get_data():
    data = db.connection.cursor()
    data.execute('select * from user')
    result = data.fetchall()
    [print(r) for r in result]
    dictionary = {"result": result}
    return jsonify(dictionary)

# delete user by username
@app.route('/delete_user/<string:name>', methods=['DELETE'])
def delete_a_user(name):
    sql_query = f'delete from user where username="{name}"'
    db.connection.cursor().execute(sql_query)
    db.connection.commit()
    return "user deleted"

# send data in json format
@app.route('/post_json', methods=['POST'])
def post_data_in_json():
    data = []
    username = request.json['username']
    password = request.json['password']
    data.append(username)
    data.append(password)
    columns = ['username', 'password']
    sql_query = 'insert into user({col1}, {col2}) values("{username}","{password}");'.format(
            col1=columns[0],
            col2=columns[1],
            username=username,
            password=password)
    db.connection.cursor().execute(sql_query)
    db.connection.commit()
    return "posted data as json"


@app.route('/update_user/<slug>', methods=['PUT'])
def update_user(slug):
    columns = ['username', 'password']
    # username = request.json['username']
    # password = request.json['password']
    username = request.form.get('username')
    password = request.form.get('password')
    sql = f'update user set {columns[0]}="{username}", {columns[1]}="{password}" where id={slug};'
    db.connection.cursor().execute(sql)
    db.connection.commit()
    return f"data updated for user for id {slug}"


# get data by passing query with the url
@app.route('/get_data_by_query', methods=['GET'])
def get_data_by_query():
    username = request.args.get('username')
    sql = f'select * from user where username="{username}";'
    data = db.connection.cursor()
    data.execute(sql)
    result = data.fetchall()
    print(result)
    for r in result:
        print(r)
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)
