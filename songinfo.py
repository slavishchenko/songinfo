import os

from utils import save_to_file
from validation import valid_save_value, valid_song_index


class SongInfo:
    path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop", "songs")

    @staticmethod
    def display_results(index: int, song: object):
        print(f"{index}. {song.artists} - {song.name}")

    @staticmethod
    def get_song_index():
        no_input = True
        while no_input:
            try:
                song_index = int(
                    input("\nChoose a song to see more details ['0' to go back]: ")
                )
                if song_index == 0:
                    no_input = False
                    return song_index
                elif valid_song_index(song_index):
                    no_input = False
                    return song_index
            except ValueError:
                print(f"Please, enter a value between 0 and 10.")

    @staticmethod
    def display_song_details(song: object, audio_analysis: object):
        print(f"\n- - {song.artists} - {song.name} - -")
        print(
            f"Album: {song.album} ({song.album.release_date}) / ({song.album.album_type})"
        )
        print(f"Tempo: {round(audio_analysis.tempo)} BPM")
        print(f"Time Signature: {audio_analysis.time_signature}/4")
        print(f"Key: {audio_analysis.key}")
        print(f"Duration: {audio_analysis.length} minutes")

    @staticmethod
    def save_promt():
        no_input = True
        while no_input:
            try:
                save = input("\nSave to a file? (Y/N): ").lower()
                if valid_save_value(save):
                    no_input = False
                    return save
                else:
                    print(f'\nPlease, choose either "y" or "n".')
            except:
                print(f'\nPlease, choose either "y" or "n".')

    def save(self, song: object, audio_analysis: object):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            if save_to_file(self.path, song, audio_analysis):
                print(f"Saved!\nFile location: {self.path}")
            else:
                print("Something went wrong. Please, try again.")
        else:
            if save_to_file(self.path, song, audio_analysis):
                print(f"Saved!\nFile location: {self.path}")
            else:
                print("Something went wrong. Please, try again.")
