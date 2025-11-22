'use client';

import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents } from 'react-leaflet';
import { Icon } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useEffect, useState } from 'react';
import { Shop } from '@/types';

// Fix for default marker icon
const defaultIcon = new Icon({
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
});

interface SearchMapProps {
    shops: Shop[];
    center?: [number, number];
    zoom?: number;
    onMarkerClick?: (shopId: string) => void;
    onMapClick?: (lat: number, lng: number) => void;
}

function MapController({ center, zoom }: { center: [number, number]; zoom: number }) {
    const map = useMap();
    useEffect(() => {
        map.setView(center, zoom);
    }, [center, zoom, map]);
    return null;
}

function MapEvents({ onMapClick }: { onMapClick?: (lat: number, lng: number) => void }) {
    useMapEvents({
        click(e) {
            onMapClick?.(e.latlng.lat, e.latlng.lng);
        },
    });
    return null;
}

export default function SearchMap({ shops, center = [51.505, -0.09], zoom = 13, onMarkerClick, onMapClick }: SearchMapProps) {
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) return <div className="h-full w-full bg-slate-900 animate-pulse" />;

    return (
        <MapContainer
            center={center}
            zoom={zoom}
            className="h-full w-full z-0"
            zoomControl={false}
        >
            {/* Light Theme Tile Layer */}
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
            />

            <MapController center={center} zoom={zoom} />
            <MapEvents onMapClick={onMapClick} />

            {shops.map((shop) => (
                <Marker
                    key={shop.id}
                    position={[shop.latitude, shop.longitude]}
                    icon={defaultIcon}
                    eventHandlers={{
                        click: () => onMarkerClick?.(shop.id),
                    }}
                >
                    <Popup className="custom-popup">
                        <div className="text-slate-900 font-semibold">{shop.shopName}</div>
                        <div className="text-slate-500 text-xs">{shop.address}</div>
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
}
