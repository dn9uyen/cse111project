import { useEffect, useState } from "react"
import { getTable } from "../api"

const cpuFilter = {
    "price": "range",
    "model": "text",
    "speed": "range",
    "cores": "range",
    "threads": "range",
    "tdp": "range",
    "hasGraphics": "bool",
    "hasCooler": "bool",
    "brand": "selection",
    "socket": "selection",
}
const ramFilter = {
    "price": "range",
    "model": "text",
    "size": "range",
    "speed": "range",
    "latency": "range",
    "brand": "selection",
    "ddrgen": "selection",
}
const motherboardFilter = {
    "price": "range",
    "model": "text",
    "usbcount": "range",
    "chipset": "selection",
    "brand": "selection",
    "ddrgen": "selection",
    "socket": "selection",
}
const psuFilter = {
    "price": "range",
    "model": "text",
    "wattage": "range",
    "brand": "selection",
    "efficiency": "selection",
}
const gpuFilter = {
    "price": "range",
    "model": "text",
    "memory": "range",
    "speed": "range",
    "hdmicount": "range",
    "displayportcount": "range",
    "brand": "selection",
    "chipset": "selection",
}
const storageFilter = {
    "price": "range",
    "model": "text",
    "capacity": "range",
    "brand": "selection",
    "storageinterface": "selection",
}
const coolerFilter = {
    "price": "range",
    "model": "text",
    "watercooled": "bool",
    "brand": "selection",
    "socket": "selection",
}



const createFilter = (filterType, filterJsonCB) => {
    const [selectedOptions, setSelectedOptions] = useState({
        brand: [],
        socket: [],
        pciegen: [],
        ddrgen: [],
        efficiency: [],
        chipset: [],
        storageinterface: [],
    });
    const [tables, setTables] = useState({
        brand: [],
        socket: [],
        pciegen: [],
        ddrgen: [],
        efficiency: [],
        chipset: [],
        storageinterface: [],
    });
    useEffect(() => {
        const fetchTables = async () => {
            const brand = await getTable("brand");
            const socket = await getTable("socket");
            const pciegen = await getTable("pciegen");
            const ddrgen = await getTable("ddrgen");
            const efficiency = await getTable("efficiency");
            const chipset = await getTable("chipset");
            const storageinterface = await getTable("storageinterface");
            setTables({
                brand,
                socket,
                pciegen,
                ddrgen,
                efficiency,
                chipset,
                storageinterface
            });
            setSelectedOptions({
                brand,
                socket,
                pciegen,
                ddrgen,
                efficiency,
                chipset,
                storageinterface
            });
        };
        fetchTables();
    }, []);

    let filter = {}
    switch (filterType) {
        case "cpu":
            filter = cpuFilter
            break;
        case "ram":
            filter = ramFilter
            break;
        case "motherboard":
            filter = motherboardFilter
            break;
        case "psu":
            filter = psuFilter
            break;
        case "gpu":
            filter = gpuFilter
            break;
        case "storage":
            filter = storageFilter
            break;
        case "cooler":
            filter = coolerFilter
            break;
    }
    const keys = Object.keys(filter);

    const handleSelectChange = (e, field) => {
        const options = Array.from(e.target.selectedOptions, option => option.value)[0];
        setSelectedOptions((prevState) => {
            let newOptions = prevState[field]
            if (!prevState[field].includes(options)) {
                newOptions.push(options)
            }
            else {
                newOptions = newOptions.filter(item => item !== options)
            }

            filterJsonCB(field, newOptions)

            return {
                ...prevState,
                [field]: newOptions,
            };
        });
    };

    const createField = (field, fieldType) => {
        switch (fieldType) {
            case "range":
                return (
                    <>
                        Min<input type="text" name={field + "min"} style={{ width: "40px", margin: "0px 15px 0px 5px" }} />
                        Max<input type="text" name={field + "max"} style={{ width: "40px", marginLeft: "5px" }} />
                    </>
                )
                break;
            case "text":
                return (
                    <input type="text" name={field} style={{ width: "100%" }} />
                )
                break;
            case "bool":
                return (
                    <>
                        <select id="dropdown" name={field}>
                            <option value="false" >No</option>
                            <option value="true" >Yes</option>
                        </select>
                    </>
                )
                break;
            case "selection":
                return (
                    <>
                        <select
                            id={field}
                            name={field}
                            multiple
                            value={selectedOptions[field] || []}
                            size={tables[field].length}
                            onChange={(e) => handleSelectChange(e, field)}
                        >
                            {tables[field].map((option, index) => (
                                <option value={option} key={index}>
                                    {option}
                                </option>
                            ))}
                        </select>
                    </>
                )
                break;
        }
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        const form = e.target;
        const formData = {};

        Array.from(form.elements).forEach((element) => {
            if (element.name) {
                if (element.value === "false") {
                    formData[element.name] = 0
                }
                else if (element.value === "false") {
                    formData[element.name] = 0
                }

                else if (element.name.includes('min') || element.name.includes('max')) {
                    const fieldName = element.name.replace(/min|max/, '');
                    let temp = formData[fieldName]
                    if (typeof(temp) === "undefined") { temp = [0, 9999] }
                    if (element.name.includes('min')) {
                        temp[0] = Number(element.value)
                    } else {
                        temp[1] = Number(element.value)
                    }
                    if (temp[1] === 0) {temp[1]=9999}
                    formData[fieldName] = temp;
                } else if (element.type === 'select-multiple') {
                    formData[element.name] = Array.from(element.selectedOptions).map(option => option.value);
                } else {
                    formData[element.name] = element.value;
                }
            }
        });
        filterJsonCB(filterType, formData)
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <button type="submit" style={{margin:"10px 0px 10px 0px"}}>Filter parts</button>
                <table>
                    <thead>
                        <tr>
                        </tr>
                    </thead>
                    <tbody >
                        {keys.map((key, index) => (
                            <tr key={index}>
                                <td>{key}</td>
                                <td>{createField(key, filter[key])}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </form>
        </div>
    );
}

const Filter = (props) => {
    const partType = props.partType
    const filterCB = props.filterCB

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            {createFilter(partType, filterCB)}
        </div>
    )
}

export default Filter
