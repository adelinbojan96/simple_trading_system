import './App.css'
import stockImage from './assets/stock_image.png'
import axios from 'axios'
import { useState } from 'react'

function App() {
    const [price, setPrice] = useState('')
    const [stock, setStock] = useState('AAPL')
    const [currency, setCurrency] = useState('$')

    const handleBuy = async () => {
        try {
            await axios.post('http://localhost:8000/api/place_order/', {
                user_id: 'current_user',
                side: 'buy',
                amount: 1,
                price: parseFloat(price),
                stock,
                currency
            })
            console.log('buy request was sent')
        } catch (error) {
            console.error('buy request failed:', error)
        }
    }

    const handleSell = async () => {
        try {
            await axios.post('http://localhost:8000/api/place_order/', {
                user_id: 'current_user',
                side: 'sell',
                amount: 1,
                price: parseFloat(price),
                stock,
                currency
            })
            console.log('Sell request sent')
        } catch (error) {
            console.error('Sell failed:', error)
        }
    }

    return (
        <>
            <div className="background-container">
                <img src={stockImage} alt="Background" />
            </div>

            <h1>Trading Platform</h1>
            <h2 className="subtitle">Where every order counts.</h2>

            <div className="card">
                <input
                    type="number"
                    placeholder="Enter price"
                    className="price-input"
                    value={price}
                    onChange={e => setPrice(e.target.value)}
                />

                <select
                    className="stock-dropdown"
                    value={stock}
                    onChange={e => setStock(e.target.value)}
                >
                    <option value="AAPL">Apple (AAPL)</option>
                    <option value="TSLA">Tesla (TSLA)</option>
                    <option value="GOOG">Google (GOOG)</option>
                    <option value="MSFT">Microsoft (MSFT)</option>
                    <option value="AMZN">Amazon (AMZN)</option>
                </select>

                <select
                    className="currency-dropdown"
                    value={currency}
                    onChange={e => setCurrency(e.target.value)}
                >
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