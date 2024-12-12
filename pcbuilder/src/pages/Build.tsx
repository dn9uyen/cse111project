import { useEffect, useRef, useState } from "react";
import BuildList from "../components/BuildList";
import ChoosePart from "../components/ChoosePart";
import { addPartInfo, getCompatability, getPartInfo } from "../api";

export default function Build() {
    const [parts, setParts] = useState({
        // partId, model, price
        "cpu": [0, "", 0],
        "cooler": [0, "", 0],
        "ram": [0, "", 0],
        "motherboard": [0, "", 0],
        "gpu": [0, "", 0],
        "storage": [0, "", 0],
        "psu": [0, "", 0],
    }
    )
    const [loading, setLoading] = useState(true)

    const getBuildCodeInfo = async (buildCode) => {
        let info = {}
        const partNames = ["cpu", "cooler", "ram", "motherboard", "gpu", "storage", "psu"]
        try {
            for (let i = 0; i < buildCode.length; i++) {
                if (buildCode[i] === "0") {
                    info[partNames[i]] = [0, "", 0]
                    continue
                }
                let response = await getPartInfo(partNames[i], parseInt(buildCode[i]))
                setPartCB(partNames[i], response[`${partNames[i]}id`], response["model"], response["price"])
            }
        }
        catch (e) { }
        finally { setLoading(false) }
    }

    useEffect(() => {
        const params = new URLSearchParams(window.location.search)
        const keys = Array.from(params.keys())
        if (keys.length > 0) {
            const buildCode = params.get(keys[0])
            if (buildCode !== null && buildCode.length === 7) {
                const partIds = buildCode.split("")
                getBuildCodeInfo(partIds)
            }
        }
        else {
            setLoading(false)
        }

    }, [])

    const [pageState, setPageState] = useState("PartList")
    const [choosePartType, setChoosePartType] = useState("")
    const buildCB = (newPageState: any, newPartType: any) => {
        if (newPageState === "PartList") {
            setChoosePartType("");
        }
        setPageState(newPageState)
        setChoosePartType(newPartType)
    }

    const setPartCB = (partType, id, model, price) => {
        setParts((prev) => ({ ...prev, [partType]: [id, model, Number(price)] }))
    }


    const textBoxRef = useRef(null);
    const [link, setLink] = useState("")
    const handleLinkClick = () => {
        textBoxRef.current.select()
    }

    const handleSaveClick = () => {
        const buildCode = String(parts["cpu"][0] || 0) + String(parts["cooler"][0] || 0) + String(parts["ram"][0] || 0) + String(parts["motherboard"][0] || 0) + String(parts["gpu"][0] || 0) + String(parts["storage"][0] || 0) + String(parts["psu"][0] || 0)
        const baseUrl = "http://localhost:5173?buildCode="
        setLink(baseUrl + buildCode)
    }

    const [conflicts, setConflicts] = useState([])
    const handleCheckCompatability = async () => {
        const conflictsJson = await getCompatability({
            "cpuid": parts["cpu"][0],
            "ramid": parts["ram"][0],
            "motherboardid": parts["motherboard"][0],
            "psuid": parts["psu"][0],
            "gpuid": parts["gpu"][0],
            "storageid": parts["storage"][0],
            "coolerid": parts["cooler"][0],
        })
        setConflicts(conflictsJson.map(conflict => conflict[2]))
        console.log(conflicts)
    }

    // const [modIn, setModIn] = useState("")
    // const [modType, setModType] = useState("")
    // const modPart = () => {
    //         addPartInfo(modType, JSON.parse(modIn))
    //     return
    // }

    if (loading) {
        return (
            <h1>
                Loading build
            </h1>
        )
    }



    return (
        <div>
            <div style={{ display: 'flex', height: '100vh' }}>
                <div style={{ marginLeft: 'auto', marginRight: 'auto', paddingLeft: '20px' }}>
                    <h1>PC Builder</h1>
                    <table>
                        <tbody>
                            <tr>
                                {pageState === "PartList" ? (
                                    <>
                                        <td>
                                            <button onClick={handleSaveClick}>Save build</button>
                                        </td>
                                        <td>
                                            <input style={{ width: '240px', border: "1px solid slategray" }} ref={textBoxRef} type="text" value={link} readOnly onClick={handleLinkClick}
                                            />

                                        </td>
                                    </>
                                ) : <></>}
                            </tr>
                        </tbody>
                    </table>

                    <button onClick={handleCheckCompatability}>Check compatability</button>
                    {conflicts.length === 0 ? (
                        <p>No conflicts found</p>
                    ) :
                        conflicts.map((conflict, index) => (
                            <p key={index}>{conflict}</p>
                        ))

                    }
                    {pageState == "PartList" && <BuildList parts={parts} buildCB={buildCB} />}
                    {pageState == "ChoosePart" && <ChoosePart partType={choosePartType} buildCB={buildCB} setPartCB={setPartCB} />}
                    {/* Part type:<input onChange={(e) => setModType(e.target.value)}></input> */}
                    {/* Part info:<input style={{width: '600px'}} onChange={(e) => setModIn(e.target.value)}></input> */}
                    {/* <button onClick={modPart}>Add part</button> */}
                </div>
            </div>
        </div>
    )
}
