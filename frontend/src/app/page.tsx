'use client';

import { useState, useEffect } from 'react';
import { MapPin } from 'lucide-react';
import Hero from '@/components/Hero';
import ShopCard from '@/components/ShopCard';
import MapModal from '@/components/MapModal';
import { searchNearby } from '@/services/api';
import { Shop } from '@/types';

export default function Home() {
  const [isMapOpen, setIsMapOpen] = useState(false);
  const [shops, setShops] = useState<Shop[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Default location (India - Delhi)
  const [location, setLocation] = useState<{ lat: number; lng: number }>({ lat: 28.6139, lng: 77.2090 });

  useEffect(() => {
    // Try to get user's location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
        },
        (error) => {
          console.log("Geolocation permission denied or error, using default (India)");
        }
      );
    }

    // Initial load - maybe generic search or popular shops
    handleSearch('batteries'); // Demo initial search
  }, []);

  const handleSearch = async (query: string) => {
    setLoading(true);
    setSearchQuery(query);
    try {
      // In a real app, get user's actual location
      const results = await searchNearby(query, location.lat, location.lng);
      setShops(results);
    } catch (error) {
      console.error("Search failed", error);
    } finally {
      setLoading(false);
    }
  };

  const handleMapClick = (lat: number, lng: number) => {
    setLocation({ lat, lng });
    // Optional: Trigger search immediately or just update location context
    if (searchQuery) {
      handleSearch(searchQuery);
    }
  };

  return (
    <main className="min-h-screen bg-white">
      <Hero onSearch={handleSearch} />

      {/* Shops Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex justify-between items-end mb-8">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 mb-2">
              {searchQuery ? `Results for "${searchQuery}"` : 'Nearby Shops'}
            </h2>
            <p className="text-slate-500">
              {shops.length > 0
                ? `Found ${shops.length} shops near you`
                : 'Search for items to find shops'}
            </p>
          </div>
          <button
            onClick={() => setIsMapOpen(true)}
            className="flex items-center gap-2 text-[#E50914] font-bold hover:underline"
            disabled={shops.length === 0 && !searchQuery} // Allow opening map even if no shops, to pick location
          >
            <MapPin className="w-5 h-5" />
            View on Map
          </button>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-80 bg-slate-100 rounded-2xl animate-pulse"></div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {shops.map((shop) => (
              <ShopCard key={shop.id} data={shop} />
            ))}
          </div>
        )}

        {!loading && shops.length === 0 && (
          <div className="text-center py-20 bg-slate-50 rounded-3xl">
            <p className="text-xl text-slate-500 font-medium">No shops found matching your search.</p>
            <p className="text-slate-400 mt-2">Try searching for "batteries", "milk", or "coffee".</p>
          </div>
        )}
      </section>

      {/* Map Modal */}
      <MapModal
        isOpen={isMapOpen}
        onClose={() => setIsMapOpen(false)}
        shops={shops}
        center={[location.lat, location.lng]}
        onMapClick={handleMapClick}
      />
    </main>
  );
}
