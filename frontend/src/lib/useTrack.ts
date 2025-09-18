export function useTrack(userId: number) {
    const track = (type: string, productId: number, category_id: number | undefined) => {
      // Existing interaction logging
      fetch('/api/interactions', {
        method: 'POST',
        body: JSON.stringify({ user: userId, product: productId, type }),
        headers: { 'Content-Type': 'application/json' },
      })
  
      // 👉 Save last clicked product
      if (type === 'click' || type === 'view') {
        localStorage.setItem('lastClickedProduct', String(productId))
      }
    }
    return { track }
  }
  