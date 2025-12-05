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
    // The backend returns `body` which contains enhanced hits with distance
    const hits: any[] = response.data.body || [];

    return hits.map(hit => {
      const distance_km = hit.distance_km || 0;
      const distance_formatted = distance_km < 1
        ? `${Math.round(distance_km * 1000)} m`
        : `${distance_km.toFixed(1)} km`;

      return {
        id: hit.document.shop_id,
        shopName: hit.document.shopName,
        fullName: hit.document.fullName,
        address: hit.document.address,
        latitude: hit.document.location[0],
        longitude: hit.document.location[1],
        is_open: true,
        distance: distance_formatted,
        distance_km: distance_km
      };
    });
  } catch (error) {
    console.error('Error searching nearby:', error);
    return [];
  }
};

export const getSuggestions = async (
  lat: number,
  lon: number,
  radiusKm: number = 10
): Promise<string[]> => {
  try {
    const response = await api.get('/search/suggestions', {
      params: {
        lat,
        lon,
        radius_km: radiusKm
      }
    });

    return response.data.body || [];
  } catch (error) {
    console.error('Error fetching suggestions:', error);
    return [];
  }
};

// Analytics API
export const getAnalyticsStats = async () => {
  try {
    const response = await axios.get(`${API_URL}/analytics/stats`);
    return response.data;
  } catch (error) {
    console.error('Error fetching analytics stats:', error);
    throw error;
  }
};

export default api;
