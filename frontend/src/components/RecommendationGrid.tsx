import { useEffect, useState } from 'react'
import { getRecommendations, getProduct, searchProducts } from '@/lib/api'
import type { Product } from '@/types'

export default function RecommendationGrid({ userId }: { userId: number }) {
  const [items, setItems] = useState<Product[]>([])

  useEffect(() => {
    let cancelled = false

    const simulateReco = async () => {
      const lastId = localStorage.getItem('lastClickedProduct')
      if (lastId) {
        const product = await getProduct(Number(lastId))
        if (product.category_id) {
          const sameCategory = await searchProducts('', product.category_id, 12, 0)
          if (!cancelled) {
            setItems([product, ...sameCategory.filter(p => p.id !== product.id)])
            return
          }
        }
      }

      try {
        const recs = await getRecommendations(userId)
        if (!cancelled) setItems(recs.map(r => r.product))
      } catch {
        const fallback = await searchProducts('')
        if (!cancelled) setItems(fallback)
      }
    }

    simulateReco()
    return () => { cancelled = true }
  }, [userId])

  return (
    <div className="mt-8">
      <h2 className="text-xl font-semibold mb-4">You Might Also Like</h2>

      <div className="flex space-x-6 overflow-x-auto scrollbar-hide pb-4">
        {items.map((p) => (
          <div key={p.id} className="min-w-[180px] flex-shrink-0">
            <div className="bg-white rounded-lg shadow hover:shadow-md transition p-3">
              <img
                src={p.image_url}
                alt={p.title}
                className="w-full h-32 object-contain mb-3"
              />
              <h3 className="text-sm font-medium line-clamp-2 mb-1">{p.title}</h3>
              <p className="text-gray-700 font-semibold text-sm mb-1">
                GH₵{(p.price_cents / 100).toLocaleString()}
              </p>
              <div className="flex items-center text-yellow-500 text-xs mb-2">
                {"★".repeat(5)} {/* Dummy 5-star rating */}
              </div>
              <button className="w-full bg-blue-600 text-white text-xs py-1.5 rounded hover:bg-blue-700">
                Add to Cart
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
