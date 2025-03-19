import dv_ui
import dv_api
import GeoCode_Geocoding
import Routes_OptimalPathFinding
import tiles2D_main

def main():
    # Call on data validation UI
    # Notes: Ideally a single screen should handle both address inputs,
    # however current implenation works perfectly good aside frim open/close flash
    start_address = dv_api.addyvally(dv_ui.dv_ui(0))
    dest_address = dv_api.addyvally(dv_ui.dv_ui(1))

    # Geocode initial and final Address
    start_latlng = GeoCode_Geocoding.Geocoding(start_address, None).get_coord()
    dest_latlng = GeoCode_Geocoding.Geocoding(dest_address, None).get_coord()

    # Destination address enviromental info search (To Be Added)

    # Call on route pathfinding (Temporary Fix)
    # Once route code is updated, save route related data items. (Distance, time, etc.)
    route = Routes_OptimalPathFinding.get_route(start_latlng, dest_latlng)

    # Ask user if additional route is desired
    # If yes, repeat process and add to route list
    # If no, preload tiles at all zoom levels with loading screen
    # (Maybe, To Be Added)

    # Initialize Viewport rendering
    tiles2D_main.main(route)

    # END OF CODE

if __name__ == "__main__":
    main()