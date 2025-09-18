import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getProduct, searchProducts } from '@/lib/api'
import type { Product } from '@/types'
import { useTrack } from '@/lib/useTrack'
import ProductCard from '@/components/ProductCard'

export default function ProductPage() {
  const { id } = useParams()
  const [p, setP] = useState<Product | null>(null)
  const [related, setRelated] = useState<Product[]>([])
  const { track } = useTrack(1)

  // Load product
  useEffect(() => {
    if (id) {
      getProduct(+id).then((prod) => {
        setP(prod)
        // Fetch from same category
        if (prod.category_id) {
          searchProducts('', prod.category_id, 6, 0).then((prods) =>
            setRelated(prods.filter((x) => x.id !== prod.id))
          )
        }
      })
    }
  }, [id])

  // Track view
  useEffect(() => {
    if (p) track('view', p.id)
  }, [p])

  if (!p) return null

  return (
    <div className="p-4 max-w-3xl mx-auto">
      {/* Product Image */}
      <img
        src={p.image_url || '/placeholder.png'}
        alt={p.title}
        className="w-full rounded-2xl mb-6 object-contain bg-gray-100"
      />

      {/* Title + Price */}
      <h1 className="text-2xl font-semibold mb-2">{p.title}</h1>
      <p className="text-gray-600 mb-4">{p.brand}</p>
      <p className="text-lg font-semibold mb-6">
        GH₵{(p.price_cents / 100).toLocaleString()}
      </p>

      {/* Add to Cart */}
      <button
        className="w-full bg-blue-600 text-white text-lg font-medium py-3 rounded-md hover:bg-blue-700 transition mb-10"
        onClick={() => track('add_to_cart', p.id)}
      >
        Add to Cart
      </button>

      {/* Customers Also Bought */}
      {related.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold mb-4">Customers also bought</h2>
          <div className="flex space-x-4 overflow-x-auto pb-2">
            {related.map((rp) => (
              <div key={rp.id} className="min-w-[160px] flex-shrink-0">
                <ProductCard p={rp} userId={1} />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
