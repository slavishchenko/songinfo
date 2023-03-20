import os
from slugify import slugify


def save_to_file(path: str, song: object, audio_analysis: object) -> bool:
    """path: path/to/directory where song files should be stored."""
    title = f"{song.artists} {song.name}"
    file_path = os.path.join(path, f"{slugify(title)}.txt")

    if not os.path.exists(file_path):
        write(file_path, song, audio_analysis)
        return True
    else:
        print(f"{slugify(title)}.txt already exists.")
        proceed = input("Do you want to overwrite the existing file? (Y/N): ").lower()
        if proceed in ["y", "n"]:
            match proceed:
                case "y":
                    write(file_path, song, audio_analysis)
                    return True
                case "n":
                    return False
        else:
            return False


def write(file_path: str, song: object, audio_analysis: object) -> bool:
    try:
        with open(file_path, "w") as f:
            f.write(f"Song Title: {song.name}")
            f.write(f"\nArtist Name: {song.artists}")
            f.write(
                f"\nAlbum: {song.album} ({song.album.release_date}) / ({song.album.album_type.capitalize()})"
            )
            f.write(f"\nTempo: {round(audio_analysis.tempo)} BPM")
            f.write(f"\nTime Signature: {audio_analysis.time_signature}/4")
            f.write(f"\nKey: {audio_analysis.key}")
            f.write(
                f"\nDuration: {round(audio_analysis.duration / 60, ndigits=2)} minutes"
            )
    except:
        return False
