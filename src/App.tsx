import { useState, useEffect, JSX } from 'react'
import './App.css'
import stockImage from './assets/stock_image.png'
import axios from 'axios'

interface Order {
    stock: string
    price: number
}

interface Orders {
    buy: Record<string, Order>
    sell: Record<string, Order>
    cancelled: string[]
}

export default function App(): JSX.Element {
    const [userId, setUserId] = useState<string>('current_user')
    const [price, setPrice] = useState<string>('')
    const [stock, setStock] = useState<string>('AAPL')
    const [currency, setCurrency] = useState<string>('$')
    const [orders, setOrders] = useState<Orders>({ buy: {}, sell: {}, cancelled: [] })

    const fetchState = async (): Promise<void> => {
        try {
            const res = await axios.get<Orders>('http://localhost:8000/api/state/', {
                params: { user_id: userId }
            })
            setOrders(res.data)
        } catch (err) {
            console.error('Failed to fetch state:', err)
        }
    }

    useEffect(() => {
        fetchState()
    }, [userId])

    const handleBuy = async (): Promise<void> => {
        try {
            await axios.post('http://localhost:8000/api/place_order/', {
                user_id: userId,
                side: 'buy',
                price: parseFloat(price),
                stock,
                currency
            })
            await fetchState()
        } catch (error) {
            console.error('Buy failed:', error)
        }
    }

    const handleSell = async (): Promise<void> => {
        try {
            await axios.post('http://localhost:8000/api/place_order/', {
                user_id: userId,
                side: 'sell',
                price: parseFloat(price),
                stock,
                currency
            })
            await fetchState()
        } catch (error) {
            console.error('Sell failed:', error)
        }
    }

    const handleCancel = async (orderId: string): Promise<void> => {
        try {
            await axios.post('http://localhost:8000/api/cancel_order/', {
                user_id: userId,
                order_id: orderId
            })
            await fetchState()
        } catch (error) {
            console.error('Cancel failed:', error)
        }
    }

    const downloadCancelledOrders = (): void => {
        const data = JSON.stringify(orders.cancelled, null, 2)
        const blob = new Blob([data], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'cancelled_orders.json'
        a.click()
        URL.revokeObjectURL(url)
    }

    return (
        <>
            <div className="background-container">
                <img src={stockImage} alt="Background" style={{ opacity: 0.2 }} />
            </div>

            <h1>Trading Platform</h1>
            <h2 className="subtitle">Where every order counts.</h2>

            <div className="card">
                <input
                    type="text"
                    placeholder="Enter user id"
                    className="user-id-input"
                    value={userId}
                    onChange={e => setUserId(e.target.value)}
                />

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

                <h3>Active Orders</h3>
                <ul className="order-list">
                    {Object.entries(orders.buy).map(([id, order]) => (
                        <li key={id}>
                            {order.stock} @ {order.price}{currency}
                            <button className="cancel-button" onClick={() => handleCancel(id)}>
                                Cancel
                            </button>
                        </li>
                    ))}
                    {Object.entries(orders.sell).map(([id, order]) => (
                        <li key={id}>
                            {order.stock} @ {order.price}{currency} (Sell)
                            <button className="cancel-button" onClick={() => handleCancel(id)}>
                                Cancel
                            </button>
                        </li>
                    ))}
                </ul>

                <h3>Cancelled Orders</h3>
                <button className="cancel-button" onClick={downloadCancelledOrders}>
                    Download Cancelled Orders
                </button>
            </div>
        </>
    )
}