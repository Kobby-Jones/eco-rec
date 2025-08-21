import { useEffect, useState } from 'react'
import { getRecommendations } from '@/lib/api'
import type { Product } from '@/types'
import ProductCard from './ProductCard'


export default function RecommendationGrid({ userId }: { userId: number }) {
const [items, setItems] = useState<{product: Product; score: number}[]>([])
useEffect(() => { getRecommendations(userId).then(setItems) }, [userId])
return (
<div className="grid grid-cols-2 md:grid-cols-4 gap-4">
{items.map(({ product }) => (
<ProductCard key={product.id} p={product} userId={userId} />
))}
</div>
)
}