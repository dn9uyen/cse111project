import { useEffect, useState } from "react";

const PartTable = (props: any) => {
    const rows = props.rows
    const [checkedParts, setChecked] = useState([])
    const selectCB = props.selectCB

    const handleCheckboxChange = (e) => {
        const { value: partId, checked: isChecked } = e.target;
        if (isChecked) {
            setChecked((prevValues) => [...prevValues, +partId]);
        } else {
            setChecked((prevValues) => prevValues.filter((item) => item !== +partId)
            );
        }
    };

    let cols = [];
    if (rows.length > 0) {
        cols = Object.keys(rows[0]); // Get column names
    }
    let partIdStr = cols.filter(str => str.includes("id"))

    useEffect(() => {
        selectCB(checkedParts)
        console.log(rows)
    }, [checkedParts]);

    useEffect(() => {
        setChecked([])
    }, [rows])

    const formatData = (row, col) => {
        if (typeof row[col] === 'boolean') {
            return row[col] ? 'Yes' : 'No'
        }
        else if (Array.isArray(row[col])) {
            return row[col].join(", ")
        }
        else {
            return row[col]
        }
    }

    const hideId = () => {
        cols = cols.filter(str => !str.includes("id"))
        return (
            cols.map((column) => (
                <th style={{ padding: '0px 20px 10px 0px', textAlign: 'left' }} key={column}>{column}</th>
            )))
    }

    return (
        <div>
            <table style={{ borderCollapse: 'collapse', width: '100%', marginTop: '20px' }}>
                <thead>
                    <tr style={{ borderBottom: '1px solid black' }}>
                        {/* Checkbox column */}
                        {cols.length > 1 ? (<th style={{ padding: '0px 20px 10px 0px', textAlign: 'left' }}>Select</th>) : <></>}
                        {/* Create column names */}
                        {hideId()}
                    </tr>
                </thead>
                <tbody>
                    {/* Create each row */}
                    {rows.map((row, index) => (
                        <tr style={{ borderBottom: '1px solid black' }} key={index}>
                            {/* Checkbox */}
                            <td style={{ padding: "10px" }}>
                                <input type="checkbox" value={rows[index][partIdStr]} onChange={handleCheckboxChange} />
                            </td>
                            {/* Fill in columns with info */}
                            {cols.map((col) => (
                                <td style={{ padding: '0px 20px 0px 0px' }} key={col}>
                                    {formatData(row, col)}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
export default PartTable
