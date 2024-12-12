import { BrowserRouter, Route, Routes } from "react-router-dom"
import Build from "./pages/Build.jsx"

function App() {

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/">
                    <Route index element={<Build />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App
