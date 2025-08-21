import RecommendationGrid from '@/components/RecommendationGrid'
export default function Home() {
const userId = 1
return (
<div className="p-2">
<h1 className="text-2xl font-semibold mb-4">Recommended for you</h1>
<RecommendationGrid userId={userId} />
</div>
)
}