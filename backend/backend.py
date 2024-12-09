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
                GROUP_CONCAT(ddrgen.name, ', ') AS ddrgen
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
    return jsonify(jsonData)

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
    return jsonify(jsonData)

@app.route("/motherboard/info", methods=["GET"])
def getMotherboardInfo():
    motherboardid = flask.request.args.get("motherboardid")
    if motherboardid == None:
        response = flask.jsonify({"error": "No motherboardid provided"})
        response.status_code = 400
        return response
    with engine.connect() as conn:
        query = """
            SELECT motherboard.*, brand.name AS brand, ddrgen.name AS ddrgen,
                pciegen.name AS pciegen, GROUP_CONCAT(storage_interface.name, ', ') AS storageinterface
            FROM motherboard
            JOIN brand ON motherboard.brandid = brand.brandid
            JOIN ddrgen ON motherboard.ddrgenid = ddrgen.ddrgenid
            JOIN pciegen ON motherboard.pciegenid = pciegen.pciegenid
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
    return jsonify(jsonData)


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
    return jsonify(jsonData)


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
    return jsonify(jsonData)


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
    return jsonify(jsonData)


@app.route("/cooler/info", methods=["GET"])
def getCoolerInfo():
    coolerid = flask.request.args.get("coolerid")
    if coolerid == None:
        response = flask.jsonify({"error": "No coolerid provided"})
        response.status_code = 400
        return response
    with engine.connect() as conn:
        query = """
            SELECT cooler.*, brand.name AS brand, GROUP_CONCAT(socket.name, ', ') AS socket
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
    return jsonify(jsonData)


if __name__ == "__main__":
    createTables()
    loadData()
    app.run()
