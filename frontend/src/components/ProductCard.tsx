import { Link } from 'react-router-dom'
import type { Product } from '@/types'
import { useTrack } from '@/lib/useTrack'


export default function ProductCard({ p, userId }: { p: Product; userId: number }) {
const { track } = useTrack(userId)
return (
<div className="rounded-2xl shadow p-4 hover:shadow-lg transition">
<Link to={`/product/${p.id}`} onClick={() => track('click', p.id)}>
<img src={p.image_url || '/placeholder.png'} alt={p.title} className="w-full h-40 object-cover rounded-xl mb-3" />
</Link>
<div className="text-sm text-gray-500">{p.brand}</div>
<div className="font-medium mb-2 line-clamp-2">{p.title}</div>
<div className="mb-3">{(p.price_cents/100).toFixed(2)} {p.currency}</div>
<div className="flex gap-2">
<Link className="text-blue-600 text-sm" to={`/product/${p.id}`}>View</Link>
<button className="text-sm" onClick={() => track('add_to_cart', p.id)}>Add to Cart</button>
</div>
</div>
)
}