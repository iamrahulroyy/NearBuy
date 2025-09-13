// src/pages/ShopDashboard.jsx
import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';

const ShopDashboard = () => {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  if (!user) {
    return <div>Redirecting to login...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <header className="flex justify-between items-center py-6">
        <h1 className="text-3xl font-bold text-gray-800">Shop Dashboard</h1>
        <div className="flex items-center space-x-4">
          <span className="text-gray-600">Welcome, {user.fullName} ({user.role})</span>
          <Button onClick={handleLogout}>Logout</Button>
        </div>
      </header>
      <main className="my-8">
        <p>This is where vendors can manage their shop, items, and inventory.</p>
        <p className="mt-4">The backend provides endpoints for:</p>
        <ul className="list-disc list-inside mt-2">
          <li>Creating, updating, and viewing shop details.</li>
          <li>Adding, updating, and deleting items.</li>
          <li>Adding and managing inventory for each item.</li>
        </ul>
        <div className="mt-6 space-x-4">
          <Link to="/manage-shop">
            <Button>Manage Shop</Button>
          </Link>
          <Link to="/manage-items">
            <Button>Manage Items</Button>
          </Link>
          <Link to="/manage-inventory">
            <Button>Manage Inventory</Button>
          </Link>
        </div>
      </main>
    </div>
  );
};

export default ShopDashboard;