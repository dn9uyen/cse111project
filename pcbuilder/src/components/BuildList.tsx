import { useEffect, useState } from "react"

const BuildList = (props: any) => {
    const [parts, setParts] = useState(props.parts)
    const buildCB = props.buildCB
    useEffect(() => { console.log(parts, "child") }, [parts])
    const calculateTotal = () => {
        let total = (parts["cpu"][2] || 0) + (parts["cooler"][2] || 0) + (parts["ram"][2] || 0) + (parts["motherboard"][2] || 0) + (parts["gpu"][2] || 0) + (parts["storage"][2] || 0) + (parts["psu"][2] || 0)
        return <div>{total}</div>
    }
    return (
        <div>
            <table style={{ borderCollapse: 'collapse', width: '100%' }}>
                <thead>
                    <tr style={{ borderBottom: '1px solid black' }}>
                        <th style={{ padding: '20px', textAlign: 'left' }}>Choose Part</th>
                        <th style={{ padding: '20px 50vw 20px 20px', textAlign: 'left' }}>Selection</th>
                        <th style={{ padding: '20px', textAlign: 'left' }}>Price</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style={{ borderBottom: '1px solid black' }}>
                        <td style={{ padding: '10px 5vw 10px 20px' }}><button onClick={() => buildCB("ChoosePart", "cpu")}>Choose CPU</button></td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["cpu"][1]}</td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["cpu"][2]}</td>
                    </tr>
                    <tr style={{ borderBottom: '1px solid black' }}>
                        <td style={{ padding: '10px 5vw 10px 20px' }}><button onClick={() => buildCB("ChoosePart", "cooler")}>Choose CPU cooler</button></td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["cooler"][1]}</td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["cooler"][2]}</td>
                    </tr>
                    <tr style={{ borderBottom: '1px solid black' }}>
                        <td style={{ padding: '10px 5vw 10px 20px' }}><button onClick={() => buildCB("ChoosePart", "ram")}>Choose RAM</button></td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["ram"][1]}</td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["ram"][2]}</td>
                    </tr>
                    <tr style={{ borderBottom: '1px solid black' }}>
                        <td style={{ padding: '10px 5vw 10px 20px' }}><button onClick={() => buildCB("ChoosePart", "motherboard")}>Choose Motherboard</button></td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["motherboard"][1]}</td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["motherboard"][2]}</td>
                    </tr>
                    <tr style={{ borderBottom: '1px solid black' }}>
                        <td style={{ padding: '10px 5vw 10px 20px' }}><button onClick={() => buildCB("ChoosePart", "gpu")}>Choose GPU</button></td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["gpu"][1]}</td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["gpu"][2]}</td>
                    </tr> 
                    <tr style={{ borderBottom: '1px solid black' }}>
                        <td style={{ padding: '10px 5vw 10px 20px' }}><button onClick={() => buildCB("ChoosePart", "storage")}>Choose Storage</button></td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["storage"][1]}</td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["storage"][2]}</td>
                    </tr>
                    <tr style={{ borderBottom: '1px solid black' }}>
                        <td style={{ padding: '10px 5vw 10px 20px' }}><button onClick={() => buildCB("ChoosePart", "psu")}>Choose PSU</button></td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["psu"][1]}</td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{parts["psu"][2]}</td>
                    </tr>
                    <tr style={{ borderBottom: '1px solid black' }}>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>Total price</td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}></td>
                        <td style={{ padding: '10px 5vw 10px 20px' }}>{calculateTotal()}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    )

}

export default BuildList
