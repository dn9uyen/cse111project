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
    jsonData = {
        "cpuid": data["cpuid"],
        "price": data["price"],
        "model": data["model"],
        "speed": data["speed"],
        "boostspeed": data["boostspeed"],
        "cores": data["cores"],
        "threads": data["threads"],
        "tdp": data["tdp"],
        "wattage": data["wattage"],
        "hascooler": data["hascooler"],
        "brand": data["brand"],
        "socket": data["socket"],
        "ddrgen": data["ddrgen"].split(",")
    }
    return jsonify(jsonData)


@app.route("/cpu/info", methods=["POST"])
def addCpu():
    body = flask.request.get_json()
    with engine.connect() as conn:
    # for col, val in body.items():

    return "a"


if __name__ == "__main__":
    createTables()
    loadData()
    app.run()
