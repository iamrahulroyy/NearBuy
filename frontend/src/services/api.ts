import axios from 'axios';
import { Shop, SearchResponse } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8050/api/v1';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchNearby = async (
  query: string,
  lat: number,
  lon: number,
  radiusKm: number = 5
): Promise<Shop[]> => {
  try {
    const response = await api.get('/search/nearby', {
      params: {
        q: query,
        lat,
        lon,
        radius_km: radiusKm
      }
    });

    // Transform Typesense response to Shop interface
    // The backend returns `body` which contains `hits`
    // Based on search.py: return send_json_response(..., body=shop_results['hits'])
    const hits: SearchResponse[] = response.data.body || [];

    return hits.map(hit => ({
      id: hit.document.shop_id, // or hit.document.id depending on backend indexing
      shopName: hit.document.shopName,
      fullName: hit.document.fullName,
      address: hit.document.address,
      latitude: hit.document.location[0],
      longitude: hit.document.location[1],
      is_open: true, // Default or fetch if available
      distance: '0.5km' // You might want to calculate this or extract from sort info
    }));
  } catch (error) {
    console.error('Error searching nearby:', error);
    return [];
  }
};

export default api;
