const apiUrl = "http://127.0.0.1:5000"

/*
 * Example usage
    <button onClick={() => getPartInfo("cpu", 1)}>Get info</button>
    <button onClick={() => addPartInfo("cpu", {"price": 1000, "model": "Intel Core i7 14700", "speed": 4.0, "boostspeed": 5.0, "cores": 16, "threads": "24", "tdp": 150, "wattage": 150, "hasgraphics": true, "hascooler": false, "brand": "Intel", "socket": "LGA1700", "ddrgen": ["DDR4", "DDR5"]})}>Add info</button>
    <button onClick={() => changePartInfo("cpu", {"cpuid": 1, "price": 1000, "model": "Intel Core i7 14700", "speed": 4.0, "boostspeed": 5.0, "cores": 16, "threads": "24", "tdp": 150, "wattage": 150, "hasgraphics": true, "hascooler": false, "brand": "Intel", "socket": "LGA1700", "ddrgen": ["DDR4", "DDR5"]})}>Add info</button>
    <button onClick={() => getTable("brand")}>Get table</button>
    <button onClick={() => filterPart("cpu", {"price": [0, 100], "model": "In", "speed": [2.0,5.0], "cores": [4,20], "threads":[8,24], "tdp":[50,200], "hasGraphics": 1, "hasCooler": 0, "brand": ["Intel"], "socket": ["LGA1700", "LGA1200"]})}>Get table</button>
 */

export async function getPartInfo(partType, partId) {
    // partType can be: cpu, ram, motherboard, psu, gpu, storage, cooler
    // partId is an int
    // Use this to get info for a specific part
    // Returns a json of the part info
    const response = await fetch(`${apiUrl}/cpu/info?${partType}id=${partId}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });
    const json = await response.json()
    if (response.status != 200) {
        return new Error(json)
    }
    return json
}

export async function addPartInfo(partType, partInfo) {
    // Add new part to database
    // partType can be: cpu, ram, motherboard, psu, gpu, storage, cooler
    // partInfo is a json of the corresponding info
    //   Example for cpu: {"price": 100, "model": "Intel Core i7 14700", "speed": 4.0, "boostspeed": 5.0, "cores": 16, "threads": "24", "tdp": 150, "wattage": 150, "hasgraphics": true, "hascooler": false, "brand": "Intel", "socket": "LGA1700", "ddrgen": ["DDR4", "DDR5"]}
    //   Example for ram: {"price": 100, "model": "Corsair Vengence", "size": 16, "speed": 3600, "latency": "CL16", "brand": "Corsair", "ddrgen": "ddr4"}
    //   Example for motherboard: {"price": 100, "model": "Asus B470", "ramspeed": 4000, "usbcount": 5, "formfactor": "ATX", "chipset": "B470", "brand": "Asus", "pciegen": "PCIe 4.0", "ddrgen": "DDR4", "socket": "AM4", "storageinterface": ["SATA", "NVMe"]}
    //   Example for psu: {"price": 100, "model": "Corsair RM1000", "wattage": 1000, "brand": "Corsair", "efficiency": "80+ Gold"}
    //   Example for gpu: {"price": 100, "model": "Gigabyte 4090", "memory": 24, "speed": 3.4, "boostspeed": 3.8, "hdmicount": 4, "displayportcount": 1, "brand": "Gigabyte", "chipset": "GeForce RTX 4090", "pciegen": "PCIe 4.0"}
    //   Example for storage: {"price": 100, "model": "Samsung 970 Evo", "capacity": 1000, "brand": "Samsung", "storageinterface": "NVMe"}
    //   Example for cooler: {"price": 100, "model": "Corsair H100i", "watercooled": false, "brand": "Corsair", "socket": ["LGA1700", "AM4", "LGA1200"]}
    // Returns json containing new part's id
    const response = await fetch(`${apiUrl}/${partType}/info`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(partInfo)
    });
    const json = await response.json()
    if (response.status != 200) {
        return new Error(json)
    }
    return json
}

export async function changePartInfo(partType, partInfo) {
    // Update part info in database. Not required to include all attributes
    // partType can be: cpu, ram, motherboard, psu, gpu, storage, cooler
    // partInfo examples same as addPartInfo()
    // Returns json of updated part info
    const response = await fetch(`${apiUrl}/${partType}/info`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(partInfo)
    });
    const json = await response.json()
    if (response.status != 200) {
        return new Error(json)
    }
    return json
}

export async function deletePartInfo(partType, partId) {
    // partType can be: cpu, ram, motherboard, psu, gpu, storage, cooler
    // partId is an int
    // Use this to delete a specific part
    // Returns a json of the deleted part info
    const response = await fetch(`${apiUrl}/cpu/info?${partType}id=${partId}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
    });
    const json = await response.json()
    if (response.status != 200) {
        return new Error(json)
    }
    return json
}

export async function getTable(table) {
    // Use this to get tables to use in other queries
    // Ex: list of brands like ["Corsair", "Intel", "Asus"]
    // Possible tables: brand, socket, pciegen, ddrgen, efficiency, chipset, storageinterface
    // Returns a json array of the table
    const response = await fetch(`${apiUrl}/filter/${table}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });
    const json = await response.json()
    if (response.status != 200) {
        return new Error(json)
    }
    return json
}

export async function filterPart(partType, filter) {
    // Use this to filter for a part type
    // partType can be: cpu, ram, motherboard, psu, gpu, storage, cooler
    // Returns a json array of part info. [{part info}, {part info}, {part info}]
    // filter is json of filter arguments
    //   json items with [int, int] are a range so "price":[10,200] is price between 10 and 200
    //   json items with [string, string, ...] are a list of strings to filter for
    // possible filter arguments:
    //   for cpu: {"price": [0, 100], "model": "Intel i7", "speed": [2.0,4.0], "cores": [4,20], "threads":[8,24], "tdp":[50,100], "hasGraphics": 1, "hasCooler": 1, "brand": ["Intel"], "socket": ["LGA1700", "LGA1200"]}
    //   for ram: {"price": [0, 100], "model": "Corsair Vengence", "size": [8, 32], "speed": [3000, 4000], "latency": [16, 20], "brand": ["Corsair"], "ddrgen": ["DDR4", "DDR5"]}
    //   for motherboard: {"price": [0,100], "model": "Asus X470", "usbcount": [2, 6], "chipset": ["X470", "X570"], "brand": ["Asus", "Gigabyte"], "ddrgen":["DDR4", "DDR5"], "socket": ["AM4"]}
    //   for psu: {"price": [0,100], "model": "", "wattage": [500, 1000], "brand": ["Corsair"], "efficiency": ["80+ Gold", "80+ Platinum"]}
    //   for gpu: {"price": [0, 100], "model": "Asus 4070", "memory": [8, 16], "speed": [1800, 2000], "hdmicount": [1, 3], "displayportcount":[0, 1], "brand": ["Asus", "Gigabyte"], "chipset": ["Nvidia 4070"]}
    //   for storage: {"price": [0, 100], "model": "Samsung 970", "capacity": [1000, 2000], "brand": ["Samsung", "Western Digital"], "storageinterface": ["NVMe"]}
    //   for cooler: {"price": [0, 100], "model": "Corsair H100", "watercooled": 1, "brand": ["Corsair", "NZXT"], "socket": ["AM4"]}
    const response = await fetch(`${apiUrl}/filter/${partType}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(filter)
    });
    const json = await response.json()
    if (response.status != 200) {
        return new Error(json)
    }
    return json
}
