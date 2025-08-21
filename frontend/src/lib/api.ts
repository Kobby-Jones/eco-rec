import axios from 'axios'
import type { Product } from '../types'


const api = axios.create({
baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000',
withCredentials: true,
})


export async function getRecommendations(userId: number, k=12) {
const { data } = await api.get('/api/recommendations', { params: { user_id: userId, k } })
return data as { product: Product; score: number }[]
}
export async function getProduct(id: number) {
const { data } = await api.get(`/api/products/${id}`)
return data as Product
}
export async function searchProducts(query?: string, category_id?: number, limit=24, offset=0) {
const { data } = await api.get('/api/products', { params: { query, category_id, limit, offset } })
return data as Product[]
}
export async function logInteraction(payload: {
user: number; product: number; type: 'impression'|'view'|'click'|'add_to_cart'|'purchase'|'rating'; value?: number; context?: any;
}) {
await api.post('/api/interactions', payload)
}