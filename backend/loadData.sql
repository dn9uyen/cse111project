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
INSERT OR IGNORE INTO cpu (cpuid, price, model, speed, boostspeed, cores, threads, tdp, wattage, hasgraphics, hascooler, brandid, socketid)
VALUES (1, 299.99, 'Intel Core i5-10400', 2.9, 4.3, 6, 12, 65, 125, 1, 1, 1, 1);

INSERT OR IGNORE INTO brand (brandid, name) VALUES (1, 'Intel');

INSERT OR IGNORE INTO socket (socketid, name) VALUES (1, 'LGA1200');

INSERT OR IGNORE INTO ddrgen (ddrgenid, name) VALUES (1, 'DDR4');
INSERT OR IGNORE INTO ddrgen (ddrgenid, name) VALUES (2, 'DDR5');

INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (1, 1);
INSERT OR IGNORE INTO cpu_ddrgen (cpuid, ddrgenid) VALUES (1, 2);
