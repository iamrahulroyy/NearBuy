'use client';

import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useEffect } from 'react';

// Fix for default marker icon
const icon = L.icon({
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
});

interface Shop {
    document: {
        shopName: string;
        location: [number, number]; // [lat, lon]
        address: string;
        contact?: string;
    };
    geo_distance_meters?: number; // Typesense might return this if sorted by distance?
}

interface MapProps {
    center: [number, number];
    shops: Shop[];
}

function ChangeView({ center }: { center: [number, number] }) {
    const map = useMap();
    useEffect(() => {
        map.setView(center, map.getZoom());
    }, [center, map]);
    return null;
}

const Map = ({ center, shops }: MapProps) => {
    return (
        <MapContainer center={center} zoom={13} style={{ height: '100%', width: '100%' }}>
            <ChangeView center={center} />
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <Marker position={center} icon={icon}>
                <Popup>You are here</Popup>
            </Marker>
            {shops.map((shop, index) => (
                <Marker
                    key={index}
                    position={shop.document.location}
                    icon={icon}
                >
                    <Popup>
                        <div className="font-bold">{shop.document.shopName}</div>
                        <div className="text-sm">{shop.document.address}</div>
                        {shop.document.contact && <div className="text-xs text-gray-500">{shop.document.contact}</div>}
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
};

export default Map;
