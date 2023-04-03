import logging
import os
import sys
import time

import dotenv

from songinfo import SongInfo
from spotify.client import Client

logging.basicConfig(
    filename="logs.log",
    level=logging.WARNING,
    datefmt="%H:%M:%S",
)

dotenv.load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

c = Client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
app = SongInfo()


def main():
    query = input("\nSearch for a song: ")
    if query:
        search = c.search(query=query, limit=10)
        print(f"\nSearch results:\n")
        for i, song in enumerate(search.results, start=1):
            app.display_results(index=i, song=song)
        song_index = app.get_song_index()
        if song_index == 0:
            main()
        else:
            song = search.results[song_index - 1]
            audio_analysis = c.get_audio_analysis(song.id)
            app.display_song_details(song, audio_analysis)
            save = app.save_promt()

            match save:
                case "n":
                    main()
                case "y":
                    app.save(song, audio_analysis)
                    main()
    else:
        print("\nNo search query provided!")


if __name__ == "__main__":
    try:
        print("\n[Press CTRL + C to quit]\n")
        main()
    except KeyboardInterrupt:
        print("\nExiting..")
        time.sleep(0.1)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
