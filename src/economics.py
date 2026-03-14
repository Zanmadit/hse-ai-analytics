def economic_effect(incidents):
    '''
    Calculates the projected economic impact.
    '''

    avg_cost = 5_000_000

    incidents_count = len(incidents)

    prevented = incidents_count * 0.38

    savings = prevented * avg_cost * 3

    before_hours = 72
    after_hours = 12
    saved_hours = before_hours - after_hours

    return prevented, savings, saved_hours