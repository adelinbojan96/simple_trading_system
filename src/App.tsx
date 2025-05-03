import './App.css'
import stockImage from './assets/stock_image.png'

function App() {
    return (
        <>
            <div className="background-container">
                <img src={stockImage} alt="Background" />
            </div>

            <h1>Trading Platform</h1>
            <h2 style={{ fontWeight: 200, fontSize: '1.25rem', color: '#888' }}>
                Where every order counts.
            </h2>

            <div className="card">
                {/* Content here */}
            </div>
        </>
    )
}

export default App
