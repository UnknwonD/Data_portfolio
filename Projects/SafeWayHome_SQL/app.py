from flask import Flask, render_template, request, jsonify
from decimal import Decimal
import psycopg2
import json

app = Flask(__name__)
radius_km = 0.5
# 37.557481 126.971763
# 37.569610 126.931485
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_function', methods=['POST'])
def execute_function():
    try:
        data = request.get_json()

        # 가져온 데이터에서 필요한 값 추출
        start = data.get('arg1').split()
        dest = data.get('arg2').split()

        current_latitude = start[0]
        current_longitude = start[1]
        destination_latitude = dest[0]
        destination_longitude = dest[1]

        try:
            conn = psycopg2.connect(
                host="host",
                port="5432",
                user="postgres",
                password="mypassword",
                database="safehome"
            )
            
            with conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT c_id, cctv.latitude, cctv.longitude, l_id, street_lamp.latitude as l_latitude, street_lamp.longitude as l_longitude FROM cctv JOIN street_lamp ON ABS(cctv.latitude - street_lamp.latitude) <= 0.003 AND ABS(cctv.longitude - street_lamp.longitude) <= 0.003 WHERE cctv.latitude BETWEEN {current_latitude} AND {destination_latitude} AND cctv.longitude BETWEEN {current_longitude} AND {destination_longitude};")
                cursor.execute(f"insert into saferoot value({destination_latitude}, {destination_longitude}, {current_latitude}, {current_longitude});")
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

            json_results = []
            for row in results:
                json_row = {key: float(value) if isinstance(value, Decimal) else value for key, value in zip(columns, row)}
                json_results.append(json_row)
            json_output = json.dumps(json_results, indent=2)
            
            # 반환할 데이터를 JSON 형식으로 응답
            return json_output
        
        except Exception as e:
            # 예외가 발생하면 500 Internal Server Error 반환
            return jsonify({'error': str(e)}), 500
    except psycopg2.Error as e:
        print("Connection failure.")
        raise e
    
@app.route('/cctv', methods=['POST'])
def process():
    try:
        data = request.get_json()

        # 가져온 데이터에서 필요한 값 추출
        start = data.get('arg1').split()

        current_latitude = start[0]
        current_longitude = start[1]

        try:
            conn = psycopg2.connect(
                host="host",
                port="5432",
                user="postgres",
                password="mypassword",
                database="safehome"
            )
            with conn:
                cursor = conn.cursor()
                cursor.execute(f'''SELECT c_id as id, cctv.latitude as latitude, cctv.longitude as longitude
                            FROM cctv
                            WHERE (
                                6371 * ACOS(COS(RADIANS({current_latitude})) * COS(RADIANS(cctv.latitude))
                                        * COS(RADIANS(cctv.longitude) - RADIANS({current_longitude}))
                                        + SIN(RADIANS({current_latitude})) * SIN(RADIANS(cctv.latitude)))
                            ) <= {radius_km}
                            ''')
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

            json_results = []
            for row in results:
                json_row = {key: float(value) if isinstance(value, Decimal) else value for key, value in zip(columns, row)}
                json_results.append(json_row)
            json_output = json.dumps(json_results, indent=2)
            
            # 반환할 데이터를 JSON 형식으로 응답
            return json_output
        
        except Exception as e:
            # 예외가 발생하면 500 Internal Server Error 반환
            return jsonify({'error': str(e)}), 500
    except psycopg2.Error as e:
        print("Connection failure.")
        raise e
    
@app.route('/lamp', methods=['POST'])
def process_lamp():
    try:
        data = request.get_json()

        # 가져온 데이터에서 필요한 값 추출
        start = data.get('arg1').split()

        current_latitude = start[0]
        current_longitude = start[1]

        try:
            conn = psycopg2.connect(
                host="host",
                port="5432",
                user="postgres",
                password="mypassword",
                database="safehome"
            )
            
            with conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                            SELECT l_id as id, street_lamp.latitude as latitude, street_lamp.longitude as longitude
                            FROM street_lamp
                            WHERE (
                                6371 * ACOS(COS(RADIANS({current_latitude})) * COS(RADIANS(street_lamp.latitude))
                                        * COS(RADIANS(street_lamp.longitude) - RADIANS({current_longitude}))
                                        + SIN(RADIANS({current_latitude})) * SIN(RADIANS(street_lamp.latitude)))
                            ) <= {radius_km};
                            ''')
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

            json_results = []
            for row in results:
                json_row = {key: float(value) if isinstance(value, Decimal) else value for key, value in zip(columns, row)}
                json_results.append(json_row)
            json_output = json.dumps(json_results, indent=2)
            
            # 반환할 데이터를 JSON 형식으로 응답
            return json_output
        
        except Exception as e:
            # 예외가 발생하면 500 Internal Server Error 반환
            return jsonify({'error': str(e)}), 500
    except psycopg2.Error as e:
        print("Connection failure.")
        raise e
    
@app.route('/bell', methods=['POST'])
def process_warn():
    try:
        data = request.get_json()

        # 가져온 데이터에서 필요한 값 추출
        start = data.get('arg1').split()

        current_latitude = start[0]
        current_longitude = start[1]

        try:
            conn = psycopg2.connect(
                host="host",
                port="5432",
                user="postgres",
                password="mypassword",
                database="safehome"
            )
            
            with conn:
                cursor = conn.cursor()
                cursor.execute(f'''SELECT
                                b_id,
                                latitude,
                                longitude,
                                sqrt(
                                    ((latitude - {current_latitude}) * (latitude - {current_latitude})) +
                                    ((longitude - {current_longitude}) * (longitude - {current_longitude}))
                                ) AS distance
                                FROM
                                    safety_bell
                                ORDER BY
                                    distance
                                LIMIT 1;
                            ''')
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

            json_results = []
            for row in results:
                json_row = {key: float(value) if isinstance(value, Decimal) else value for key, value in zip(columns, row)}
                json_results.append(json_row)
            json_output = json.dumps(json_results, indent=2)
            
            # 반환할 데이터를 JSON 형식으로 응답
            return json_output
        
        except Exception as e:
            # 예외가 발생하면 500 Internal Server Error 반환
            return jsonify({'error': str(e)}), 500
    except psycopg2.Error as e:
        print("Connection failure.")
        raise e


if __name__ == '__main__':
    app.run(debug=True)
