import { useEffect, useState } from 'react'
import ProductList from '@/components/ProductList'
import RecommendationGrid from '@/components/RecommendationGrid'
import { searchProducts } from '@/lib/api'
import type { Product } from '@/types'

export default function Home() {
  const userId = 1
  const [products, setProducts] = useState<Product[]>([])

  useEffect(() => {
    const loadProducts = async () => {
      const data = await searchProducts('', undefined, 12, 0) // fetch first 12 products
      setProducts(data)
    }
    loadProducts()
  }, [])

  return (
    <div className="p-2 space-y-10">
      {/* Top Product Listing */}
      <div>
        <h1 className="text-2xl font-semibold mb-4">Shop</h1>
        <ProductList products={products} userId={userId} />
      </div>

      {/* Recommended Section */}
      <div>
        <h2 className="text-2xl font-semibold mb-4">Recommended for you</h2>
        <RecommendationGrid userId={userId} />
      </div>
    </div>
  )
}
