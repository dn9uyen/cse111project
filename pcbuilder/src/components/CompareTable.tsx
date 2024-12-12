import { useEffect, useState } from "react";

const CompareTable = (props: any) => {
    const rows = props.rows

    let cols = [];
    if (rows.length > 0) {
        cols = Object.keys(rows[0]); // Get column names
    }
    let partIdStr = cols.filter(str => str.includes("id"))

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
            <h3>Comparison table</h3>
            <table style={{ borderCollapse: 'collapse', width: '100%', marginTop: '20px' }}>
                <thead>
                    <tr style={{ border: '1px solid black', borderLeft: '1px solid black', borderRight:'1px solid black' }}>
                        {/* Checkbox column */}
                        {cols.length > 1 ? (<th style={{ padding: '20px 20px 0px 0px', textAlign: 'left' }}></th>) : <></>}
                        {/* Create column names */}
                        {hideId()}
                    </tr>
                </thead>
                <tbody>
                    {/* Create each row */}
                    {rows.map((row, index) => (
                        <tr style={{ borderBottom: '1px solid black', borderLeft: '1px solid black', borderRight:'1px solid black' }} key={index}>
                            <td style={{ padding: "10px" }}>
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
export default CompareTable
