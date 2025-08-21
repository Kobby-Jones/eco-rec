import { useCallback } from 'react'
import { logInteraction } from './api'
export function useTrack(userId: number) {
const track = useCallback((type: string, productId: number, value?: number, context?: any) => {
logInteraction({ user: userId, product: productId, type: type as any, value, context })
}, [userId])
return { track }
}