import { useState } from "react"
import { filterPart, getPartInfo } from "../api"
import Filter from "./Filter"
import PartTable from "./PartTable"
import CompareTable from "./CompareTable"

const ChoosePart = (props) => {
    const buildCB = props.buildCB
    const setPartCB = props.setPartCB
    const partType = props.partType
    const [rows, setRows] = useState([])
    const [isCompareDisabled, setIsCompareDisabled] = useState(true)
    const [isSelectDisabled, setIsSelectDisabled] = useState(true)
    const [filter, setFilter] = useState({})
    const [checkedParts, setCheckedParts] = useState([])
    const [comparing, setComparing] = useState(false)


    const selectCB = (_checkedParts) => {
        if (_checkedParts.length === 1) {
            setIsSelectDisabled(false)
            setIsCompareDisabled(true)
        } else { setIsSelectDisabled(true); setIsCompareDisabled(true) }
        if (_checkedParts.length > 1) {
            setIsCompareDisabled(false)
        }
        setCheckedParts(_checkedParts)
        return;
    }

    const filterCB = async (partType, formData) => {
        const jsonData = await filterPart(partType, formData)
        setRows(jsonData)
    }

    const handleSelect = async () => {
        let partInfo = await getPartInfo(partType, checkedParts[0])
        setPartCB(partType, checkedParts[0], partInfo["model"], partInfo["price"])
        buildCB("PartList")
    }

    // reset filter after compare

    return (
        <>
            <h3>Choose a {partType}</h3>
            <button onClick={() => buildCB("PartList")}>Back to part list</button>
            <button
                onClick={() => handleSelect()}
                disabled={isSelectDisabled}
                style={{
                    backgroundColor: isSelectDisabled ? '#d3d3d3' : '',
                    cursor: isSelectDisabled ? 'not-allowed' : 'pointer',
                    marginLeft: "17%"
                }}>Select part </button>
            <button
                onClick={() => setComparing((prev) => (!prev))}
                disabled={isCompareDisabled}
                style={{
                    backgroundColor: isCompareDisabled ? '#d3d3d3' : '',
                    cursor: isCompareDisabled ? 'not-allowed' : 'pointer',
                    marginLeft: "10px"
                }}>{comparing ? "Stop comparing" : "Compare parts"}</button>

            {comparing ? (<div style={{ marginLeft: '23%'}}> <CompareTable rows={rows.filter(row => checkedParts.includes(row[`${partType}id`]))} /> </div>) : (<></>)}
            <div style={{ display: 'flex', alignItems: 'flex-start' }}>
                <div style={{ marginRight: '3vw' }}>
                    <Filter partType={partType} filterCB={filterCB} />
                </div>
                <PartTable rows={rows} selectCB={selectCB} />
            </div >
        </>
    )

}

export default ChoosePart
