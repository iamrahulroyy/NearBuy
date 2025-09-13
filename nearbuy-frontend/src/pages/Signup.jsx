// src/pages/Signup.jsx
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import api from '../lib/api';
import { useAuth } from '../context/AuthContext';

const Signup = () => {
  const [role, setRole] = useState('user');
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    shopName: '',
    address: '',
    contact: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    let endpoint = '';
    let payload = {};
    if (role === 'user') {
      endpoint = '/users/signup/user';
      payload = { fullName: formData.fullName, email: formData.email, password: formData.password };
    } else if (role === 'vendor') {
      endpoint = '/users/signup/vendor';
      // The backend expects specific fields for a vendor signup
      payload = {
        fullName: formData.fullName,
        email: formData.email,
        password: formData.password,
        shopName: formData.shopName,
        address: formData.address,
        contact: formData.contact,
        // The backend `ShopCreate` schema has lat/lon. For simplicity, we can
        // prompt the user to add this later in the dashboard or set a default.
        latitude: 20.2961, // Example default
        longitude: 85.8245, // Example default
        is_open: true,
      };
    }

    try {
      const response = await api.post(endpoint, payload);
      if (response.status === 201) {
        alert(response.data.message);
        navigate('/login');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'An unexpected error occurred during registration.');
    } finally {
      setLoading(false);
    }
  };

  if (user) {
    return <Navigate to="/dashboard" />;
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl">Sign Up</CardTitle>
          <CardDescription>
            Choose your account type and fill in the details.
          </CardDescription>
          {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        </CardHeader>
        <CardContent className="grid gap-4">
          <form onSubmit={handleSubmit}>
            <div className="grid gap-2">
              <Label>Account Type</Label>
              <Select value={role} onValueChange={setRole}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="user">User</SelectItem>
                  <SelectItem value="vendor">Vendor</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="grid gap-2 mt-4">
              <Label htmlFor="fullName">Full Name</Label>
              <Input id="fullName" value={formData.fullName} onChange={handleInputChange} />
            </div>
            <div className="grid gap-2 mt-4">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" value={formData.email} onChange={handleInputChange} />
            </div>
            <div className="grid gap-2 mt-4">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" value={formData.password} onChange={handleInputChange} />
            </div>
            {role === 'vendor' && (
              <>
                <div className="grid gap-2 mt-4">
                  <Label htmlFor="shopName">Shop Name</Label>
                  <Input id="shopName" value={formData.shopName} onChange={handleInputChange} />
                </div>
                <div className="grid gap-2 mt-4">
                  <Label htmlFor="address">Shop Address</Label>
                  <Input id="address" value={formData.address} onChange={handleInputChange} />
                </div>
                <div className="grid gap-2 mt-4">
                  <Label htmlFor="contact">Contact</Label>
                  <Input id="contact" value={formData.contact} onChange={handleInputChange} />
                </div>
              </>
            )}
            <Button type="submit" className="w-full mt-6" disabled={loading}>
              {loading ? 'Signing Up...' : 'Sign Up'}
            </Button>
          </form>
        </CardContent>
        <div className="text-center text-sm mb-4">
          Already have an account? <Link to="/login" className="underline">Log in</Link>
        </div>
      </Card>
    </div>
  );
};

export default Signup;