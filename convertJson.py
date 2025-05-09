import csv
import json
import sys

def csv_to_geojson(csv_file, geojson_file=None, lat_field='lat', lon_field='long'):
    """
    Convert a CSV file with latitude and longitude columns to GeoJSON format.
    
    Args:
        csv_file: Path to the input CSV file
        geojson_file: Path to the output GeoJSON file (if None, prints to stdout)
        lat_field: Name of the latitude field in the CSV
        lon_field: Name of the longitude field in the CSV
    """
    features = []
    
    # Read CSV file
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip rows without coordinates
            if not row.get(lat_field) or not row.get(lon_field):
                continue
            
            # Try to convert lat/lon to float
            try:
                lat = float(row[lat_field])
                lon = float(row[lon_field])
            except ValueError:
                print(f"Warning: Could not convert coordinates for row: {row}")
                continue
            
            # Create a copy of the row without the coordinate fields to use as properties
            properties = {k: v for k, v in row.items() if k not in (lat_field, lon_field)}
            
            # Create a GeoJSON feature
            feature = {
                "type": "Feature",
                "properties": properties,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]  # GeoJSON uses [longitude, latitude] order
                }
            }
            
            features.append(feature)
    
    # Create the GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Write to file or stdout
    if geojson_file:
        with open(geojson_file, 'w') as f:
            json.dump(geojson, f, indent=2)
        print(f"Converted {len(features)} points to GeoJSON and saved to {geojson_file}")
    else:
        print(json.dumps(geojson, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python csv_to_geojson.py input.csv [output.geojson] [lat_field] [lon_field]")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    geojson_file = sys.argv[2] if len(sys.argv) > 2 else None
    lat_field = sys.argv[3] if len(sys.argv) > 3 else 'lat'
    lon_field = sys.argv[4] if len(sys.argv) > 4 else 'long'
    
    csv_to_geojson(csv_file, geojson_file, lat_field, lon_field)