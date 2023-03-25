import logging
import os
import sys
import time

import dotenv

from spotify.client import Client
from utils import save_to_file


logging.basicConfig(
    filename="logs.log",
    level=logging.WARNING,
    datefmt="%H:%M:%S",
)

dotenv.load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
PATH_TO_DIRECTORY = os.path.join(
    os.path.join(os.environ["USERPROFILE"]), "Desktop", "songs"
)
c = Client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)


def main():
    query = input("Search for a song: ")
    if query:
        search = c.search(query=query, limit=10)
        print("\n[Press CTRL + C to quit]")
        print(f"\nSearch results:\n")
        for i, song in enumerate(search.results, start=1):
            print(f"{i}. {song.artists} - {song.name}")
        try:
            song_index = int(input("\nChoose a song to see more details: "))
            if isinstance(song_index, int) and song_index in range(1, 11):
                song = search.results[song_index - 1]
                audio_analysis = c.get_audio_analysis(song.id)
                print(f"\n- - {song.artists} - {song.name} - -")
                print(
                    f"Album: {song.album} ({song.album.release_date}) / ({song.album.album_type})"
                )
                print(f"Tempo: {round(audio_analysis.tempo)} BPM")
                print(f"Time Signature: {audio_analysis.time_signature}/4")
                print(f"Key: {audio_analysis.key}")
                print(
                    f"Duration: {round(audio_analysis.duration / 60, ndigits=2)} minutes"
                )
                save = input("\nSave to a file? (Y/N): ").lower()
                if save in ["y", "n"]:
                    match save:
                        case "y":
                            if not os.path.exists(PATH_TO_DIRECTORY):
                                os.makedirs(PATH_TO_DIRECTORY)
                                if save_to_file(
                                    PATH_TO_DIRECTORY, song, audio_analysis
                                ):
                                    print(f"Saved!\nFile location: {PATH_TO_DIRECTORY}")
                                else:
                                    print("Something went wrong. Please, try again.")
                            else:
                                if save_to_file(
                                    PATH_TO_DIRECTORY, song, audio_analysis
                                ):
                                    print(f"Saved!\nFile location: {PATH_TO_DIRECTORY}")
                                else:
                                    print("Something went wrong. Please, try again.")
                        case "n":
                            quit()
                else:
                    print(
                        f'"{save}" is not a valid input.\nPlease, choose either "y" or "n".'
                    )
            else:
                print(
                    f'"{song_index}" is not a valid input.\nPlease, enter a value between 1 and 10.'
                )
        except ValueError:
            print("Please, enter a number between 1 and 10.")
    else:
        print("\nNo search query provided!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting..")
        time.sleep(0.1)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
