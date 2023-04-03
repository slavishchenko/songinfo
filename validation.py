def valid_song_index(song_index: int) -> bool:
    return True if isinstance(song_index, int) and song_index in range(1, 11) else False


def valid_save_value(value: str):
    return True if value in ["y", "n"] else False
