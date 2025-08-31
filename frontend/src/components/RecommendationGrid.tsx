import { useEffect, useState } from 'react'
import { getRecommendations, searchProducts } from '@/lib/api'
import type { Product } from '@/types'
import ProductCard from './ProductCard'

export default function RecommendationGrid({ userId }: { userId: number }) {
  const [items, setItems] = useState<{product: Product; score: number}[]>([])
  const [fallback, setFallback] = useState<Product[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        const recs = await getRecommendations(userId)
        if (!cancelled) {
          console.log('recs', recs)            // <— DEBUG
          setItems(recs)
        }
        if ((!recs || recs.length === 0) && !cancelled) {
          const products = await searchProducts('')
          if (!cancelled) setFallback(products)
        }
      } catch (e: any) {
        console.error('Reco error:', e)
        setError(String(e?.message || e))
        const products = await searchProducts('')
        if (!cancelled) setFallback(products)
      }
    })()
    return () => { cancelled = true }
  }, [userId])

  const cards = items.length > 0 ? items.map(({ product }) => product) : fallback

  return (
    <div className="space-y-3">
      {/* DEBUG PANEL */}
      <pre className="text-xs bg-gray-50 p-2 rounded border">
        items: {items.length} | fallback: {fallback.length} | error: {error ?? 'none'}
      </pre>

      {/* TEMP: render plain <img> tags to guarantee we see requests in “Img” */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {cards.slice(0, 8).map((p) => (
          <img
            key={p.id}
            src={p.image_url || '/placeholder.png'}
            onError={(e) => { (e.currentTarget as HTMLImageElement).src = '/placeholder.png' }}
            alt={p.title}
            className="w-full h-40 object-cover rounded-xl bg-gray-100"
            loading="lazy"
          />
        ))}
      </div>

      {/* ORIGINAL CARD GRID (can keep or re-enable after test) */}
      {/* <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {cards.map((p) => <ProductCard key={p.id} p={p} userId={userId} />)}
      </div> */}
    </div>
  )
}
