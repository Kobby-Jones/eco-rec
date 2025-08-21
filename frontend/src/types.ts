export type Product = {
    id: number; sku: string; title: string; description?: string;
    price_cents: number; currency: string; brand?: string;
    image_url?: string; attributes?: Record<string,any>; category_id?: number;
    }