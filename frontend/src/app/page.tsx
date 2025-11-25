'use client';

import { useState, useEffect, useRef } from 'react';
import { MapPin, Sparkles } from 'lucide-react';
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
  const [selectedRadius, setSelectedRadius] = useState(5); // Default 5km
  const resultsRef = useRef<HTMLElement>(null);

  // Default location (Agartala, Tripura)
  const [location, setLocation] = useState<{ lat: number; lng: number }>({ lat: 23.8315, lng: 91.2868 });

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
          console.log("Geolocation permission denied or error, using default (Agartala, Tripura)");
        }
      );
    }

    // Initial load - no auto search to show chips
    // handleSearch('batteries');
  }, []);

  const handleSearch = async (query: string, radius?: number) => {
    setLoading(true);
    setSearchQuery(query);

    // Scroll to results
    setTimeout(() => {
      resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);

    try {
      const searchRadius = radius !== undefined ? radius : selectedRadius;
      const results = await searchNearby(query, location.lat, location.lng, searchRadius);
      setShops(results);
    } catch (error) {
      console.error("Search failed", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDistanceChange = (distance: number) => {
    setSelectedRadius(distance);
    // Re-run search with new distance if there's an active query
    if (searchQuery) {
      handleSearch(searchQuery, distance);
    }
  };

  const handleMapClick = (lat: number, lng: number) => {
    setLocation({ lat, lng });
    // Optional: Trigger search immediately or just update location context
    if (searchQuery) {
      handleSearch(searchQuery);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    handleSearch(suggestion);
  };

  return (
    <main className="min-h-screen bg-white">
      <Hero
        onSearch={(q) => handleSearch(q)}
        radius={selectedRadius}
        onRadiusChange={handleDistanceChange}
      />

      {/* Shops Section */}
      <section ref={resultsRef} className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">

        {!searchQuery ? (
          <div className="py-8">
            {/* Empty state or additional marketing content could go here if needed, 
                 but for now we keep it clean as the Hero handles the main call to action. 
                 We can leave this empty or remove the conditional entirely if we want 
                 the shops list to be the only thing below hero. 
                 Actually, let's just show nothing here so the page is clean. */}
          </div>
        ) : (
          <>
            <div className="flex justify-between items-end mb-8">
              <div>
                <h2 className="text-3xl font-bold text-slate-900 mb-2">
                  Results for "{searchQuery}"
                </h2>
                <p className="text-slate-500">
                  {shops.length > 0
                    ? `Found ${shops.length} shops near you`
                    : 'Search for items to find shops'}
                </p>
              </div>
              <button
                onClick={() => setIsMapOpen(true)}
                className="flex items-center gap-2 text-[#FF6B35] font-bold hover:underline"
                disabled={shops.length === 0}
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
              </div>
            )}
          </>
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
