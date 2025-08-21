import type { Product } from '@/types'
import ProductCard from './ProductCard'
export default function ProductList({ products, userId }:{products:Product[]; userId:number}) {
return (
<div className="grid grid-cols-2 md:grid-cols-4 gap-4">
{products.map(p => <ProductCard key={p.id} p={p} userId={userId} />)}
</div>
)
}