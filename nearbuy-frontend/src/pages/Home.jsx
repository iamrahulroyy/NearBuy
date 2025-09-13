// src/pages/Home.jsx
import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Link } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8059/api/v1';

const Home = () => {
  const [query, setQuery] = useState('');
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);
  const [shops, setShops] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Get user's current location on page load
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLatitude(position.coords.latitude);
        setLongitude(position.coords.longitude);
      },
      (error) => {
        console.error("Geolocation error:", error);
        setMessage("Geolocation is not available. Please allow location access.");
      }
    );
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    try {
      if (!latitude || !longitude) {
        setMessage('Please enable location services to search nearby shops.');
        setLoading(false);
        return;
      }
      const response = await axios.get(`${API_BASE_URL}/search/nearby`, {
        params: { q: query, lat: latitude, lon: longitude, radius_km: 5 },
      });
      setShops(response.data.body);
      setMessage(response.data.message);
    } catch (error) {
      console.error('Search failed:', error);
      setMessage(error.response?.data?.detail || 'An error occurred during search.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <header className="flex justify-between items-center py-6">
        <h1 className="text-3xl font-bold text-gray-800">NearBuy</h1>
        <div>
          <Link to="/login" className="mr-4 text-gray-600 hover:text-gray-900">Login</Link>
          <Link to="/signup">
            <Button>Sign Up</Button>
          </Link>
        </div>
      </header>

      <main className="my-8">
        <div className="flex justify-center items-center">
          <form onSubmit={handleSearch} className="flex w-full max-w-xl space-x-2">
            <Input
              type="text"
              placeholder="Search for an item..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="flex-grow"
            />
            <Button type="submit" disabled={loading}>
              {loading ? 'Searching...' : 'Search Nearby'}
            </Button>
          </form>
        </div>
        <div className="my-8 text-center text-gray-500">
          {message && <p>{message}</p>}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {shops.map((hit) => {
            const doc = hit.document;
            const shop = doc.shop_id; // The response format has changed, adjust accordingly
            return (
              <Card key={shop.shop_id}>
                <CardHeader>
                  <CardTitle>{doc.shopName}</CardTitle>
                  <CardDescription>{doc.address}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm">Item: {doc.itemName}</p>
                  <p className="text-sm">Price: ₹{doc.price}</p>
                </CardContent>
                <CardFooter>
                  <Button variant="outline">View Shop</Button>
                </CardFooter>
              </Card>
            );
          })}
        </div>
      </main>
    </div>
  );
};

export default Home;