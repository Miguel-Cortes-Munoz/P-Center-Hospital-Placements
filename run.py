import os
from src.network_manager import NetworkManager
from src.model_logic import PCenterSolver
from src.visualizer import MapVisualizer

def main():
    PROVINCE_CSV = {
        "Alberta":                  "data/PopulationData/98-401-X2021006_English_CSV_data_Prairies.csv",
        "British Columbia":         "data/PopulationData/98-401-X2021006_English_CSV_data_BritishColumbia.csv",
        "Manitoba":                 "data/PopulationData/98-401-X2021006_English_CSV_data_Prairies.csv",
        "New Brunswick":            "data/PopulationData/98-401-X2021006_English_CSV_data_Atlantic.csv",
        "Newfoundland and Labrador":"data/PopulationData/98-401-X2021006_English_CSV_data_Atlantic.csv",
        "Northwest Territories":    "data/PopulationData/98-401-X2021006_English_CSV_data_Territories.csv",
        "Nova Scotia":              "data/PopulationData/98-401-X2021006_English_CSV_data_Atlantic.csv",
        "Nunavut":                  "data/PopulationData/98-401-X2021006_English_CSV_data_Territories.csv",
        "Ontario":                  "data/PopulationData/98-401-X2021006_English_CSV_data_Ontario.csv",
        "Prince Edward Island":     "data/PopulationData/98-401-X2021006_English_CSV_data_Atlantic.csv",
        "Quebec":                   "data/PopulationData/98-401-X2021006_English_CSV_data_Quebec.csv",
        "Saskatchewan":             "data/PopulationData/98-401-X2021006_English_CSV_data_Prairies.csv",
        "Yukon":                    "data/PopulationData/98-401-X2021006_English_CSV_data_Territories.csv",
    }
    
    place_input = input("Please enter a Canadian city (e.g. Coaldale, Alberta): ")
    
    parts = place_input.split(",")
    if len(parts) < 2:
        raise ValueError("Please provide the city and province (e.g., 'Lethbridge, Alberta')")
    
    province = parts[1].strip()
    pop_path = PROVINCE_CSV.get(province)
    
    if pop_path is None:
        raise ValueError(f"Unrecognized province: '{province}'. Check spelling and capitalization.")

    p_count = int(input("How many Hospitals? "))

    place_query = place_input + ", Canada"
    manager = NetworkManager(place_query)
    
    print(f"--- Loading map for {place_query} ---")
    graph = manager.load_graph()
    
    print(f"--- Loading demand data from {pop_path} ---")
    demand_weights = manager.load_demand_from_shapefile("data/DAdata/lda_000b21a_e.shp", pop_path)
    
    demand_nodes = list(demand_weights.keys())
    
    print("--- Computing distance matrix ---")
    distances = manager.compute_distances(demand_nodes)
    print("Done with distance computation.")

    print(f"--- Solving P-Center for p={p_count} ---")
    solver = PCenterSolver(demand_nodes, distances, p_count=p_count, weights=demand_weights)
    hospitals, max_dist = solver.solve()

    print(f"\nStatus: Optimal")
    print(f"Maximized Equity Distance: {max_dist:.3f} meters")
    for i, h in enumerate(hospitals, 1):
        print(f"Hospital {i} Location (Node ID): {h}")

    if not os.path.exists("images"):
        os.makedirs("images")

    viz = MapVisualizer(graph)
    safe_filename = place_input.replace(", ", "_").replace(" ", "_")
    output_path = f"images/{safe_filename}_p{p_count}.png"
    
    viz.save_map(hospitals, filename=output_path)
    print(f"--- Visualization saved to {output_path} ---")

if __name__ == "__main__":
    main()