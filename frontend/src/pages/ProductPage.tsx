import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getProduct } from '@/lib/api'
import type { Product } from '@/types'
import { useTrack } from '@/lib/useTrack'


export default function ProductPage() {
const { id } = useParams()
const [p, setP] = useState<Product | null>(null)
const { track } = useTrack(1)
useEffect(() => { if (id) getProduct(+id).then(setP) }, [id])
useEffect(() => { if (p) track('view', p.id) }, [p])
if (!p) return null
return (
<div className="p-2">
<img src={p.image_url || '/placeholder.png'} className="w-full max-w-xl rounded-2xl mb-6" />
<h1 className="text-3xl font-semibold mb-2">{p.title}</h1>
<div className="text-gray-500 mb-4">{p.brand}</div>
<div className="mb-6">{(p.price_cents/100).toFixed(2)} {p.currency}</div>
<p className="max-w-3xl">{p.description}</p>
</div>
)
}