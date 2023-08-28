from audioparser.generics.music_objects import Track


def make_track_methods_string():
    methods_string = ''
    for index, method in enumerate(Track.GET_AND_DOWNLOAD_METHODS):
        if index == len(Track.GET_AND_DOWNLOAD_METHODS) - 1:
            methods_string += method
        else:
            methods_string += method + ', '
    return methods_string


