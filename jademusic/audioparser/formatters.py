def format_query(query):
    if query in ('0', ' '): query = ''
    return query.replace(' ', '+').lower()


def format_track_title(title):
    symbols_for_replace = str.maketrans({sym: None for sym in r'<>/:"\|?*&,'})
    formatted_title = title.translate(symbols_for_replace)
    return formatted_title


def make_number_prefix(track_num, tracks_count):
    if track_num is None or tracks_count is None:
        return
        
    if track_num == 0: 
        track_num = 1
        number_prefix = f'[{track_num}/{tracks_count}] '
    elif track_num:
        number_prefix = f'[{track_num+1}/{tracks_count}] '
    else:
        number_prefix = ''
    return number_prefix


def format_tracks_amount(query_params):
    tracks_amount = query_params.get('n')
    if tracks_amount is None:
        return 5
    return int(tracks_amount)


def validate_query(query):
    pass


def get_validated_query(query):
    validate_query(query)
    return query
