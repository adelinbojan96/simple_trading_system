import './App.css'
import stockImage from './assets/stock_image.png'

function App() {
    const handleBuy = () => {
        // TODO: write logic here
        console.log('Buy clicked')
    }

    const handleSell = () => {
        // TODO: write logic here
        console.log('Sell clicked')
    }

    return (
        <>
            <div className="background-container">
                <img src={stockImage} alt="Background" />
            </div>

            <h1>Trading Platform</h1>
            <h2 className="subtitle">Where every order counts.</h2>

            <div className="card">
                <input type="number" placeholder="Enter price" className="price-input" />

                <select className="stock-dropdown">
                    <option value="AAPL">Apple (AAPL)</option>
                    <option value="TSLA">Tesla (TSLA)</option>
                    <option value="GOOG">Google (GOOG)</option>
                    <option value="MSFT">Microsoft (MSFT)</option>
                    <option value="AMZN">Amazon (AMZN)</option>
                </select>

                <select className="currency-dropdown">
                    <option value="€">Euro (€)</option>
                    <option value="$">Dollar ($)</option>
                    <option value="£">Pound (£)</option>
                </select>

                <div className="button-group">
                    <button className="buy-button" onClick={handleBuy}>Buy</button>
                    <button className="sell-button" onClick={handleSell}>Sell</button>
                </div>
            </div>
        </>
    )
}

export default App