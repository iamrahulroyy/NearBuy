'use client';

import { useState, useEffect, useRef } from 'react';
import { MapPin } from 'lucide-react';
import Hero from '@/components/Hero';
import ShopCard from '@/components/ShopCard';
import MapModal from '@/components/MapModal';
import LocationRequest from '@/components/LocationRequest';
import { searchNearby } from '@/services/api';
import { Shop } from '@/types';

export default function Home() {
  const [isMapOpen, setIsMapOpen] = useState(false);
  const [shops, setShops] = useState<Shop[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRadius, setSelectedRadius] = useState(5); // Default 5km
  const resultsRef = useRef<HTMLElement>(null);

  // Location State
  const [location, setLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [showLocationPrompt, setShowLocationPrompt] = useState(false);

  useEffect(() => {
    // Check if we already have a location saved in session
    const savedLoc = localStorage.getItem('user_location');
    if (savedLoc) {
      setLocation(JSON.parse(savedLoc));
    } else {
      // Only show prompt if we don't have a location
      setShowLocationPrompt(true);
    }
  }, []);

  const handleAllowLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const newLoc = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          setLocation(newLoc);
          localStorage.setItem('user_location', JSON.stringify(newLoc));
          setShowLocationPrompt(false);
        },
        (error) => {
          console.error("Geolocation error:", error);
          // If denied by browser after clicking allow, maybe show manual picker or default
          // For now, we'll fall back to default but keep the prompt hidden or show an error
          alert("Could not get location. Please enable it in your browser settings.");
          // Optionally fall back to default location
          handleDenyLocation();
        }
      );
    } else {
      alert("Geolocation is not supported by this browser.");
      handleDenyLocation();
    }
  };

  const handleDenyLocation = () => {
    // User denied or error. Set default location (Agartala)
    const defaultLoc = { lat: 23.8315, lng: 91.2868 };
    setLocation(defaultLoc);
    setShowLocationPrompt(false);
    // We don't save default location to localStorage so we ask again next time? 
    // Or maybe we do. Let's not save it so they have a chance to allow next time.
  };

  const handleSearch = async (query: string, radius?: number) => {
    if (!location) return;

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
    if (searchQuery) {
      handleSearch(searchQuery, distance);
    }
  };

  const handleMapClick = (lat: number, lng: number) => {
    setLocation({ lat, lng });
    if (searchQuery) {
      handleSearch(searchQuery);
    }
  };

  // Control body overflow to prevent scrolling when no search results
  useEffect(() => {
    if (!searchQuery) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'auto';
    }

    // Cleanup on unmount
    return () => {
      document.body.style.overflow = 'auto';
    };
  }, [searchQuery]);

  return (
    <main className="min-h-screen bg-white relative">
      {/* Location Permission Modal Overlay */}
      {showLocationPrompt && (
        <LocationRequest onAllow={handleAllowLocation} onDeny={handleDenyLocation} />
      )}

      <Hero
        onSearch={(q) => handleSearch(q)}
        radius={selectedRadius}
        onRadiusChange={handleDistanceChange}
      />

      {/* Shops Section */}
      <section ref={resultsRef} className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        {searchQuery && (
          <>
            <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-4 mb-8">
              <div className="flex-1">
                <h2 className="text-2xl md:text-3xl font-bold text-slate-900 mb-2">
                  Results for "{searchQuery}"
                </h2>
                <p className="text-sm md:text-base text-slate-500">
                  {shops.length > 0
                    ? `Found ${shops.length} shops near you`
                    : 'Search for items to find shops'}
                </p>
              </div>
              <button
                onClick={() => setIsMapOpen(true)}
                className="flex items-center justify-center gap-2 text-[#FF6B35] font-bold hover:underline bg-orange-50 hover:bg-orange-100 px-4 py-2.5 rounded-full transition-colors self-start md:self-auto"
                disabled={shops.length === 0}
              >
                <MapPin className="w-4 h-4 md:w-5 md:h-5" />
                <span className="text-sm md:text-base">View on Map</span>
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
        center={location ? [location.lat, location.lng] : [23.8315, 91.2868]}
        onMapClick={handleMapClick}
      />
    </main>
  );
}
