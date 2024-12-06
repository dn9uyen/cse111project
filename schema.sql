CREATE TABLE IF NOT EXISTS cpu (
    cpuid INT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    model VARCHAR(128) NOT NULL,
    speed DECIMAL(3, 2) NOT NULL, -- GHz
    boostspeed DECIMAL(3, 2) NOT NULL, -- GHz
    cores INT NOT NULL,
    threads INT NOT NULL,
    tdp INT NOT NULL, -- watts (heat)
    wattage INT NOT NULL, -- watts (power)
    hasgraphics BOOLEAN NOT NULL, -- integrated graphics
    hascooler BOOLEAN NOT NULL, -- cooler included
    brandid INT NOT NULL,
    socketid INT NOT NULL,
    FOREIGN KEY (brandid) REFERENCES brand(brandid),
    FOREIGN KEY (socketid) REFERENCES socket(socketid)
);

CREATE TABLE IF NOT EXISTS ram (
    ramid INT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    model VARCHAR(128) NOT NULL,
    size INT NOT NULL, -- GB
    speed INT NOT NULL, -- MHz
    latency VARCHAR(20) NOT NULL, -- CL latency
    brandid INT NOT NULL,
    ddrgenid INT NOT NULL,
    FOREIGN KEY (brandid) REFERENCES brand(brandid),
    FOREIGN KEY (ddrgenid) REFERENCES ddrgen(ddrgenid)
);

CREATE TABLE IF NOT EXISTS motherboard (
    motherboardid INT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    model VARCHAR(128) NOT NULL,
    ramspeed INT NOT NULL,            -- Max supported speed, MHz
    usbcount INT NOT NULL,
    formfactor VARCHAR(16) NOT NULL,
    chipset VARCHAR(16) NOT NULL,
    brandid INT NOT NULL,
    pciegenid INT NOT NULL,
    ddrgenid INT NOT NULL,
    socketid INT NOT NULL,
    FOREIGN KEY (brandid) REFERENCES brand(brandid),
    FOREIGN KEY (pciegenid) REFERENCES pciegen(pciegenid),
    FOREIGN KEY (ddrgenid) REFERENCES ddrgen(ddrgenid),
    FOREIGN KEY (socketid) REFERENCES socket(socketid)
);

CREATE TABLE IF NOT EXISTS psu (
    psuid INT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    model VARCHAR(128) NOT NULL,
    wattage INT NOT NULL, -- watts (power)
    brandid INT NOT NULL,
    efficiencyid INT NOT NULL,
    FOREIGN KEY (brandid) REFERENCES brand(brandid),
    FOREiGN KEY (efficiencyid) REFERENCES efficiency(efficiencyid)
);

CREATE TABLE IF NOT EXISTS gpu (
    gpuid INT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    model VARCHAR(128) NOT NULL,
    memory INT NOT NULL, -- GB
    speed DECIMAL(4, 3) NOT NULL, -- Clock speed, GHz
    boostspeed DECIMAL(4, 3) NOT NULL, -- Boost clock speed, GHz
    hdmicount INT NOT NULL,
    displayportcount INT NOT NULL,
    brandid INT NOT NULL,
    chipsetid INT NOT NULL,
    pciegenid INT NOT NULL,
    FOREIGN KEY (brandid) REFERENCES brand(brandid),
    FOREIGN KEY (pciegenid) REFERENCES pciegen(pciegenid),
    FOREIGN KEY (chipsetid) REFERENCES chipset(chipsetid)
);

CREATE TABLE IF NOT EXISTS storage (
    storageid INT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    model VARCHAR(128) NOT NULL,
    capacity INT NOT NULL, -- GB
    brandid INT NOT NULL,
    storageinterfaceid INT NOT NULL,
    FOREIGN KEY (brandid) REFERENCES brand(brandid),
    FOREIGN KEY (storageinterfaceid) REFERENCES storage_interface(storageinterfaceid)
);

CREATE TABLE IF NOT EXISTS cooler (
    coolerid INT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    model VARCHAR(128) NOT NULL,
    watercooled BOOLEAN NOT NULL,
    brandid INT NOT NULL,
    FOREIGN KEY (brandid) REFERENCES brand(brandid)
);



CREATE TABLE IF NOT EXISTS brand (
    brandid INT PRIMARY KEY,
    name VARCHAR(16) NOT NULL
);

CREATE TABLE IF NOT EXISTS storage_interface (
    storageinterfaceid INT PRIMARY KEY,
    name VARCHAR(16) NOT NULL  -- SATA, NVMe, etc.
);

CREATE TABLE IF NOT EXISTS socket (
    socketid INT PRIMARY KEY,
    name VARCHAR(16) NOT NULL -- AM4, AM5, LGA1700, etc
);

CREATE TABLE IF NOT EXISTS pciegen (
    pciegenid INT PRIMARY KEY,
    name VARCHAR(16) NOT NULL -- PCIe 3.0, PCIe 4.0, etc
);

CREATE TABLE IF NOT EXISTS ddrgen (
    ddrgenid INT PRIMARY KEY,
    name VARCHAR(8) NOT NULL -- DDR4, DDR5
);

CREATE TABLE IF NOT EXISTS chipset (
    chipsetid INT PRIMARY KEY,
    name VARCHAR(16) NOT NULL -- AMD X670, INTEL Z690, etc
);

CREATE TABLE IF NOT EXISTS efficiency (
    efficiencyid INT PRIMARY KEY,
    name VARCHAR(16) NOT NULL -- 80+ Bronze, 80+ Gold, etc
);



-- motherboards can support multiple interfaces
CREATE TABLE IF NOT EXISTS motherboard_storage_interface (
    motherboardid INT NOT NULL,
    storageinterfaceid INT NOT NULL,
    PRIMARY KEY (motherboardid, interfaceid),
    FOREIGN KEY (motherboardid) REFERENCES motherboard(motherboardid),
    FOREIGN KEY (storageinterfaceid) REFERENCES storage_interface(storageinterfaceid)
);

-- cpu can support multiple ddr generations
CREATE TABLE IF NOT EXISTS cpu_ddrgen ( 
    cpuid INT NOT NULL,
    ddrgenid INT NOT NULL,
    PRIMARY KEY (cpuid, ddrgenid),
    FOREIGN KEY (cpuid) REFERENCES cpu(cpuid),
    FOREIGN KEY (ddrgenid) REFERENCES ddrgen(ddrgenid)
);

-- cooler can support multiple sockets
CREATE TABLE IF NOT EXISTS cooler_socket ( 
    coolerid INT NOT NULL,
    socketid INT NOT NULL,
    PRIMARY KEY (coolerid, socketid),
    FOREIGN KEY (coolerid) REFERENCES cooler(coolerid),
    FOREIGN KEY (socketid) REFERENCES socket(socketid)
);



CREATE TABLE IF NOT EXISTS user (
    userid INT NOT NULL,
    username VARCHAR(32) NOT NULL,
    password VARCHAR(60) NOT NULL -- hashed if we have time to implement
);

CREATE TABLE IF NOT EXISTS build (
    buildid INT,
    userid INT,
    cpuid INT,
    ramid INT,
    motherboardid INT,
    psuid INT,
    gpuid INT,
    storageid INT,
);