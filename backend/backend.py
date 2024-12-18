import flask
from flask import Flask, jsonify
import sqlite3
from typing import List, Tuple
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
db = SQLAlchemy(app)
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

# Needed for CORS
@app.route("/cpu/info", methods=["OPTIONS"])
@app.route("/ram/info", methods=["OPTIONS"])
@app.route("/motherboard/info", methods=["OPTIONS"])
@app.route("/psu/info", methods=["OPTIONS"])
@app.route("/storage/info", methods=["OPTIONS"])
@app.route("/gpu/info", methods=["OPTIONS"])
@app.route("/cooler/info", methods=["OPTIONS"])
@app.route("/filter/brand", methods=["OPTIONS"])
@app.route("/filter/socket", methods=["OPTIONS"])
@app.route("/filter/pciegen", methods=["OPTIONS"])
@app.route("/filter/ddrgen", methods=["OPTIONS"])
@app.route("/filter/efficiency", methods=["OPTIONS"])
@app.route("/filter/chipset", methods=["OPTIONS"])
@app.route("/filter/storageinterface", methods=["OPTIONS"])
@app.route("/filter/cpu", methods=["OPTIONS"])
@app.route("/filter/ram", methods=["OPTIONS"])
@app.route("/filter/motherboard", methods=["OPTIONS"])
@app.route("/filter/psu", methods=["OPTIONS"])
@app.route("/filter/gpu", methods=["OPTIONS"])
@app.route("/filter/storage", methods=["OPTIONS"])
@app.route("/filter/cooler", methods=["OPTIONS"])
@app.route("/compatability", methods=["OPTIONS"])
def preflight():
    response = flask.make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


def createTables():
    with open("createTables.sql", "r") as file:
        script = file.read()
        statements = script.split(";")
    with engine.connect() as conn:
        for statement in statements:
            # statement = statement.strip()
            conn.execute(text(statement))
        conn.commit()


def loadData():
    with open("loadData.sql", "r") as file:
        script = file.read()
        statements = script.split(";")
    with engine.connect() as conn:
        for statement in statements:
            # statement = statement.strip()
            conn.execute(text(statement))
        conn.commit()


@app.route("/cpu/info", methods=["GET"])
def getCpuInfo():
    cpuid = flask.request.args.get("cpuid")
    if cpuid == None:
        response = flask.jsonify({"error": "No cpuid provided"})
        response.status_code = 400
        return response
    with engine.connect() as conn:
        query = """
            SELECT cpu.*, brand.name AS brand, socket.name AS socket,
                GROUP_CONCAT(ddrgen.name, ',') AS ddrgen
            FROM cpu
            JOIN brand ON cpu.brandid = brand.brandid
            JOIN socket on cpu.socketid = socket.socketid
            JOIN cpu_ddrgen ON cpu.cpuid = cpu_ddrgen.cpuid
            JOIN ddrgen ON cpu_ddrgen.ddrgenid = ddrgen.ddrgenid
            WHERE cpu.cpuid = ?
        """
        data = conn.exec_driver_sql(query, (cpuid,)).mappings().fetchone()
        if data == None:
            response = flask.jsonify({"error": "Invalid cpuid"})
            response.status_code = 404
            return response
    jsonData = {}
    for col, val in data.items():
        if col == "ddrgen":
            jsonData[col] = val.split(",")
        else:
            jsonData[col] = val
    response = flask.make_response(jsonData)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/cpu/info", methods=["POST"])
def addCpuInfo():
    body = flask.request.get_json()
    rows = {
        "price": body["price"],
        "model": body["model"],
        "speed": body["speed"],
        "boostspeed": body["boostspeed"],
        "cores": body["cores"],
        "threads": body["threads"],
        "tdp": body["tdp"],
        "wattage": body["wattage"],
        "hasgraphics": body["hasgraphics"],
        "hascooler": body["hascooler"],
    }
    ddrgens = body["ddrgen"]
    cpuid = body.get("cpuid", None)
    if cpuid != None:
        rows["cpuid"] = cpuid
    
    with engine.connect() as conn:
        query = f"SELECT brandid FROM brand WHERE name LIKE '{body['brand']}'"
        rows["brandid"] = conn.exec_driver_sql(query).fetchone()[0]
        query = f"SELECT socketid FROM socket WHERE name LIKE '{body['socket']}'"
        rows["socketid"] = conn.exec_driver_sql(query).fetchone()[0]

        for key, value in rows.items():
            if type(value) == str:
                rows[key] = f"'{value}'"
        query = f"""
            INSERT OR IGNORE INTO cpu ({", ".join(rows.keys())}) VALUES ({", ".join(map(str,rows.values()))})
        """
        conn.exec_driver_sql(query)

        if cpuid == None:
            query = "SELECT last_insert_rowid() AS LastInsertedID;"
            cpuid = conn.exec_driver_sql(query).fetchone()[0]

        for ddrgen in ddrgens:
            query = f"SELECT ddrgenid FROM ddrgen WHERE name LIKE '{ddrgen}'"
            ddrgenid = conn.exec_driver_sql(query).fetchone()[0]
            query = f"INSERT INTO cpu_ddrgen (cpuid, ddrgenid) VALUES ({cpuid}, {ddrgenid})"
            conn.exec_driver_sql(query)
        conn.commit()

    response = flask.make_response({"cpuid": cpuid})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/cpu/info", methods=["PUT"])
def updateCpuInfo():
    body = flask.request.get_json()
    cpuid = body["cpuid"]
    with app.test_client() as client:
        response = client.delete(f"http://localhost:5000/cpu/info?cpuid={cpuid}").json
        for col, val in body.items():
            response[col] = val
        response["cpuid"] = cpuid
        client.post(f"http://localhost:5000/cpu/info", json=response)

    response = flask.make_response(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/cpu/info", methods=["DELETE"])
def deleteCpuInfo():
    cpuid = flask.request.args.get("cpuid")
    with app.test_client() as client:
        response = client.get(f"http://localhost:5000/cpu/info?cpuid={cpuid}")
    with engine.connect() as conn:
        query = f"DELETE FROM cpu WHERE cpuid = {cpuid}"
        conn.exec_driver_sql(query)
        query = f"DELETE FROM cpu_ddrgen WHERE cpuid = {cpuid}"
        conn.exec_driver_sql(query)
        conn.commit()
    response = flask.make_response(response.json)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@app.route("/ram/info", methods=["GET"])
def getRamInfo():
    ramid = flask.request.args.get("ramid")
    if ramid == None:
        response = flask.jsonify({"error": "No ramid provided"})
        response.status_code = 400
        return response
    with engine.connect() as conn:
        query = """
            SELECT ram.*, brand.name AS brand, ddrgen.name AS ddrgen
            FROM ram
            JOIN brand ON ram.brandid = brand.brandid
            JOIN ddrgen ON ram.ddrgenid = ddrgen.ddrgenid
            WHERE ram.ramid = ?
        """
        data = conn.exec_driver_sql(query, (ramid,)).mappings().fetchone()
        if data == None:
            response = flask.jsonify({"error": "Invalid ramid"})
            response.status_code = 404
            return response

    jsonData = {}
    for col, val in data.items():
        jsonData[col] = val
    response = flask.make_response(jsonData)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/ram/info", methods=["POST"])
def addRamInfo():
    body = flask.request.get_json()
    rows = {
        "price": body["price"],
        "model": body["model"],
        "size": body["size"],
        "speed": body["speed"],
        "latency": body["latency"]
    }
    ramid = body.get("ramid", None)
    if ramid != None:
        rows["ramid"] = ramid
    
    with engine.connect() as conn:
        query = f"SELECT brandid FROM brand WHERE name LIKE '{body['brand']}'"
        rows["brandid"] = conn.exec_driver_sql(query).fetchone()[0]
        query = f"SELECT ddrgenid FROM ddrgen WHERE name LIKE '{body['ddrgen']}'"
        rows["ddrgenid"] = conn.exec_driver_sql(query).fetchone()[0]

        for key, value in rows.items():
            if type(value) == str:
                rows[key] = f"'{value}'"
        query = f"""
            INSERT OR IGNORE INTO ram ({", ".join(rows.keys())}) VALUES ({", ".join(map(str,rows.values()))})
        """
        conn.exec_driver_sql(query)

        if ramid == None:
            query = "SELECT last_insert_rowid() AS LastInsertedID;"
            ramid = conn.exec_driver_sql(query).fetchone()[0]

        conn.commit()

    response = flask.make_response({"ramid": ramid})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/ram/info", methods=["PUT"])
def updateRamInfo():
    body = flask.request.get_json()
    ramid = body["ramid"]
    with app.test_client() as client:
        response = client.delete(f"http://localhost:5000/ram/info?ramid={ramid}").json
        for col, val in body.items():
            response[col] = val
        response["ramid"] = ramid
        client.post(f"http://localhost:5000/ram/info", json=response)

    response = flask.make_response(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/ram/info", methods=["DELETE"])
def deleteRamInfo():
    ramid = flask.request.args.get("ramid")
    with app.test_client() as client:
        response = client.get(f"http://localhost:5000/ram/info?ramid={ramid}")
    with engine.connect() as conn:
        query = f"DELETE FROM ram WHERE ramid = {ramid}"
        conn.exec_driver_sql(query)
        conn.commit()
    response = flask.make_response(response.json)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@app.route("/motherboard/info", methods=["GET"])
def getMotherboardInfo():
    motherboardid = flask.request.args.get("motherboardid")
    if motherboardid == None:
        response = flask.jsonify({"error": "No motherboardid provided"})
        response.status_code = 400
        return response
    with engine.connect() as conn:
        query = """
            SELECT motherboard.*, brand.name AS brand, ddrgen.name AS ddrgen, socket.name AS socket,
                pciegen.name AS pciegen, GROUP_CONCAT(storage_interface.name, ',') AS storageinterface
            FROM motherboard
            JOIN brand ON motherboard.brandid = brand.brandid
            JOIN ddrgen ON motherboard.ddrgenid = ddrgen.ddrgenid
            JOIN pciegen ON motherboard.pciegenid = pciegen.pciegenid
            JOIN socket ON motherboard.socketid = socket.socketid
            JOIN motherboard_storage_interface ON motherboard.motherboardid = motherboard_storage_interface.motherboardid
            JOIN storage_interface ON motherboard_storage_interface.storageinterfaceid = storage_interface.storageinterfaceid
            WHERE motherboard.motherboardid = ?
        """
        data = conn.exec_driver_sql(query, (motherboardid,)).mappings().fetchone()
        if data == None:
            response = flask.jsonify({"error": "Invalid motherboardid"})
            response.status_code = 404
            return response

    jsonData = {}
    for col, val in data.items():
        if col == "storageinterface":
            jsonData[col] = val.split(",")
        else:
            jsonData[col] = val
    response = flask.make_response(jsonData)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/motherboard/info", methods=["POST"])
def addMotherboardInfo():
    body = flask.request.get_json()
    rows = {
        "price": body["price"],
        "model": body["model"],
        "ramspeed": body["ramspeed"],
        "usbcount": body["usbcount"],
        "formfactor": body["formfactor"],
        "chipset": body["chipset"],
    }
    storageinterface = body["storageinterface"]
    motherboardid = body.get("motherboardid", None)
    if motherboardid != None:
        rows["motherboardid"] = motherboardid
    
    with engine.connect() as conn:
        query = f"SELECT brandid FROM brand WHERE name LIKE '{body['brand']}'"
        rows["brandid"] = conn.exec_driver_sql(query).fetchone()[0]
        query = f"SELECT socketid FROM socket WHERE name LIKE '{body['socket']}'"
        rows["socketid"] = conn.exec_driver_sql(query).fetchone()[0]
        query = f"SELECT pciegenid FROM pciegen WHERE name LIKE '{body['pciegen']}'"
        rows["pciegenid"] = conn.exec_driver_sql(query).fetchone()[0]
        query = f"SELECT ddrgenid FROM ddrgen WHERE name LIKE '{body['ddrgen']}'"
        rows["ddrgenid"] = conn.exec_driver_sql(query).fetchone()[0]

        for key, value in rows.items():
            if type(value) == str:
                rows[key] = f"'{value}'"
        query = f"""
            INSERT OR IGNORE INTO motherboard ({", ".join(rows.keys())}) VALUES ({", ".join(map(str,rows.values()))})
        """
        conn.exec_driver_sql(query)

        if motherboardid == None:
            query = "SELECT last_insert_rowid() AS LastInsertedID;"
            motherboardid = conn.exec_driver_sql(query).fetchone()[0]

        for interface in storageinterface:
            query = f"SELECT storageinterfaceid FROM storage_interface WHERE name LIKE '{interface}'"
            storageinterfaceid = conn.exec_driver_sql(query).fetchone()[0]
            query = f"INSERT INTO motherboard_storage_interface (motherboardid, storageinterfaceid) VALUES ({motherboardid}, {storageinterfaceid})"
            conn.exec_driver_sql(query)
        conn.commit()

    response = flask.make_response({"motherboardid": motherboardid})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/motherboard/info", methods=["PUT"])
def updateMotherboardInfo():
    body = flask.request.get_json()
    motherboardid = body["motherboardid"]
    with app.test_client() as client:
        response = client.delete(f"http://localhost:5000/motherboard/info?motherboardid={motherboardid}").json
        for col, val in body.items():
            response[col] = val
        response["motherboard"] = motherboardid
        client.post(f"http://localhost:5000/motherboard/info", json=response)

    response = flask.make_response(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/motherboard/info", methods=["DELETE"])
def deleteMotherboardInfo():
    motherboardid = flask.request.args.get("motherboardid")
    with app.test_client() as client:
        response = client.get(f"http://localhost:5000/motherboard/info?motherboardid={motherboardid}")
    with engine.connect() as conn:
        query = f"DELETE FROM motherboard WHERE motherboardid = {motherboardid}"
        conn.exec_driver_sql(query)
        query = f"DELETE FROM motherboard_storage_interface WHERE motherboardid = {motherboardid}"
        conn.exec_driver_sql(query)
        conn.commit()
    response = flask.make_response(response.json)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/psu/info", methods=["GET"])
def getPsuInfo():
    psuid = flask.request.args.get("psuid")
    if psuid == None:
        response = flask.jsonify({"error": "No psuid provided"})
        response.status_code = 400
        return response
    with engine.connect() as conn:
        query = """
            SELECT psu.*, brand.name AS brand, efficiency.name AS efficiency
            FROM psu
            JOIN brand ON psu.brandid = brand.brandid
            JOIN efficiency ON efficiency.efficiencyid = psu.efficiencyid
            WHERE psu.psuid = ?
        """
        data = conn.exec_driver_sql(query, (psuid,)).mappings().fetchone()
        if data == None:
            response = flask.jsonify({"error": "Invalid psuid"})
            response.status_code = 404
            return response

    jsonData = {}
    for col, val in data.items():
        jsonData[col] = val
    response = flask.make_response(jsonData)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/psu/info", methods=["POST"])
def addPsuInfo():
    body = flask.request.get_json()
    rows = {
        "price": body["price"],
        "model": body["model"],
        "wattage": body["wattage"],
    }
    psuid = body.get("psuid", None)
    if psuid != None:
        rows["psuid"] = psuid
    
    with engine.connect() as conn:
        query = f"SELECT brandid FROM brand WHERE name LIKE '{body['brand']}'"
        rows["brandid"] = conn.exec_driver_sql(query).fetchone()[0]
        query = f"SELECT efficiencyid FROM efficiency WHERE name LIKE '{body['efficiency']}'"
        rows["efficiencyid"] = conn.exec_driver_sql(query).fetchone()[0]

        for key, value in rows.items():
            if type(value) == str:
                rows[key] = f"'{value}'"
        query = f"""
            INSERT OR IGNORE INTO psu ({", ".join(rows.keys())}) VALUES ({", ".join(map(str,rows.values()))})
        """
        conn.exec_driver_sql(query)

        if psuid == None:
            query = "SELECT last_insert_rowid() AS LastInsertedID;"
            psuid = conn.exec_driver_sql(query).fetchone()[0]

        conn.commit()

    response = flask.make_response({"psuid": psuid})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/psu/info", methods=["PUT"])
def updatePsuInfo():
    body = flask.request.get_json()
    psuid = body["psuid"]
    with app.test_client() as client:
        response = client.delete(f"http://localhost:5000/psu/info?psuid={psuid}").json
        for col, val in body.items():
            response[col] = val
        response["psuid"] = psuid
        client.post(f"http://localhost:5000/psu/info", json=response)

    response = flask.make_response(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/psu/info", methods=["DELETE"])
def deletePsuInfo():
    psuid = flask.request.args.get("psuid")
    with app.test_client() as client:
        response = client.get(f"http://localhost:5000/psu/info?psuid={psuid}")
    with engine.connect() as conn:
        query = f"DELETE FROM psu WHERE psuid = {psuid}"
        conn.exec_driver_sql(query)
        conn.commit()
    response = flask.make_response(response.json)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/gpu/info", methods=["GET"])
def getGpuInfo():
    gpuid = flask.request.args.get("gpuid")
    if gpuid == None:
        response = flask.jsonify({"error": "No gpuid provided"})
        response.status_code = 400
        return response
    with engine.connect() as conn:
        query = """
            SELECT gpu.*, brand.name AS brand, pciegen.name AS pciegen, chipset.name AS chipset
            FROM gpu
            JOIN brand ON gpu.brandid = brand.brandid
            JOIN pciegen ON gpu.pciegenid = pciegen.pciegenid
            JOIN chipset ON gpu.chipsetid = chipset.chipsetid
            WHERE gpu.gpuid = ?
        """
        data = conn.exec_driver_sql(query, (gpuid,)).mappings().fetchone()
        if data == None:
            response = flask.jsonify({"error": "Invalid gpuid"})
            response.status_code = 404
            return response

    jsonData = {}
    for col, val in data.items():
        jsonData[col] = val
    response = flask.make_response(jsonData)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/gpu/info", methods=["POST"])
def addGpuInfo():
    body = flask.request.get_json()
    rows = {
        "price": body["price"],
        "model": body["model"],
        "memory": body["memory"],
        "speed": body["speed"],
        "boostspeed": body["boostspeed"],
        "hdmicount": body["hdmicount"],
        "displayportcount": body["displayportcount"],
    }
    gpuid = body.get("gpuid", None)
    if gpuid != None:
        rows["gpuid"] = gpuid
    
    with engine.connect() as conn:
        query = f"SELECT brandid FROM brand WHERE name LIKE '{body['brand']}'"
        rows["brandid"] = conn.exec_driver_sql(query).fetchone()[0]
        query = f"SELECT pciegenid FROM pciegen WHERE name LIKE '{body['pciegen']}'"
        rows["pciegenid"] = conn.exec_driver_sql(query).fetchone()[0]
        query = f"SELECT chipsetid FROM chipset WHERE name LIKE '{body['chipset']}'"
        rows["chipsetid"] = conn.exec_driver_sql(query).fetchone()[0]

        for key, value in rows.items():
            if type(value) == str:
                rows[key] = f"'{value}'"
        query = f"""
            INSERT OR IGNORE INTO gpu ({", ".join(rows.keys())}) VALUES ({", ".join(map(str,rows.values()))})
        """
        conn.exec_driver_sql(query)

        if gpuid == None:
            query = "SELECT last_insert_rowid() AS LastInsertedID;"
            gpuid = conn.exec_driver_sql(query).fetchone()[0]

        conn.commit()

    response = flask.make_response({"gpuid": gpuid})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/gpu/info", methods=["PUT"])
def updateGpuInfo():
    body = flask.request.get_json()
    gpuid = body["gpuid"]
    with app.test_client() as client:
        response = client.delete(f"http://localhost:5000/gpu/info?gpuid={gpuid}").json
        for col, val in body.items():
            response[col] = val
        response["gpuid"] = gpuid
        client.post(f"http://localhost:5000/gpu/info", json=response)

    response = flask.make_response(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/gpu/info", methods=["DELETE"])
def deleteGpuInfo():
    gpuid = flask.request.args.get("gpuid")
    with app.test_client() as client:
        response = client.get(f"http://localhost:5000/gpu/info?gpuid={gpuid}")
    with engine.connect() as conn:
        query = f"DELETE FROM gpu WHERE gpuid = {gpuid}"
        conn.exec_driver_sql(query)
        conn.commit()
    response = flask.make_response(response.json)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@app.route("/storage/info", methods=["GET"])
def getStorageInfo():
    storageid = flask.request.args.get("storageid")
    if storageid == None:
        response = flask.jsonify({"error": "No storageid provided"})
        response.status_code = 400
        return response
    with engine.connect() as conn:
        query = """
            SELECT storage.*, brand.name AS brand, storage_interface.name AS storageinterface
            FROM storage
            JOIN brand ON storage.brandid = brand.brandid
            JOIN storage_interface ON storage.storageinterfaceid = storage_interface.storageinterfaceid
            WHERE storage.storageid = ?
        """
        data = conn.exec_driver_sql(query, (storageid,)).mappings().fetchone()
        if data == None:
            response = flask.jsonify({"error": "Invalid storageid"})
            response.status_code = 404
            return response

    jsonData = {}
    for col, val in data.items():
        jsonData[col] = val
    response = flask.make_response(jsonData)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/storage/info", methods=["POST"])
def addStorageInfo():
    body = flask.request.get_json()
    rows = {
        "price": body["price"],
        "model": body["model"],
        "capacity": body["capacity"],
    }
    storageid = body.get("storageid", None)
    if storageid != None:
        rows["storageid"] = storageid
    
    with engine.connect() as conn:
        query = f"SELECT brandid FROM brand WHERE name LIKE '{body['brand']}'"
        rows["brandid"] = conn.exec_driver_sql(query).fetchone()[0]
        query = f"SELECT storageinterfaceid FROM storage_interface WHERE name LIKE '{body['storageinterface']}'"
        rows["storageinterfaceid"] = conn.exec_driver_sql(query).fetchone()[0]

        for key, value in rows.items():
            if type(value) == str:
                rows[key] = f"'{value}'"
        query = f"""
            INSERT OR IGNORE INTO storage ({", ".join(rows.keys())}) VALUES ({", ".join(map(str,rows.values()))})
        """
        conn.exec_driver_sql(query)

        if storageid == None:
            query = "SELECT last_insert_rowid() AS LastInsertedID;"
            storageid = conn.exec_driver_sql(query).fetchone()[0]

        conn.commit()

    response = flask.make_response({"storageid": storageid})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/storage/info", methods=["PUT"])
def updateStorageInfo():
    body = flask.request.get_json()
    storageid = body["storageid"]
    with app.test_client() as client:
        response = client.delete(f"http://localhost:5000/storage/info?storageid={storageid}").json
        for col, val in body.items():
            response[col] = val
        response["storageid"] = storageid
        client.post(f"http://localhost:5000/storage/info", json=response)

    response = flask.make_response(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/storage/info", methods=["DELETE"])
def deleteStorageInfo():
    storageid = flask.request.args.get("storageid")
    with app.test_client() as client:
        response = client.get(f"http://localhost:5000/storage/info?storageid={storageid}")
    with engine.connect() as conn:
        query = f"DELETE FROM storage WHERE storageid = {storageid}"
        conn.exec_driver_sql(query)
        conn.commit()
    response = flask.make_response(response.json)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@app.route("/cooler/info", methods=["GET"])
def getCoolerInfo():
    coolerid = flask.request.args.get("coolerid")
    if coolerid == None:
        response = flask.jsonify({"error": "No coolerid provided"})
        response.status_code = 400
        return response
    with engine.connect() as conn:
        query = """
            SELECT cooler.*, brand.name AS brand, GROUP_CONCAT(socket.name, ',') AS socket
            FROM cooler
            JOIN brand ON cooler.brandid = brand.brandid
            JOIN cooler_socket ON cooler.coolerid = cooler_socket.coolerid
            JOIN socket ON cooler_socket.socketid = socket.socketid
            WHERE cooler.coolerid = ?
        """
        data = conn.exec_driver_sql(query, (coolerid,)).mappings().fetchone()
        if data == None:
            response = flask.jsonify({"error": "Invalid coolerid"})
            response.status_code = 404
            return response

    jsonData = {}
    for col, val in data.items():
        if col == "socket":
            jsonData[col] = val.split(",")
        else:
            jsonData[col] = val
    response = flask.make_response(jsonData)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/cooler/info", methods=["POST"])
def addCoolerInfo():
    body = flask.request.get_json()
    rows = {
        "price": body["price"],
        "model": body["model"],
        "watercooled": body["watercooled"],
    }
    sockets = body["socket"]
    coolerid = body.get("coolerid", None)
    if coolerid != None:
        rows["coolerid"] = coolerid
    
    with engine.connect() as conn:
        query = f"SELECT brandid FROM brand WHERE name LIKE '{body['brand']}'"
        rows["brandid"] = conn.exec_driver_sql(query).fetchone()[0]

        for key, value in rows.items():
            if type(value) == str:
                rows[key] = f"'{value}'"
        query = f"""
            INSERT OR IGNORE INTO cooler ({", ".join(rows.keys())}) VALUES ({", ".join(map(str,rows.values()))})
        """
        conn.exec_driver_sql(query)

        if coolerid == None:
            query = "SELECT last_insert_rowid() AS LastInsertedID;"
            coolerid = conn.exec_driver_sql(query).fetchone()[0]

        for socket in sockets:
            query = f"SELECT socketid FROM socket WHERE name LIKE '{socket}'"
            socketid = conn.exec_driver_sql(query).fetchone()[0]
            query = f"INSERT INTO cooler_socket (coolerid, socketid) VALUES ({coolerid}, {socketid})"
            conn.exec_driver_sql(query)
        conn.commit()

    response = flask.make_response({"coolerid": coolerid})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/cooler/info", methods=["PUT"])
def updateCoolerInfo():
    body = flask.request.get_json()
    coolerid = body["coolerid"]
    with app.test_client() as client:
        response = client.delete(f"http://localhost:5000/cooler/info?coolerid={coolerid}").json
        for col, val in body.items():
            response[col] = val
        response["coolerid"] = coolerid
        client.post(f"http://localhost:5000/cooler/info", json=response)

    response = flask.make_response(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/cooler/info", methods=["DELETE"])
def deleteCoolerInfo():
    coolerid = flask.request.args.get("coolerid")
    with app.test_client() as client:
        response = client.get(f"http://localhost:5000/cooler/info?coolerid={coolerid}")
    with engine.connect() as conn:
        query = f"DELETE FROM cooler WHERE coolerid = {coolerid}"
        conn.exec_driver_sql(query)
        query = f"DELETE FROM cooler_socket WHERE coolerid = {coolerid}"
        conn.exec_driver_sql(query)
        conn.commit()
    response = flask.make_response(response.json)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@app.route("/filter/brand", methods=["GET"])
def getBrand():
    with engine.connect() as conn:
        query = " SELECT brand.name FROM brand"
        result = conn.exec_driver_sql(query).fetchall()
    data = [i[0] for i in result]
    response = flask.make_response(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
@app.route("/filter/socket", methods=["GET"])
def getSocket():
    with engine.connect() as conn:
        query = " SELECT socket.name FROM socket"
        result = conn.exec_driver_sql(query).fetchall()
    data = [i[0] for i in result]
    response = flask.make_response(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
@app.route("/filter/pciegen", methods=["GET"])
def getPciegen():
    with engine.connect() as conn:
        query = " SELECT pciegen.name FROM pciegen"
        result = conn.exec_driver_sql(query).fetchall()
    data = [i[0] for i in result]
    response = flask.make_response(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
@app.route("/filter/ddrgen", methods=["GET"])
def getDdrgen():
    with engine.connect() as conn:
        query = " SELECT ddrgen.name FROM ddrgen"
        result = conn.exec_driver_sql(query).fetchall()
    data = [i[0] for i in result]
    response = flask.make_response(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
@app.route("/filter/efficiency", methods=["GET"])
def getEfficiency():
    with engine.connect() as conn:
        query = " SELECT efficiency.name FROM efficiency"
        result = conn.exec_driver_sql(query).fetchall()
    data = [i[0] for i in result]
    response = flask.make_response(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
@app.route("/filter/chipset", methods=["GET"])
def getChipset():
    with engine.connect() as conn:
        query = " SELECT chipset.name FROM chipset"
        result = conn.exec_driver_sql(query).fetchall()
    data = [i[0] for i in result]
    response = flask.make_response(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
@app.route("/filter/storageinterface", methods=["GET"])
def getStorageinterface():
    with engine.connect() as conn:
        query = " SELECT storage_interface.name FROM storage_interface"
        result = conn.exec_driver_sql(query).fetchall()
    data = [i[0] for i in result]
    response = flask.make_response(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response









@app.route("/filter/cpu", methods=["POST"])
def filterCpu():
    body = flask.request.get_json()
    with engine.connect() as conn:
        query = f"""
            SELECT cpuid FROM cpu
            JOIN brand ON brand.brandid = cpu.brandid
            JOIN socket ON socket.socketid = cpu.socketid
            WHERE cpu.price BETWEEN {body["price"][0]} AND {body["price"][1]}
                AND cpu.model LIKE "{body["model"]}%"
                AND cpu.speed BETWEEN {body["speed"][0]} AND {body["speed"][1]}
                AND cpu.cores BETWEEN {body["cores"][0]} AND {body["cores"][1]}
                AND cpu.threads BETWEEN {body["threads"][0]} AND {body["threads"][1]}
                AND cpu.hasGraphics = {body["hasGraphics"]}
                AND cpu.hasCooler = {body["hasCooler"]}
                AND brand.name IN ({'"{}"'.format('", "'.join(body["brand"]))})
                AND socket.name IN ({'"{}"'.format('", "'.join(body["socket"]))})
        """
        result = conn.exec_driver_sql(query).fetchall()
        jsonArr = []
        with app.test_client() as client:
            for cpuid in result:
                jsonArr.append(client.get(f"http://localhost:5000/cpu/info?cpuid={cpuid[0]}").json)
            
    response = flask.make_response(jsonArr)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/filter/ram", methods=["POST"])
def filterRam():
    body = flask.request.get_json()
    with engine.connect() as conn:
        query = f"""
            SELECT ramid FROM ram
            JOIN brand ON brand.brandid = ram.brandid
            JOIN ddrgen ON ddrgen.ddrgenid = ram.ddrgenid
            WHERE ram.price BETWEEN {body["price"][0]} AND {body["price"][1]}
                AND ram.model LIKE "{body["model"]}%"
                AND ram.size BETWEEN {body["size"][0]} AND {body["size"][1]}
                AND ram.speed BETWEEN {body["speed"][0]} AND {body["speed"][1]}
                AND ram.latency BETWEEN {body["latency"][0]} AND {body["latency"][1]}
                AND brand.name IN ({'"{}"'.format('", "'.join(body["brand"]))})
                AND ddrgen.name IN ({'"{}"'.format('", "'.join(body["ddrgen"]))})
        """
        result = conn.exec_driver_sql(query).fetchall()
        jsonArr = []
        with app.test_client() as client:
            for ramid in result:
                jsonArr.append(client.get(f"http://localhost:5000/ram/info?ramid={ramid[0]}").json)
            
    response = flask.make_response(jsonArr)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/filter/motherboard", methods=["POST"])
def filterMotherboard():
    body = flask.request.get_json()
    with engine.connect() as conn:
        query = f"""
            SELECT motherboardid FROM motherboard
            JOIN brand ON brand.brandid = motherboard.brandid
            JOIN chipset ON chipset.chipsetid = motherboard.chipsetid
            JOIN ddrgen ON ddrgen.ddrgenid = motherboard.ddrgenid
            JOIN socket ON socket.socketid = motherboard.socketid
            WHERE motherboard.price BETWEEN {body["price"][0]} AND {body["price"][1]}
                AND motherboard.model LIKE "{body["model"]}%"
                AND motherboard.usbcount BETWEEN {body["usbcount"][0]} AND {body["usbcount"][1]}
                AND chipset.name IN ({'"{}"'.format('", "'.join(body["chipset"]))})
                AND brand.name IN ({'"{}"'.format('", "'.join(body["brand"]))})
                AND ddrgen.name IN ({'"{}"'.format('", "'.join(body["ddrgen"]))})
                AND socket.name IN ({'"{}"'.format('", "'.join(body["socket"]))})
        """
        result = conn.exec_driver_sql(query).fetchall()
        jsonArr = []
        with app.test_client() as client:
            for motherboardid in result:
                jsonArr.append(client.get(f"http://localhost:5000/motherboard/info?motherboardid={motherboardid[0]}").json)
            
    response = flask.make_response(jsonArr)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/filter/psu", methods=["POST"])
def filterPsu():
    body = flask.request.get_json()
    with engine.connect() as conn:
        query = f"""
            SELECT psuid FROM psu
            JOIN brand ON brand.brandid = psu.brandid
            JOIN efficiency ON efficiency.efficiencyid = psu.efficiencyid
            WHERE psu.price BETWEEN {body["price"][0]} AND {body["price"][1]}
                AND psu.model LIKE "{body["model"]}%"
                AND psu.wattage BETWEEN {body["wattage"][0]} AND {body["wattage"][1]}
                AND brand.name IN ({'"{}"'.format('", "'.join(body["brand"]))})
                AND efficiency.name IN ({'"{}"'.format('", "'.join(body["efficiency"]))})
        """
        result = conn.exec_driver_sql(query).fetchall()
        jsonArr = []
        with app.test_client() as client:
            for psuid in result:
                jsonArr.append(client.get(f"http://localhost:5000/psu/info?psuid={psuid[0]}").json)
            
    response = flask.make_response(jsonArr)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/filter/gpu", methods=["POST"])
def filterGpu():
    body = flask.request.get_json()
    with engine.connect() as conn:
        query = f"""
            SELECT gpuid FROM gpu
            JOIN brand ON brand.brandid = gpu.brandid
            JOIN chipset ON chipset.chipsetid = gpu.chipsetid
            WHERE gpu.price BETWEEN {body["price"][0]} AND {body["price"][1]}
                AND gpu.model LIKE "{body["model"]}%"
                AND gpu.memory BETWEEN {body["memory"][0]} AND {body["memory"][1]}
                AND gpu.speed BETWEEN {body["speed"][0]} AND {body["speed"][1]}
                AND gpu.hdmicount BETWEEN {body["hdmicount"][0]} AND {body["hdmicount"][1]}
                AND gpu.displayportcount BETWEEN {body["displayportcount"][0]} AND {body["displayportcount"][1]}
                AND chipset.name IN ({'"{}"'.format('", "'.join(body["chipset"]))})
                AND brand.name IN ({'"{}"'.format('", "'.join(body["brand"]))})
        """
        result = conn.exec_driver_sql(query).fetchall()
        jsonArr = []
        with app.test_client() as client:
            for gpuid in result:
                jsonArr.append(client.get(f"http://localhost:5000/gpu/info?gpuid={gpuid[0]}").json)
            
    response = flask.make_response(jsonArr)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/filter/storage", methods=["POST"])
def filterStorage():
    body = flask.request.get_json()
    with engine.connect() as conn:
        query = f"""
            SELECT storageid FROM storage
            JOIN brand ON brand.brandid = storage.brandid
            JOIN storage_interface ON storage_interface.storageinterfaceid = storage.storageinterfaceid
            WHERE storage.price BETWEEN {body["price"][0]} AND {body["price"][1]}
                AND storage.model LIKE "{body["model"]}%"
                AND storage.capacity BETWEEN {body["capacity"][0]} AND {body["capacity"][1]}
                AND storage_interface.name IN ({'"{}"'.format('", "'.join(body["storageinterface"]))})
                AND brand.name IN ({'"{}"'.format('", "'.join(body["brand"]))})
        """
        result = conn.exec_driver_sql(query).fetchall()
        jsonArr = []
        with app.test_client() as client:
            for storageid in result:
                jsonArr.append(client.get(f"http://localhost:5000/storage/info?storageid={storageid[0]}").json)
            
    response = flask.make_response(jsonArr)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/filter/cooler", methods=["POST"])
def filterCooler():
    body = flask.request.get_json()
    with engine.connect() as conn:
        query = f"""
            SELECT cooler.coolerid FROM cooler
            JOIN brand ON brand.brandid = cooler.brandid
            JOIN cooler_socket ON cooler_socket.coolerid = cooler.coolerid
            JOIN socket ON socket.socketid = cooler_socket.socketid
            WHERE cooler.price BETWEEN {body["price"][0]} AND {body["price"][1]}
                AND cooler.model LIKE "{body["model"]}%"
                AND cooler.watercooled = {body["watercooled"]}
                AND socket.name IN ({'"{}"'.format('", "'.join(body["socket"]))})
                AND brand.name IN ({'"{}"'.format('", "'.join(body["brand"]))})
        """
        result = conn.exec_driver_sql(query).fetchall()
        jsonArr = []
        with app.test_client() as client:
            for coolerid in result:
                jsonArr.append(client.get(f"http://localhost:5000/cooler/info?coolerid={coolerid[0]}").json)
            
        seen = set()
        processedJson = []

        for item in jsonArr:
            if item['coolerid'] not in seen:
                processedJson.append(item)
                seen.add(item['coolerid'])
    response = flask.make_response(processedJson)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/compatability", methods=["POST"])
def checkCompatability():
    body = flask.request.get_json()
    print(body)
    with app.test_client() as client:
        if body['cpuid'] != 0:
            cpu = client.get(f"http://localhost:5000/cpu/info?cpuid={body['cpuid']}").json
        if body['ramid'] != 0:
            ram = client.get(f"http://localhost:5000/ram/info?ramid={body['ramid']}").json
        if body['motherboardid'] != 0:
            motherboard = client.get(f"http://localhost:5000/motherboard/info?motherboardid={body['motherboardid']}").json
        if body['psuid'] != 0:
            psu = client.get(f"http://localhost:5000/psu/info?psuid={body['psuid']}").json
        if body['gpuid'] != 0:
            gpu = client.get(f"http://localhost:5000/gpu/info?gpuid={body['gpuid']}").json
        if body['storageid'] != 0:
            storage = client.get(f"http://localhost:5000/storage/info?storageid={body['storageid']}").json
        if body['coolerid'] != 0:
            cooler = client.get(f"http://localhost:5000/cooler/info?coolerid={body['coolerid']}").json
    conflicts = []
    with engine.connect() as conn:
        # CPU RAM
        if body['cpuid'] != 0 and body['ramid'] != 0:
            cpuramcompat = False
            for ddrgen in cpu["ddrgen"]:
                query = f"SELECT ddrgenid FROM ddrgen WHERE name LIKE '{ddrgen}'"
                ddrgenid = conn.exec_driver_sql(query).fetchone()[0]
                if ddrgenid == ram["ddrgenid"]:
                    cpuramcompat = True
            if cpuramcompat == False:
                conflicts.append(["cpu", "ram", "Incompatible cpu and ram ddrgen"])
                conn.exec_driver_sql(query)

        #Motherboard RAM
        if body['motherboardid'] != 0 and body['ramid'] != 0:
            if motherboard["ddrgenid"] != ram["ddrgenid"]:
                conflicts.append(["motherboard", "ram", "Incompatible motherboard and ram ddrgen"])

        # CPU Motherboard
        if body['cpuid'] != 0 and body['motherboardid'] != 0:
            if cpu["socketid"] != motherboard["socketid"]:
                conflicts.append(["cpu", "motherboard", "Incompatible motherboard and cpu socket"])

        # Motherboard cooler
        if body['motherboardid'] != 0 and body['coolerid'] != 0:
            query = f"SELECT socketid FROM cooler_socket WHERE socketid == {motherboard['socketid']}"
            result = conn.exec_driver_sql(query).fetchone()
            if result == None:
                conflicts.append(["motherboard", "cooler", "Incompatible motherboard and cooler socket"])
        # Cpu cooler
        if body['cpuid'] != 0 and body['coolerid'] != 0:
            query = f"SELECT socketid FROM cooler_socket WHERE socketid == {cpu['socketid']}"
            result = conn.exec_driver_sql(query).fetchone()
            if result == None:
                conflicts.append(["cpu", "cooler", "Incompatible cpu and cooler socket"])


        # # Cooler needed?
        # if body['cpuid'] != 0 and body['coolerid'] != 0:
        #     if cpu["hascooler"] == False and body['coolerid'] == 0:
        #         conflicts.append(["cpu", "cooler", "CPU does not come with cooler"])

        # motherboard storage
        if body['storageid'] != 0 and body['motherboardid'] != 0:
            query = f"SELECT storageinterfaceid FROM motherboard_storage_interface WHERE motherboard_storage_interface.motherboardid = {motherboard['motherboardid']}"
            storageInterfaces = conn.exec_driver_sql(query).fetchall()
            if storage["storageinterfaceid"] not in storageInterfaces:
                conflicts.append(["motherboard", "storage", "Motherboard does not support chosen storage interface"])

    response = flask.make_response(conflicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response




if __name__ == "__main__":
    createTables()
    loadData()
    app.run()
