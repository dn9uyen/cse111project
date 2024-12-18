-- .separator |
-- .import 'data/cpu.tbl' cpu
-- .import 'data/ram.tbl' ram
-- .import 'data/motherboard.tbl' motherboard
-- .import 'data/psu.tbl' psu
-- .import 'data/gpu.tbl' gpu
-- .import 'data/storage.tbl' storage
-- .import 'data/brand.tbl' brand
-- .import 'data/storage_interface.tbl' storage_interface
-- .import 'data/socket.tbl' socket
-- .import 'data/pciegen.tbl' pciegen
-- .import 'data/ddrgen.tbl' ddrgen
-- .import 'data/chipset.tbl' chipset
-- .import 'data/efficiency.tbl' efficiency
-- .import 'data/motherboard_storage_interface.tbl' motherboard_storage_interface
-- .import 'data/cpu_ddrgen.tbl' cpu_ddrgen
-- Insert data into brand table
INSERT OR IGNORE INTO brand (brandid, name) VALUES (1, 'Intel');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (2, 'AMD');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (3, 'Corsair');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (4, 'G.Skill');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (5, 'Samsung');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (6, 'NVIDIA');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (7, 'Thermalright');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (8, 'ASUS');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (9, 'Gigabyte');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (10, 'MSI');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (11, 'Cooler Master');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (12, 'Noctua');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (13, 'be quiet!');
INSERT OR IGNORE INTO brand (brandid, name) VALUES (14, 'NZXT');

-- Insert data into efficiency table
INSERT OR IGNORE INTO efficiency (efficiencyid, name) VALUES (1, '80+ Bronze');
INSERT OR IGNORE INTO efficiency (efficiencyid, name) VALUES (2, '80+ Gold');
INSERT OR IGNORE INTO efficiency (efficiencyid, name) VALUES (3, '80+ Platinum');

-- Insert data into chipset table
INSERT OR IGNORE INTO chipset (chipsetid, name) VALUES (1, 'AMD B550');
INSERT OR IGNORE INTO chipset (chipsetid, name) VALUES (2, 'Intel Z490');
INSERT OR IGNORE INTO chipset (chipsetid, name) VALUES (3, 'GeForce RTX 4070 SUPER');
INSERT OR IGNORE INTO chipset (chipsetid, name) VALUES (4, 'Intel H470');
INSERT OR IGNORE INTO chipset (chipsetid, name) VALUES (5, 'Intel B750');
INSERT OR IGNORE INTO chipset (chipsetid, name) VALUES (6, 'GeForce RTX 4060');
INSERT OR IGNORE INTO chipset (chipsetid, name) VALUES (7, 'Radeon RX 7700 XT');
INSERT OR IGNORE INTO chipset (chipsetid, name) VALUES (8, 'GeForce RTX 4090');

-- Insert data into socket and ddrgen tables for compatibility
INSERT OR IGNORE INTO socket (socketid, name) VALUES (1, 'LGA1200');
INSERT OR IGNORE INTO socket (socketid, name) VALUES (2, 'AM4');
INSERT OR IGNORE INTO socket (socketid, name) VALUES (3, 'LGA1700');
INSERT OR IGNORE INTO socket (socketid, name) VALUES (4, 'AM5');
INSERT OR IGNORE INTO socket (socketid, name) VALUES (5, 'LGA1151');
INSERT OR IGNORE INTO socket (socketid, name) VALUES (6, 'LGA1851');

INSERT OR IGNORE INTO ddrgen (ddrgenid, name) VALUES (1, 'DDR4');
INSERT OR IGNORE INTO ddrgen (ddrgenid, name) VALUES (2, 'DDR5');

-- Insert data into pciegen and storage_interface tables
INSERT OR IGNORE INTO pciegen (pciegenid, name) VALUES (1, 'PCIe 3.0');
INSERT OR IGNORE INTO pciegen (pciegenid, name) VALUES (2, 'PCIe 4.0');
INSERT OR IGNORE INTO storage_interface (storageinterfaceid, name) VALUES (1, 'SATA');
INSERT OR IGNORE INTO storage_interface (storageinterfaceid, name) VALUES (2, 'NVMe');

-- Insert data into the CPU table
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (1, 299.99, 'Intel Core i5-10400', 2.9, 4.3, 6, 12, 65, 125, 1, 1, 1, 1);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (2, 105.00, 'AMD Ryzen 5600X', 3.7, 4.6, 6, 12, 65, 85, 0, 1, 2, 2);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (3, 89.99, 'AMD Ryzen 3600', 3.6, 4.2, 6, 12, 65, 75, 0, 1, 2, 2);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (4, 111.99, 'Intel Core i5-12400F', 2.5, 4.4, 6, 12, 65, 150, 0, 1, 1, 3);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (5, 438.99, 'Intel Core i9-14900K', 3.2, 6.0, 24, 32, 125, 240, 1, 0, 1, 3);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (6, 299.99, 'Intel Core i5-11400F', 2.6, 4.4, 6, 12, 65, 90, 0, 1, 1, 1);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (7, 200.99, 'AMD Ryzen 5700X3D', 3.0, 4.1, 8, 16, 105, 120, 0, 0, 2, 2);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (8, 449.00, 'AMD Ryzen 7 7800X3D', 4.2, 5.0, 8, 16, 120, 120, 1, 0, 2, 4);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (9, 479.99, 'AMD Ryzen 7 9800X3D', 4.7, 5.2, 8, 16, 120, 120, 1, 0, 2, 4);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (10, 209.98, 'Intel Core i7-12700K', 3.6, 5.0, 12, 20, 125, 125, 1, 0, 1, 3);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (11, 89.99, 'Intel Core i5-9400F', 2.9, 4.1, 6, 6, 65, 65, 0, 1, 1, 5);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (12, 130.00, 'Intel Core i7-6700K', 4.0, 4.2, 4, 8, 91, 91, 1, 0, 1, 5);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (13, 319.00, 'Intel Core Ultra 5 245K', 4.2, 5.2, 14, 14, 125, 125, 1, 0, 1, 6);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (14, 399.00, 'Intel Core Ultra 7 265KF', 3.9, 5.5, 20, 20, 125, 125, 0, 0, 1, 6);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (15, 289.00, 'Intel Core Ultra 5 245KF', 4.2, 5.2, 14, 14, 125, 125, 0, 0, 1, 6);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (16, 639.98, 'AMD Ryzen 9 7950X3D', 4.2, 5.7, 16, 12, 120, 120, 1, 0, 2, 4);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (17, 599.00, 'AMD Ryzen 9 9950X', 4.3, 5.7, 16, 32, 170, 170, 1, 0, 2, 4);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (18, 93.99, 'AMD Ryzen 5 3600', 3.6, 4.2, 6, 12, 65, 65, 0, 1, 2, 2);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (19, 78.99, 'AMD Ryzen 5 5500', 3.6, 4.2, 6, 12, 65, 65, 0, 1, 2, 2);
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (20, 312.00, 'AMD Ryzen 9 5950X', 3.4, 4.9, 16, 32, 105, 105, 0, 0, 2, 2);

-- Insert data into the RAM table (with new size attribute)
INSERT OR IGNORE INTO ram (ramid, price, model, size, speed, latency, brandid, ddrgenid)
VALUES (1, 89.99, 'Corsair Vengeance LPX', 16, 3200, 16, 3, 1);
INSERT OR IGNORE INTO ram (ramid, price, model, size, speed, latency, brandid, ddrgenid)
VALUES (2, 108.99, 'Corsair Vengeance RGB', 32, 3600, 18, 3, 1);
INSERT OR IGNORE INTO ram (ramid, price, model, size, speed, latency, brandid, ddrgenid)
VALUES (3, 109.99, 'G.Skill Ripjaws V', 32, 3600, 18, 4, 1);
INSERT OR IGNORE INTO ram (ramid, price, model, size, speed, latency, brandid, ddrgenid)
VALUES (4, 79.99, 'G.Skill Ripjaws V', 16, 3600, 18, 4, 1);
INSERT OR IGNORE INTO ram (ramid, price, model, size, speed, latency, brandid, ddrgenid)
VALUES (5, 189.99, 'G.Skill Triden Z5 RGB', 64, 6400, 32, 4, 2);
INSERT OR IGNORE INTO ram (ramid, price, model, size, speed, latency, brandid, ddrgenid)
VALUES (6, 119.99, 'Corsair Vengeance', 32, 6000, 30, 3, 2);
INSERT OR IGNORE INTO ram (ramid, price, model, size, speed, latency, brandid, ddrgenid)
VALUES (7, 119.99, 'Corsair Vengeance', 32, 6000, 30, 3, 2);
INSERT OR IGNORE INTO ram (ramid, price, model, size, speed, latency, brandid, ddrgenid)
VALUES (8, 108.99, 'Corsair Dominator Titanium', 64, 6600, 32, 3, 2);

-- Insert data into motherboard table
INSERT OR IGNORE INTO motherboard (motherboardid, price, model, ramspeed, usbcount, formfactor, chipsetid, brandid, pciegenid, ddrgenid, socketid)
VALUES (1, 199.99, 'ASUS TUF Gaming B550', 4400, 6, 'ATX', 1, 8, 2, 1, 2);
INSERT OR IGNORE INTO motherboard (motherboardid, price, model, ramspeed, usbcount, formfactor, chipsetid, brandid, pciegenid, ddrgenid, socketid)
VALUES (2, 109.99, 'MSI B550 GAMING GEN3', 4400, 10, 'ATX', 1, 10, 2, 1, 2);
INSERT OR IGNORE INTO motherboard (motherboardid, price, model, ramspeed, usbcount, formfactor, chipsetid, brandid, pciegenid, ddrgenid, socketid)
VALUES (3, 99.99, 'Gigabyte H410M H V2', 2933, 6, 'Micro ATX', 4, 9, 2, 1, 1);
INSERT OR IGNORE INTO motherboard (motherboardid, price, model, ramspeed, usbcount, formfactor, chipsetid, brandid, pciegenid, ddrgenid, socketid)
VALUES (4, 159.99, 'MSI B760 GAMING PLUS WIFI', 6800, 10, 'ATX', 5, 10, 2, 2, 3);

-- Insert data into PSU table with correct brand and efficiency reference
INSERT OR IGNORE INTO psu (psuid, price, model, wattage, brandid, efficiencyid)
VALUES (1, 79.99, 'Corsair CX650M', 650, 3, 1);
INSERT OR IGNORE INTO psu (psuid, price, model, wattage, brandid, efficiencyid)
VALUES (2, 99.99, 'Corsair RM750e', 750, 3, 2);
INSERT OR IGNORE INTO psu (psuid, price, model, wattage, brandid, efficiencyid)
VALUES (3, 159.99, 'Corsair RM1000e', 1000, 3, 2);
INSERT OR IGNORE INTO psu (psuid, price, model, wattage, brandid, efficiencyid)
VALUES (4, 104.99, 'Corsair RM850', 850, 3, 2);
INSERT OR IGNORE INTO psu (psuid, price, model, wattage, brandid, efficiencyid)
VALUES (5, 154.99, 'Corsair SF750', 750, 3, 3);

-- Insert data into GPU table
INSERT OR IGNORE INTO gpu (gpuid, price, model, memory, speed, boostspeed, hdmicount, displayportcount, brandid, chipsetid, pciegenid)
VALUES (1, 599.99, 'Gigabyte WINDFORCE OC', 12, 1.980, 2.505, 1, 3, 9, 3, 2);
INSERT OR IGNORE INTO gpu (gpuid, price, model, memory, speed, boostspeed, hdmicount, displayportcount, brandid, chipsetid, pciegenid)
VALUES (2, 298.99, 'MSI VENTUS 2X BLACK OC', 8, 1.830, 2.505, 1, 3, 10, 6, 2);
INSERT OR IGNORE INTO gpu (gpuid, price, model, memory, speed, boostspeed, hdmicount, displayportcount, brandid, chipsetid, pciegenid)
VALUES (3, 398.99, 'Gigabyte GAMING OC', 12, 1.700, 2.599, 2, 2, 9, 7, 2);
INSERT OR IGNORE INTO gpu (gpuid, price, model, memory, speed, boostspeed, hdmicount, displayportcount, brandid, chipsetid, pciegenid)
VALUES (4, 1999.99, 'Asus ROG STRIX GAMING OC', 24, 2.235, 2.640, 2, 3, 8, 8, 2);

-- Insert data into storage table
INSERT OR IGNORE INTO storage (storageid, price, model, capacity, brandid, storageinterfaceid)
VALUES (1, 59.99, 'Samsung 970 Evo', 500, 5, 2);
INSERT OR IGNORE INTO storage (storageid, price, model, capacity, brandid, storageinterfaceid)
VALUES (2, 159.99, 'Samsung 990 Pro', 2000, 5, 2);
INSERT OR IGNORE INTO storage (storageid, price, model, capacity, brandid, storageinterfaceid)
VALUES (3, 299.99, 'Samsung 990 Pro', 4000, 5, 2);
INSERT OR IGNORE INTO storage (storageid, price, model, capacity, brandid, storageinterfaceid)
VALUES (4, 119.99, 'Samsung 980 Pro', 1000, 5, 2);
INSERT OR IGNORE INTO storage (storageid, price, model, capacity, brandid, storageinterfaceid)
VALUES (5, 103.99, 'Samsung 980 Evo', 1000, 5, 1);
INSERT OR IGNORE INTO storage (storageid, price, model, capacity, brandid, storageinterfaceid)
VALUES (6, 99.99, 'Samsung 960 Evo', 500, 5, 1);

-- Insert data into the cooler table
INSERT OR IGNORE INTO cooler (coolerid, price, model, watercooled, brandid)
VALUES (1, 34.99, 'Thermalright Peerless Assassin 120 SE', 0, 7);
INSERT OR IGNORE INTO cooler (coolerid, price, model, watercooled, brandid)
VALUES (2, 124.99, 'Corsair iCUE H150i ELITE CAPELLIX XT', 1, 3);
INSERT OR IGNORE INTO cooler (coolerid, price, model, watercooled, brandid)
VALUES (3, 79.99, 'Corsair iCUE H100i RGB ELITE', 1, 3);
INSERT OR IGNORE INTO cooler (coolerid, price, model, watercooled, brandid)
VALUES (4, 29.99, 'Cooler Master Hyper 212 Black Edition', 0, 11);
INSERT OR IGNORE INTO cooler (coolerid, price, model, watercooled, brandid)
VALUES (5, 119.95, 'Noctua NH-D15 chromax.black', 0, 12);
INSERT OR IGNORE INTO cooler (coolerid, price, model, watercooled, brandid)
VALUES (6, 89.90, 'be quiet! Dark Rock Pro 5', 0, 13);
INSERT OR IGNORE INTO cooler (coolerid, price, model, watercooled, brandid)
VALUES (7, 109.95, 'Noctua NH-D15', 0, 12);
INSERT OR IGNORE INTO cooler (coolerid, price, model, watercooled, brandid)
VALUES (8, 179.99, 'NZXT Kraken 360', 1, 14);


-- Additional interface and DDR compatibility
INSERT OR IGNORE INTO motherboard_storage_interface (motherboardid, storageinterfaceid) VALUES (1, 1);
INSERT OR IGNORE INTO motherboard_storage_interface (motherboardid, storageinterfaceid) VALUES (1, 2);
INSERT OR IGNORE INTO motherboard_storage_interface (motherboardid, storageinterfaceid) VALUES (2, 1);
INSERT OR IGNORE INTO motherboard_storage_interface (motherboardid, storageinterfaceid) VALUES (2, 2);
INSERT OR IGNORE INTO motherboard_storage_interface (motherboardid, storageinterfaceid) VALUES (3, 1);
INSERT OR IGNORE INTO motherboard_storage_interface (motherboardid, storageinterfaceid) VALUES (3, 2);
INSERT OR IGNORE INTO motherboard_storage_interface (motherboardid, storageinterfaceid) VALUES (4, 1);
INSERT OR IGNORE INTO motherboard_storage_interface (motherboardid, storageinterfaceid) VALUES (4, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (1, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (2, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (3, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (4, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (4, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (5, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (5, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (6, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (6, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (7, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (8, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (9, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (10, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (10, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (11, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (12, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (13, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (14, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (15, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (16, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (17, 2);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (18, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (19, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (20, 1);

INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (1, 1);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (1, 2);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (1, 3);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (1, 4);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (1, 5);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (1, 6);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (2, 1);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (2, 2);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (2, 3);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (2, 4);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (2, 5);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (2, 6);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (3, 1);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (3, 2);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (3, 3);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (3, 4);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (3, 5);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (3, 6);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (4, 1);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (4, 2);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (4, 3);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (4, 4);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (4, 5);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (4, 6);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (5, 1);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (5, 2);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (5, 3);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (5, 4);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (5, 5);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (5, 6);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (6, 1);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (6, 2);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (6, 3);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (6, 4);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (6, 5);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (6, 6);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (7, 1);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (7, 2);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (7, 3);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (7, 4);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (7, 5);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (7, 6);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (8, 1);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (8, 2);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (8, 3);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (8, 4);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (8, 5);
INSERT OR IGNORE INTO cooler_socket (coolerid, socketid) VALUES (8, 6);
