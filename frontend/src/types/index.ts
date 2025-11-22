export interface Shop {
    id: string;
    shopName: string;
    fullName: string;
    address: string;
    contact?: string;
    is_open: boolean;
    latitude: number;
    longitude: number;
    distance?: string; // Calculated on frontend or returned by search
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
