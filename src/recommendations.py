def generate_recommendations(location_risk):
    '''
    Generates intelligent recommendations based on risk areas.
    '''
    
    top_locations = location_risk.head().index.tolist()
    recs = []
    for loc in top_locations:
        recs.append(f"Усилить контроль техники безопасности на объекте {loc}")
    return recs