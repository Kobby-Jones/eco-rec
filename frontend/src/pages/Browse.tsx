import { useEffect, useState } from 'react'
import { searchProducts } from '@/lib/api'
import type { Product } from '@/types'
import ProductList from '@/components/ProductList'
export default function Browse() {
const [list, setList] = useState<Product[]>([])
useEffect(() => { searchProducts("").then(setList) }, [])
return (
<div className="p-2">
<h1 className="text-2xl font-semibold mb-4">Browse</h1>
<ProductList products={list} userId={1} />
</div>
)
}