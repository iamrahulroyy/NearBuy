export interface Shop {
    id: string;
    shopName: string;
    fullName: string;
    address: string;
    contact?: string;
    is_open: boolean;
    latitude: number;
    longitude: number;
    distance?: string; // Formatted distance for display (e.g., "1.2 km")
    distance_km?: number; // Actual distance in kilometers from backend
}

export interface Item {
    id: string;
    itemName: string;
    description: string;
    price: number;
    shop_id: string;
    stock_status: string;
}

export interface SearchResponse {
    document: {
        id: string;
        shopName: string;
        fullName: string;
        address: string;
        location: [number, number]; // [lat, lon]
        shop_id: string;
        // Add other fields as needed from Typesense response
    };
    highlight: any;
    text_match: number;
}
