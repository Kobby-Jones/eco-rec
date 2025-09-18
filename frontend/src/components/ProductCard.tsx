import { useState } from 'react'
import { Link } from 'react-router-dom'
import type { Product } from '@/types'
import { useTrack } from '@/lib/useTrack'

export default function ProductCard({ p, userId }: { p: Product; userId: number }) {
  const { track } = useTrack(userId)
  const [src, setSrc] = useState(p.image_url || '/placeholder.png')

  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition flex flex-col items-center p-4">
      <Link
        to={`/product/${p.id}`}
        onClick={() => track('click', p.id, p.category_id)}
        className="w-full flex justify-center"
      >
        <img
          src={src}
          alt={p.title}
          className="w-full h-40 object-contain mb-3"
          onError={() => setSrc('/placeholder.png')}
          loading="lazy"
        />
      </Link>

      {/* Title */}
      <h3 className="text-sm font-medium text-gray-800 text-center mb-1">
        {p.title}
      </h3>

      {/* Price */}
      <p className="text-gray-900 font-semibold mb-1">
        GH₵{(p.price_cents / 100).toLocaleString()}
      </p>

      {/* Stars */}
      <div className="flex items-center text-yellow-500 text-sm mb-2">
        {"★".repeat(5)}
      </div>

      {/* Add to Cart */}
      <button
        className="w-full bg-blue-600 text-white text-sm font-medium py-2 rounded-md hover:bg-blue-700 transition"
        onClick={() => track('add_to_cart', p.id)}
      >
        Add to Cart
      </button>
    </div>
  )
}
